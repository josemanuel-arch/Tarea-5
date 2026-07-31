"""Detección de disponibilidad (stock) por producto — enfocado en México.

Estrategia de detección, de más a menos fiable:

  1. Shopify: si la URL es de un producto Shopify (`/products/<handle>`), se
     consulta el endpoint público `/products/<handle>.js` y se lee el campo
     `available` (dato oficial de la tienda). La mayoría de tiendas
     especializadas mexicanas (Colecciona, Kodama, Juguetibici, Wunderbox,
     Kantocards, Mushi-Mushi, Akibara, Lofty...) son Shopify.
  2. JSON-LD: se busca el campo schema.org `availability` (InStock / OutOfStock
     / PreOrder) en el HTML. Funciona en muchas tiendas VTEX y WooCommerce
     (Liverpool, Juguetron, Gameplanet, Chedraui...).
  3. Palabras clave: texto de botón "Agregar al carrito" vs "Agotado", con
     variantes en español e inglés por tienda.

Es un MONITOR: solo lee páginas/endpoints públicos y avisa. No automatiza la
compra ni evade protecciones anti-bot.
"""

import json
import re
from urllib.parse import urlsplit, urlunsplit

import requests

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
}

# Señales de texto por tienda (en minúsculas). Cubren español (México) e inglés.
# 'in' = disponible/comprable; 'out' = agotado/no disponible.
RETAILER_PRESETS = {
    "amazon": {
        "in": ["agregar al carrito", "comprar ahora", "realizar pedido anticipado",
                "en stock", "add to cart", "buy now"],
        "out": ["actualmente no disponible", "no disponible", "temporalmente agotado",
                "currently unavailable", "no disponible."],
    },
    "walmart": {
        "in": ["agregar al carrito", "comprar ahora", "agregar", "add to cart"],
        "out": ["sin existencia", "agotado", "no disponible", "out of stock"],
    },
    "liverpool": {
        "in": ["agregar a la bolsa", "comprar ahora"],
        "out": ["agotado", "producto no disponible", "sin inventario"],
    },
    "sanborns": {
        "in": ["agregar a la bolsa", "comprar"],
        "out": ["agotado", "no disponible", "producto no disponible"],
    },
    "sears": {
        "in": ["agregar a la bolsa", "comprar"],
        "out": ["agotado", "no disponible", "producto no disponible"],
    },
    "costco": {
        "in": ["agregar al carrito"],
        "out": ["agotado", "no disponible"],
    },
    "juguetron": {  # VTEX
        "in": ["agregar al carrito", "comprar ahora"],
        "out": ["producto no disponible", "agotado", "avísame"],
    },
    "juguetibici": {  # Shopify
        "in": ["agregar al carrito"],
        "out": ["agotado"],
    },
    "gameplanet": {  # WooCommerce
        "in": ["añadir al carrito", "agregar al carrito"],
        "out": ["agotado", "sin existencias"],
    },
    "delsol": {
        "in": ["agregar al carrito"],
        "out": ["agotado", "no disponible", "sin existencias"],
    },
    "coppel": {
        "in": ["agregar al carrito", "comprar ahora"],
        "out": ["agotado", "no disponible", "sin stock"],
    },
    "mercadolibre": {
        "in": ["disponible", "disponibles", "última disponible"],
        "out": ["sin stock", "publicación pausada", "finalizada"],
    },
    "shopify": {
        "in": ["agregar al carrito", "añadir al carrito", "add to cart"],
        "out": ["agotado", "sold out"],
    },
    "woocommerce": {
        "in": ["añadir al carrito", "agregar al carrito", "add to cart"],
        "out": ["agotado", "sin existencias", "out of stock"],
    },
    # Preventa (preorder): comprable. Se listan aparte para reutilizar.
    "preventa_in": ["realizar pedido anticipado", "preordenar", "reservar"],
    "preventa_out": ["preventa agotada", "preorder sold out"],
    "generic": {
        "in": ["agregar al carrito", "añadir al carrito", "comprar ahora", "comprar",
                "disponible", "add to cart", "buy now", "in stock"],
        "out": ["agotado", "no disponible", "sin existencias", "sin stock",
                "out of stock", "sold out", "unavailable"],
    },
}

