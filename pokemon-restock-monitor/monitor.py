#!/usr/bin/env python3
"""Monitor de stock de Pokémon TCG con notificaciones instantáneas.

Vigila una lista de productos (Amazon, Pokémon Center, Best Buy, Walmart,
Target, GameStop, o cualquier URL) y te avisa al instante cuando alguno pasa
a disponible, con el link directo de compra.

  python monitor.py                 # inicia el monitoreo continuo
  python monitor.py --once          # una sola pasada (para probar)
  python monitor.py --test-notify   # manda una notificación de prueba
  python monitor.py --selftest      # prueba la lógica de detección (sin red)
  python monitor.py --config otro.yaml

IMPORTANTE: esta herramienta solo LEE páginas públicas y te NOTIFICA. No compra
por ti ni evade protecciones. Usa intervalos razonables y respeta los términos
de cada sitio. Para las tiendas más agresivas contra scraping (Target/Walmart),
combínala con servicios de push nativo; ver el README.
"""

import argparse
import datetime
import os
import random
import sys
import time

import yaml

import checkers
from notifier import Notifier
from store import Store

# Límites de cordura para no martillar a ninguna tienda.
MIN_INTERVAL = 30          # segundos mínimos entre revisiones de un mismo producto
GAP_BETWEEN_REQUESTS = (1.5, 4.0)  # pausa aleatoria entre productos, en segundos
MAX_BACKOFF = 8            # multiplicador máximo del intervalo al ser bloqueado


def log(msg):
    stamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{stamp}] {msg}", flush=True)


def load_dotenv(path=".env"):
    """Carga variables desde un archivo .env sin dependencias externas."""
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            val = val.strip().strip('"').strip("'")
            os.environ.setdefault(key.strip(), val)


class Config:
    def __init__(self):
        self.telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        self.telegram_chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
        self.discord_webhook = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()


def load_products(config_path, defaults):
    with open(config_path, "r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}

    file_defaults = raw.get("defaults", {})
    products = []
    for item in raw.get("products", []):
        if not item.get("url"):
            log(f"[!] Producto sin URL, se omite: {item.get('name', '???')}")
            continue
        p = dict(item)
        p["interval"] = max(
            MIN_INTERVAL,
            int(item.get("interval_seconds", file_defaults.get("interval_seconds", defaults["interval"]))),
        )
        p["jitter"] = int(item.get("jitter_seconds", file_defaults.get("jitter_seconds", defaults["jitter"])))
        p["timeout"] = int(item.get("timeout_seconds", file_defaults.get("timeout_seconds", defaults["timeout"])))
        p["name"] = item.get("name", p["url"])
        p["_next"] = 0.0
        p["_backoff"] = 1
        products.append(p)
    return products


def handle_result(product, result, store, notifier):
    key = product["url"]
    prev = store.get_state(key)
    name = product["name"]
    state = result.state

    label = {
        "in": "🟢 EN STOCK",
        "out": "⚪ agotado",
        "unknown": "❔ indeterminado",
        "blocked": "🚫 bloqueado (captcha/anti-bot)",
        "error": "⚠️  error de red",
    }.get(state, state)
    extra = f" http={result.status_code}" if result.status_code else ""
    log(f"{label}{extra} · {name}")

    if state == "in" and prev != "in":
        notifier.alert(name, product.get("retailer", ""), key, product.get("price"))

    # Solo persistimos estados fiables. En 'unknown/blocked/error' conservamos el
    # anterior para no disparar alertas falsas ni perder una transición real.
    if state in ("in", "out"):
        store.set_state(key, state)


def run(products, store, notifier, once=False):
    now = time.time()
    for p in products:
        p["_next"] = now  # revisa todo en la primera vuelta

    log(f"Monitoreando {len(products)} producto(s). Ctrl+C para detener.")
    while True:
        now = time.time()
        due = [p for p in products if p["_next"] <= now]
        due.sort(key=lambda p: p["_next"])

        for p in due:
            result = checkers.check_product(p, timeout=p["timeout"])
            handle_result(p, result, store, notifier)

            base = p["interval"]
            jitter = random.uniform(-p["jitter"], p["jitter"])
            if result.state in ("blocked", "error"):
                p["_backoff"] = min(p["_backoff"] * 2, MAX_BACKOFF)
                delay = base * p["_backoff"] + abs(jitter)
            else:
                p["_backoff"] = 1
                delay = base + jitter
            p["_next"] = time.time() + max(MIN_INTERVAL, delay)

            time.sleep(random.uniform(*GAP_BETWEEN_REQUESTS))

        if once:
            break

        upcoming = min(p["_next"] for p in products)
        time.sleep(max(1.0, min(upcoming - time.time(), 30.0)))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Monitor de stock de Pokémon TCG")
    parser.add_argument("--config", default="products.yaml", help="archivo de productos (YAML)")
    parser.add_argument("--once", action="store_true", help="una sola pasada y salir")
    parser.add_argument("--test-notify", action="store_true", help="enviar notificación de prueba")
    parser.add_argument("--selftest", action="store_true", help="probar la detección sin red")
    parser.add_argument("--env", default=".env", help="archivo de variables (por defecto .env)")
    args = parser.parse_args(argv)

    if args.selftest:
        print("Autoprueba de detección (offline):\n")
        return 0 if checkers.run_selftest() else 1

    load_dotenv(args.env)
    cfg = Config()
    notifier = Notifier(cfg)

    channels = ["consola"]
    if cfg.telegram_token and cfg.telegram_chat:
        channels.append("Telegram")
    if cfg.discord_webhook:
        channels.append("Discord")
    log(f"Canales de notificación activos: {', '.join(channels)}")
    if channels == ["consola"]:
        log("[i] Solo consola. Configura Telegram o Discord en .env para recibir push. Ver README.")

    if args.test_notify:
        notifier.test()
        return 0

    if not os.path.exists(args.config):
        log(f"[!] No existe '{args.config}'. Copia products.example.yaml y edítalo.")
        return 1

    defaults = {"interval": 90, "jitter": 30, "timeout": 20}
    products = load_products(args.config, defaults)
    if not products:
        log("[!] No hay productos válidos que monitorear.")
        return 1

    store = Store("state.json")
    try:
        run(products, store, notifier, once=args.once)
    except KeyboardInterrupt:
        log("Detenido por el usuario.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
