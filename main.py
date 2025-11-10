import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === НАСТРОЙКИ ===
SHOP_NAME = "Libelle"
TOKEN = os.environ['TELEGRAM_TOKEN']
PORT = int(os.environ.get('PORT', 8000))  # Koyeb требует 8000

# Категории
categories = {
    "rings": "Кольца",
    "necklaces": "Ожерелья",
    "bracelets": "Браслеты"
}

# Товары
products = {
    "rings": [
        {"id": "ring1", "name": "Золотое кольцо", "price": 5000, "description": "Изысканное золотое кольцо для любого случая."},
        {"id": "ring2", "name": "Серебряное кольцо", "price": 3000, "description": "Элегантное кольцо из серебра."}
    ],
    "necklaces": [
        {"id": "necklace1", "name": "Ожерелье с камнем", "price": 4500, "description": "Прекрасное ожерелье с натуральным камнем."}
    ],
    "bracelets": [
        {"id": "bracelet1", "name": "Браслет с камнями", "price": 4000, "description": "Браслет с натуральными камнями, ручная работа."}
    ]
}

# === ХЕНДЛЕРЫ ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"Добро пожаловать в {SHOP_NAME}!\n\nВыберите категорию украшений:"
    keyboard = [[InlineKeyboardButton(name, callback_data=f"cat_{key}")] for key, name in categories.items()]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cat_key = query.data.replace("cat_", "")
    items = products.get(cat_key, [])
    if not items:
        await query.edit_message_text("Товаров нет.")
        return
    keyboard = [[InlineKeyboardButton(p["name"], callback_data=f"prod_{p['id']}")] for p in items]
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])
    await query.edit_message_text(f"«{categories[cat_key]}» — выберите товар:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    prod_id = query.data.replace("prod_", "")
    product = next((p for items in products.values() for p in items if p["id"] == prod_id), None)
    if not product:
        await query.edit_message_text("Товар не найден.")
        return
    text = f"**{product['name']}**\nЦена: {product['price']}₴\n\n{product['description']}"
    keyboard = [
        [InlineKeyboardButton("Купить", callback_data=f"buy_{product['id']}")],
        [InlineKeyboardButton("Назад", callback_data="back")]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def buy_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    prod_id = query.data.replace("buy_", "")
    product = next((p for items in products.values() for p in items if p["id"] == prod_id), None)
    if not product:
        await query.edit_message_text("Товар не найден.")
        return
    await query.edit_message_text(
        f"Спасибо за покупку *{product['name']}*!\nМенеджер свяжется с вами.",
        parse_mode="Markdown"
    )

async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = f"Добро пожаловать в {SHOP_NAME}!\n\nВыберите категорию:"
    keyboard = [[InlineKeyboardButton(name, callback_data=f"cat_{key}")] for key, name in categories.items()]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# === ЗАПУСК ===
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_category, pattern=r"^cat_"))
    app.add_handler(CallbackQueryHandler(show_product, pattern=r"^prod_"))
    app.add_handler(CallbackQueryHandler(buy_product, pattern=r"^buy_"))
    app.add_handler(CallbackQueryHandler(go_back, pattern=r"^back$"))

    # WEBHOOK — РАБОТАЕТ НА KOyeb
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=None  # Koyeb сам подставит https://твой-домен.koyeb.app/ТОКЕН
    )