# La tienda te sirvió una página de bloqueo/captcha en vez del producto.
BLOCK_SIGNALS = [
    "captcha", "robot check", "are you a human", "verify you are a human",
    "enable javascript", "access denied", "request blocked", "unusual traffic",
    "pardon our interruption", "lo sentimos, algo salió mal",
]

_AVAIL_RE = re.compile(r'"availability"\s*:\s*"([^"]+)"', re.IGNORECASE)


class CheckResult:
    """state: 'in' | 'out' | 'unknown' | 'blocked' | 'error'."""

    def __init__(self, state, status_code=None, note=""):
        self.state = state
        self.status_code = status_code
        self.note = note

    def __repr__(self):
        return f"<CheckResult {self.state} http={self.status_code} {self.note}>"


def _preset_for(product):
    retailer = (product.get("retailer") or "generic").lower()
    preset = RETAILER_PRESETS.get(retailer)
    if not isinstance(preset, dict) or "in" not in preset:
        preset = RETAILER_PRESETS["generic"]
    return preset


# ---------------------------- Shopify (.js) ----------------------------------

def shopify_js_url(product):
    """Devuelve la URL del endpoint .js de Shopify, o None si no aplica.

    Se activa si el producto declara `platform: shopify` o si la URL contiene
    `/products/<handle>`. Se puede desactivar con `platform: none`.
    """
    platform = (product.get("platform") or "").lower()
    if platform == "none":
        return None
    url = product["url"]
    parts = urlsplit(url)
    path = parts.path
    if platform != "shopify" and "/products/" not in path:
        return None
    # Toma la ruta hasta el handle del producto y agrega .js
    idx = path.find("/products/")
    if idx == -1:
        return None
    tail = path[idx + len("/products/"):]
    handle = tail.split("/")[0]
    if not handle:
        return None
    if handle.endswith(".js") or handle.endswith(".json"):
        new_path = path[:idx] + "/products/" + handle
    else:
        new_path = path[:idx] + "/products/" + handle + ".js"
    return urlunsplit((parts.scheme, parts.netloc, new_path, "", ""))


def _parse_shopify(payload):
    """Lee el JSON de Shopify (.js). Disponible si el producto o alguna
    variante tiene available=true."""
    try:
        data = json.loads(payload)
    except (json.JSONDecodeError, TypeError):
        return "unknown"
    if isinstance(data, dict):
        if data.get("available") is True:
            return "in"
        variants = data.get("variants") or []
        if any(v.get("available") for v in variants if isinstance(v, dict)):
            return "in"
        if "available" in data or variants:
            return "out"
    return "unknown"


# ---------------------------- JSON-LD ----------------------------------------

def _jsonld_state(text):
    """Estado a partir del campo schema.org availability. None si no hay señal."""
    values = [m.lower() for m in _AVAIL_RE.findall(text)]
    if not values:
        return None
    has_in = any(("instock" in v or "preorder" in v or "backorder" in v or
                  "onlineonly" in v or "limitedavailability" in v) for v in values)
    has_out = any(("outofstock" in v or "soldout" in v or "discontinued" in v) for v in values)
    if has_in and not has_out:
        return "in"
    if has_out and not has_in:
        return "out"
    return None  # ambiguo: hay disponibles y agotados en la página


# ---------------------------- Detección HTML ---------------------------------

