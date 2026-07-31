# Monitor de stock · Pokémon TCG

Vigila los productos que le indiques (**Amazon MX, Sanborns, Sears, Liverpool,
Walmart MX, Juguetrón, Juguetibici, Gameplanet, Costco**, tiendas Shopify
especializadas, o cualquier URL) y te **avisa al instante** cuando alguno pasa a
disponible, con el **link directo de compra**. Tú compras en un toque.

> **Qué hace y qué no.** Esto es un *monitor + notificador*. Lee páginas y
> endpoints públicos y te avisa. **No compra por ti, no rellena checkouts y no
> evade captchas ni protecciones anti-bot.** Es la ayuda legítima que te pone en
> la pista a tiempo; el clic de compra lo das tú. Así no arriesgas tu cuenta.

> 🇲🇽 **¿Dónde comprar en México, bots de alerta y precios en pesos?**
> Todo está en **[RECURSOS-MEXICO.md](RECURSOS-MEXICO.md)**: comunidades de
> alerta (Coleccio, Keepa, NowInStock MX…), tiendas por canal y precios MXN de
> referencia. En México, **la preventa le gana al restock** — empieza por ahí.

---

## 1. Instalación

Requiere Python 3.9+.

```bash
cd pokemon-restock-monitor
python3 -m venv .venv && source .venv/bin/activate   # opcional pero recomendado
pip install -r requirements.txt
```

## 2. Configura las notificaciones

```bash
cp .env.example .env
```

Abre `.env` y llena **solo el canal que quieras**:

- **Telegram (recomendado — push a tu teléfono, con botón "Comprar ahora"):**
  1. En Telegram escribe a **@BotFather**, manda `/newbot` y sigue los pasos. Te da un **token**.
  2. Escríbele cualquier cosa a tu nuevo bot (para que pueda contestarte).
  3. Consigue tu **chat_id**: escribe a **@userinfobot**, o abre
     `https://api.telegram.org/bot<TU_TOKEN>/getUpdates` y busca `"chat":{"id":...}`.
  4. Pega ambos en `.env` (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`).
- **Discord (opcional):** en tu servidor → Ajustes del canal → Integraciones →
  Webhooks → Nuevo webhook → Copiar URL → pégala en `DISCORD_WEBHOOK_URL`.

Prueba que llega:

```bash
python3 monitor.py --test-notify
```

## 3. Configura qué vigilar

```bash
cp products.example.yaml products.yaml
```

Edita `products.yaml` y pon **tus URLs reales** (abre el producto en la tienda y
copia el link). Ejemplo mínimo:

```yaml
defaults:
  interval_seconds: 120    # cada cuánto revisar (mínimo 30)
  jitter_seconds: 40       # variación aleatoria, para no tener patrón fijo

products:
  - name: "30th Celebration · ETB (Amazon MX preventa)"
    url: "https://www.amazon.com.mx/dp/B0H78BB9TY"
    retailer: amazon        # amazon | walmart | liverpool | sanborns | sears |
                            # costco | juguetron | juguetibici | gameplanet |
                            # delsol | coppel | mercadolibre | shopify | generic
    price: "$1,099 MXN"     # opcional, solo informativo
```

El archivo `products.example.yaml` ya trae ejemplos mexicanos listos (Amazon MX,
tienda Shopify, Sanborns, Gameplanet).

## 4. Ejecuta

```bash
python3 monitor.py            # monitoreo continuo (Ctrl+C para parar)
python3 monitor.py --once     # una sola pasada (para probar la config)
python3 monitor.py --selftest # prueba la lógica de detección, sin red
```

Cuando un producto pase de agotado a disponible, recibes la alerta con el link.
Solo avisa en la **transición** a disponible (no te spamea mientras siga en stock).

---

## Dejarlo corriendo 24/7

El monitor solo sirve si está encendido cuando cae el restock. Opciones:

- **En segundo plano (rápido):**
  ```bash
  nohup python3 monitor.py > monitor.log 2>&1 &
  ```
- **Servicio systemd (Linux, arranca solo):** crea `/etc/systemd/system/poke-monitor.service`
  apuntando a `ExecStart=/ruta/.venv/bin/python /ruta/monitor.py` y
  `systemctl enable --now poke-monitor`.
- **Host siempre encendido:** una Raspberry Pi, un VPS barato, o un contenedor.
  Mientras tenga internet y Python, funciona.

## Cómo detecta el stock

De más a menos fiable, y automático:

1. **Shopify** — si la URL es de un producto Shopify (`/products/<handle>`), usa
   el endpoint público `/products/<handle>.js` y lee el campo `available` (el
   dato de stock **oficial de la tienda**). La mayoría de tiendas especializadas
   mexicanas son Shopify (Colecciona, Kodama, Wunderbox, Juguetibici,
   Kantocards, Mushi-Mushi, Akibara, Lofty…). Es lo más confiable.
2. **JSON-LD** — lee el campo `availability` de schema.org (`InStock` /
   `OutOfStock` / `PreOrder`) del HTML. Funciona en muchas VTEX y WooCommerce
   (Liverpool, Juguetrón, Gameplanet, Chedraui…).
3. **Palabras clave** — texto de botón "Agregar al carrito" vs "Agotado", con
   variantes en español (México) e inglés por tienda.

## Afinar la detección

Si una tienda rara cambia su HTML y falla, define las señales tú mismo por producto:

```yaml
  - name: "Producto X"
    url: "https://tienda.example.com/x"
    retailer: generic
    in_signals: ["Agregar al carrito"]      # texto presente cuando SÍ hay
    out_signals: ["Agotado", "Sin existencias"]  # texto presente cuando NO hay
```

## Límites honestos (léelo)

- **Amazon MX, Walmart MX y Mercado Libre** son agresivos contra el scraping:
  pueden devolverte una página de captcha/bloqueo. El monitor lo detecta (estado
  `bloqueado`), aplica *backoff* y sigue, pero su fiabilidad ahí es baja. Para
  **Amazon MX** lo mejor es **Keepa** (alertas gratis de stock/precio, sin
  código). Este monitor rinde mejor en las **tiendas Shopify** (usa el dato
  oficial de stock) y en las que exponen JSON-LD (Liverpool, Sanborns, Gameplanet).
- **La alerta no es el cuello de botella real** en los drops más calientes: en
  México lo que de verdad te consigue producto a MSRP es la **preventa**
  (Amazon MX vendido por Amazon, o tienda especializada autorizada). Usa este
  monitor como una capa más, no como bala de plata. Ver **RECURSOS-MEXICO.md**.
- **Sé respetuoso:** no bajes `interval_seconds` a valores agresivos. Revisar
  cada 90–120 s por producto es suficiente y evita que te bloqueen.

## Estructura

| Archivo | Qué hace |
|---|---|
| `monitor.py` | Bucle principal, planificador, CLI |
| `checkers.py` | Descarga y detección de stock por tienda |
| `notifier.py` | Notificaciones Telegram / Discord / consola |
| `store.py` | Estado persistente (evita alertas repetidas) |
| `products.example.yaml` | Plantilla de productos a vigilar |
| `.env.example` | Plantilla de tokens de notificación |
| `RECURSOS-MEXICO.md` | Bots de alerta, tiendas y precios MXN |

`products.yaml`, `.env` y `state.json` están en `.gitignore`: tus datos y
tokens no se suben al repositorio.
