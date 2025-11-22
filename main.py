from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Название магазина
SHOP_NAME = "💎 Libelle 💎"

# Категории товаров
categories = {
    "rings": "Кольца",
    "necklaces": "Ожерелья",
    "bracelets": "Браслеты"
}

# Товары по категориям
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

# /start — приветствие и категории
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"Добро пожаловать в {SHOP_NAME}!\n\nВыберите категорию украшений:"
    keyboard = [[InlineKeyboardButton(name, callback_data=f"cat_{key}")] for key, name in categories.items()]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# Выбор категории — показать товары
async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    cat_key = query.data.replace("cat_", "")
    items = products.get(cat_key, [])
    
    if not items:
        await query.edit_message_text("В этой категории пока нет товаров.")
        return
    
    keyboard = [[InlineKeyboardButton(item["name"], callback_data=f"prod_{item['id']}")] for item in items]
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back")])
    
    await query.edit_message_text(f"Выберите товар из категории «{categories[cat_key]}»:", reply_markup=InlineKeyboardMarkup(keyboard))

# Показ информации о товаре
async def show_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    prod_id = query.data.replace("prod_", "")
    # Найдем товар
    product = None
    for items in products.values():
        for p in items:
            if p["id"] == prod_id:
                product = p
                break
    if not product:
        await query.edit_message_text("Товар не найден.")
        return
    
    text = f"**{product['name']}**\nЦена: {product['price']}₴\n\n{product['description']}"
    keyboard = [[InlineKeyboardButton("🛒 Купить", callback_data=f"buy_{product['id']}")],
                [InlineKeyboardButton("🔙 Назад", callback_data="back")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# Оформление покупки (пока просто сообщение)
async def buy_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    prod_id = query.data.replace("buy_", "")
    product = None
    for items in products.values():
        for p in items:
            if p["id"] == prod_id:
                product = p
                break
    if not product:
        await query.edit_message_text("Товар не найден.")
        return
    
    await query.edit_message_text(f"Спасибо за покупку *{product['name']}*!\nНаш менеджер свяжется с вами для оформления заказа.", parse_mode="Markdown")

# Обработка кнопки назад
async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context)

# Создаем приложение
application = ApplicationBuilder().token("8247000975:AAGWPSSNYcygmHphOONHn4nPsOh2AQsmz4Q").build()

# Хэндлеры
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(show_category, pattern="^cat_"))
application.add_handler(CallbackQueryHandler(show_product, pattern="^prod_"))
application.add_handler(CallbackQueryHandler(buy_product, pattern="^buy_"))
application.add_handler(CallbackQueryHandler(go_back, pattern="^back$"))

# Запуск
application.run_polling()