def detect_state(html, product):
    text = html.lower()

    if any(sig in text for sig in BLOCK_SIGNALS):
        return "blocked"

    preset = _preset_for(product)
    out_signals = [s.lower() for s in (product.get("out_signals") or preset["out"])]
    in_signals = [s.lower() for s in (product.get("in_signals") or preset["in"])]

    # 1) Señales personalizadas del usuario mandan.
    if product.get("out_signals") and any(sig in text for sig in out_signals):
        return "out"
    if product.get("in_signals") and any(sig in text for sig in in_signals):
        return "in"

    # 2) JSON-LD schema.org availability (fiable y multiplataforma).
    ld = _jsonld_state(text)
    if ld is not None:
        return ld

    # 3) Preventa agotada / preventa activa (antes que las señales genéricas).
    if any(sig in text for sig in RETAILER_PRESETS["preventa_out"]):
        return "out"
    if any(sig in text for sig in RETAILER_PRESETS["preventa_in"]):
        return "in"

    # 4) Palabras clave del preset. "Agotado" tiene prioridad.
    if any(sig in text for sig in out_signals):
        return "out"
    if any(sig in text for sig in in_signals):
        return "in"
    return "unknown"


# ---------------------------- Revisión de un producto ------------------------

def check_product(product, timeout=20):
    """Descarga y evalúa. Prioriza el endpoint Shopify si aplica."""
    headers = dict(DEFAULT_HEADERS)

    js_url = shopify_js_url(product)
    if js_url:
        try:
            resp = requests.get(js_url, headers=headers, timeout=timeout)
            if resp.status_code == 200 and resp.text.strip().startswith("{"):
                state = _parse_shopify(resp.text)
                if state in ("in", "out"):
                    return CheckResult(state, status_code=resp.status_code, note="shopify")
            # Si el .js no sirvió, caemos al HTML normal.
        except requests.RequestException:
            pass  # caer al HTML

    try:
        resp = requests.get(product["url"], headers=headers, timeout=timeout, allow_redirects=True)
    except requests.RequestException as exc:
        return CheckResult("error", note=str(exc)[:200])

    if resp.status_code in (403, 429, 503):
        return CheckResult("blocked", status_code=resp.status_code)
    if resp.status_code >= 400:
        return CheckResult("error", status_code=resp.status_code)

    return CheckResult(detect_state(resp.text, product), status_code=resp.status_code)


# ---- Autoprueba offline (no toca ninguna tienda ni red) ---------------------

_SELFTEST_CASES = [
    # retailer, html/json, esperado, ¿es shopify .js?
    ("amazon", "<div>Actualmente no disponible.</div>", "out", False),
    ("amazon", "<span id='add-to-cart-button'>Agregar al Carrito</span>", "in", False),
    ("liverpool", "<button>Agregar a la bolsa</button>", "in", False),
    ("liverpool", "<div>Producto no disponible</div>", "out", False),
    ("gameplanet", "<p class='stock out-of-stock'>Agotado</p>", "out", False),
    ("sanborns", "<button>Agregar a la bolsa</button>", "in", False),
    ("generic", '<script>{"@type":"Product","offers":{"availability":"https://schema.org/InStock"}}</script>', "in", False),
    ("generic", '<script>{"offers":{"availability":"https://schema.org/OutOfStock"}}</script>', "out", False),
    ("generic", "<p>por favor verify you are a human</p>", "blocked", False),
    ("juguetibici", '{"available": true, "variants": [{"available": false}]}', "in", True),
    ("juguetibici", '{"available": false, "variants": [{"available": false}]}', "out", True),
]


def run_selftest():
    ok = 0
    for retailer, payload, expected, is_js in _SELFTEST_CASES:
        if is_js:
            got = _parse_shopify(payload)
        else:
            got = detect_state(payload, {"retailer": retailer})
        mark = "OK " if got == expected else "XX "
        if got == expected:
            ok += 1
        kind = "shopify.js" if is_js else "html"
        print(f"  {mark} [{retailer:12} {kind:10}] esperado={expected!r} obtenido={got!r}")
    print(f"\n{ok}/{len(_SELFTEST_CASES)} casos correctos")
    return ok == len(_SELFTEST_CASES)
