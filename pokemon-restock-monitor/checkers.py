"""Detección de disponibilidad (stock) por producto.

Enfoque legítimo: se descarga la página pública del producto y se buscan
señales de texto que indican si está disponible para comprar o agotado.
NO automatiza la compra ni evade protecciones anti-bot: solo lee y avisa.

La detección por palabras clave es heurística. Cada tienda cambia su HTML
con el tiempo, así que puedes sobreescribir las señales por producto en el
archivo de configuración con `in_signals` / `out_signals`.
"""

import time
import random

import requests

# User-Agent realista de navegador. Puedes cambiarlo si una tienda te bloquea.
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
}

# Señales por tienda (en minúsculas). Se cubren variantes en inglés y español
# para que funcione tanto en amazon.com como en amazon.com.mx, etc.
RETAILER_PRESETS = {
    "amazon": {
        "in": ["add to cart", "buy now", "agregar al carrito", "comprar ya", "add to basket"],
        "out": [
            "currently unavailable", "no disponible actualmente",
            "see all buying options", "ver todas las opciones de compra",
            "temporarily out of stock", "no está disponible",
        ],
    },
    "target": {
        "in": ["add to cart", "ship it", "pick it up", "agregar al carrito"],
        "out": ["out of stock", "sold out", "agotado", "temporarily out of stock"],
    },
    "walmart": {
        "in": ["add to cart", "agregar al carrito", "buy now"],
        "out": ["out of stock", "not available", "agotado", "sold out"],
    },
    "bestbuy": {
        "in": ["add to cart"],
        "out": ["sold out", "coming soon", "agotado"],
    },
    "gamestop": {
        "in": ["add to cart", "pre-order"],
        "out": ["not available", "out of stock", "agotado", "unavailable"],
    },
    "pokemoncenter": {
        "in": ["add to cart", "agregar al carrito"],
        "out": ["sold out", "out of stock", "agotado", "coming soon"],
    },
    # 'generic' se usa cuando no reconoces la tienda: cubre lo más común.
    "generic": {
        "in": ["add to cart", "buy now", "agregar al carrito", "comprar", "in stock", "disponible"],
        "out": ["out of stock", "sold out", "unavailable", "agotado", "no disponible"],
    },
}

# Marcas de que la tienda te sirvió una página de bloqueo / captcha en vez del producto.
BLOCK_SIGNALS = [
    "captcha", "robot check", "are you a human", "verify you are a human",
    "enable javascript", "access denied", "request blocked", "unusual traffic",
    "pardon our interruption",
]


class CheckResult:
    """Resultado de una revisión.

    state: 'in' (disponible), 'out' (agotado), 'unknown' (no se pudo determinar),
           'blocked' (la tienda devolvió captcha/bloqueo), 'error' (fallo de red).
    """

    def __init__(self, state, status_code=None, note=""):
        self.state = state
        self.status_code = status_code
        self.note = note

    def __repr__(self):
        return f"<CheckResult {self.state} http={self.status_code} {self.note}>"


def _preset_for(product):
    retailer = (product.get("retailer") or "generic").lower()
    return RETAILER_PRESETS.get(retailer, RETAILER_PRESETS["generic"])


def detect_state(html, product):
    """Decide el estado a partir del HTML descargado."""
    text = html.lower()

    if any(sig in text for sig in BLOCK_SIGNALS):
        return "blocked"

    preset = _preset_for(product)
    out_signals = [s.lower() for s in (product.get("out_signals") or preset["out"])]
    in_signals = [s.lower() for s in (product.get("in_signals") or preset["in"])]

    # "Agotado" tiene prioridad: si aparece, lo damos por no disponible.
    if out_signals and any(sig in text for sig in out_signals):
        return "out"
    if in_signals and any(sig in text for sig in in_signals):
        return "in"
    return "unknown"


def check_product(product, timeout=20):
    """Descarga la página del producto y devuelve un CheckResult."""
    url = product["url"]
    headers = dict(DEFAULT_HEADERS)
    # Pequeña variación del Accept-Language para no repetir una huella idéntica.
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
    except requests.RequestException as exc:
        return CheckResult("error", note=str(exc)[:200])

    if resp.status_code in (403, 429, 503):
        # Rechazo típico de anti-bot / rate limit.
        return CheckResult("blocked", status_code=resp.status_code)
    if resp.status_code >= 400:
        return CheckResult("error", status_code=resp.status_code)

    state = detect_state(resp.text, product)
    return CheckResult(state, status_code=resp.status_code)


# ---- Autoprueba offline de la lógica de detección (no toca ninguna tienda) ----

_SELFTEST_CASES = [
    ("amazon", "<html><button>Add to Cart</button></html>", "in"),
    ("amazon", "<div>Currently unavailable</div><button>Add to Cart</button>", "out"),
    ("amazon", "<div>No disponible actualmente</div>", "out"),
    ("pokemoncenter", "<button>Add to Cart</button>", "in"),
    ("pokemoncenter", "<span>Sold Out</span>", "out"),
    ("bestbuy", "<div>Coming Soon</div>", "out"),
    ("target", "<button>Add to cart</button>", "in"),
    ("generic", "<p>Please verify you are a human</p>", "blocked"),
    ("generic", "<p>algo sin señales</p>", "unknown"),
]


def run_selftest():
    ok = 0
    for retailer, html, expected in _SELFTEST_CASES:
        got = detect_state(html, {"retailer": retailer})
        mark = "OK " if got == expected else "XX "
        if got == expected:
            ok += 1
        print(f"  {mark} [{retailer}] esperado={expected!r} obtenido={got!r}")
    print(f"\n{ok}/{len(_SELFTEST_CASES)} casos correctos")
    return ok == len(_SELFTEST_CASES)
