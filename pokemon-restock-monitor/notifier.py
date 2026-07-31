"""Envío de notificaciones cuando un producto pasa a disponible.

Canales soportados (se activan solos si defines sus variables de entorno):
  - Telegram  -> push a tu teléfono, con botón "Comprar ahora" (recomendado)
  - Discord   -> mensaje a un webhook de tu servidor/canal
  - Consola   -> siempre; imprime en la terminal con un beep

La notificación incluye el link directo al producto para que compres tú mismo
en un toque. Esta herramienta NO compra por ti.
"""

import html as _html
import sys

import requests


def _esc(text):
    return _html.escape(str(text))


def send_telegram(token, chat_id, name, retailer, url, price=None):
    api = f"https://api.telegram.org/bot{token}/sendMessage"
    lines = ["🔔 <b>¡EN STOCK!</b>", _esc(name)]
    if retailer:
        lines.append(f"🏬 {_esc(retailer)}")
    if price:
        lines.append(f"💲 {_esc(price)}")
    payload = {
        "chat_id": chat_id,
        "text": "\n".join(lines),
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
        "reply_markup": {
            "inline_keyboard": [[{"text": "🛒 Comprar ahora", "url": url}]]
        },
    }
    resp = requests.post(api, json=payload, timeout=15)
    resp.raise_for_status()


def send_discord(webhook_url, name, retailer, url, price=None):
    parts = [f"🔔 **¡EN STOCK!** {name}"]
    if retailer:
        parts.append(f"🏬 {retailer}")
    if price:
        parts.append(f"💲 {price}")
    parts.append(url)
    payload = {"content": "\n".join(parts)}
    resp = requests.post(webhook_url, json=payload, timeout=15)
    resp.raise_for_status()


def console_alert(name, retailer, url):
    # \a hace sonar el beep de la terminal.
    sys.stdout.write("\a")
    print(f"\n{'='*60}\n🔔  ¡EN STOCK!  {name}")
    if retailer:
        print(f"    Tienda: {retailer}")
    print(f"    Link:   {url}\n{'='*60}\n")


class Notifier:
    def __init__(self, cfg):
        self.cfg = cfg

    def alert(self, name, retailer, url, price=None):
        """Envía por todos los canales configurados. Nunca deja de avisar por
        consola aunque falle un canal remoto."""
        console_alert(name, retailer, url)

        cfg = self.cfg
        if cfg.telegram_token and cfg.telegram_chat:
            try:
                send_telegram(cfg.telegram_token, cfg.telegram_chat, name, retailer, url, price)
            except Exception as exc:  # noqa: BLE001 - queremos seguir con otros canales
                print(f"    [!] Falló Telegram: {exc}")

        if cfg.discord_webhook:
            try:
                send_discord(cfg.discord_webhook, name, retailer, url, price)
            except Exception as exc:  # noqa: BLE001
                print(f"    [!] Falló Discord: {exc}")

    def test(self):
        """Manda una notificación de prueba por cada canal configurado."""
        name = "PRUEBA · Monitor de stock funcionando ✅"
        url = "https://tcg.pokemon.com/en-us/expansions/30th-celebration/"
        self.alert(name, "Autoprueba", url, price="$0.00")
        channels = ["consola"]
        if self.cfg.telegram_token and self.cfg.telegram_chat:
            channels.append("Telegram")
        if self.cfg.discord_webhook:
            channels.append("Discord")
        print(f"Notificación de prueba enviada por: {', '.join(channels)}")
