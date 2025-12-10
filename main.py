from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Назва магазину
SHOP_NAME = "💎 Libelle 💎"

# Категорії товарів
categories = {
    "rings": "Кільця",
    "necklaces": "Намиста",
    "bracelets": "Браслети"
}

# Товари по категоріях
products = {
    "rings": [
        {"id": "ring1", "name": "Золоте кільце", "price": 0, "description": "Вишукана золота каблучка на будь-який випадок."},
        {"id": "ring2", "name": "Срібне кільце", "price": 0, "description": "Елегантна каблучка зі срібла."}
    ],
    "necklaces": [
        {"id": "necklace1", "name": "Намисто з каменем", "price": 0, "description": "Чудове намисто з натуральним каменем."}
    ],
    "bracelets": [
        {"id": "bracelet1", "name": "Браслет з камінням", "price": 0, "description": "Браслет з натуральними каменями, ручна робота."}
    ]
}

# /start — привітання та категорії
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"Ласкаво просимо до {SHOP_NAME}! ✨\n\nОберіть категорію прикрас:"
    keyboard = [[InlineKeyboardButton(name, callback_data=f"cat_{key}")] for key, name in categories.items()]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# Вибір категорії — показ товарів
async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
   
    cat_key = query.data.replace("cat_", "")
    items = products.get(cat_key, [])
   
    if not items:
        await query.edit_message_text("У цій категорії поки що немає товарів.")
        return
   
    keyboard = [[InlineKeyboardButton(item["name"], callback_data=f"prod_{item['id']}")] for item in items]
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back")])
   
    await query.edit_message_text(f"Оберіть прикрасу з категорії «{categories[cat_key]}»:", 
                                  reply_markup=InlineKeyboardMarkup(keyboard))

# Показ інформації про товар
async def show_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
   
    prod_id = query.data.replace("prod_", "")
    product = None
    for items in products.values():
        for p in items:
            if p["id"] == prod_id:
                product = p
                break
        if product:
            break
    
    if not product:
        await query.edit_message_text("Товар не знайдено.")
        return
   
    text = f"*{product['name']}*\nЦіна: {product['price']} ₴\n\n{product['description']}"
    keyboard = [
        [InlineKeyboardButton("🛒 Купити", callback_data=f"buy_{product['id']}")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# Оформлення покупки
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
        if product:
            break
    
    if not product:
        await query.edit_message_text("Товар не знайдено.")
        return
   
    await query.edit_message_text(
        f"Дякуємо за покупку *{product['name']}*! 🎉\n\nНаш менеджер зв'яжеться з вами найближчим часом для оформлення замовлення та узгодження деталей доставки.",
        parse_mode="Markdown"
    )

# Кнопка «Назад»
async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # Повернення до головного меню
    await start(update, context)

# Створення додатка
application = ApplicationBuilder().token("8247000975:AAGWPSSNYcygmHphOONHn4nPsOh2AQsmz4Q").build()

# Хендлери
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(show_category, pattern="^cat_"))
application.add_handler(CallbackQueryHandler(show_product, pattern="^prod_"))
application.add_handler(CallbackQueryHandler(buy_product, pattern="^buy_"))
application.add_handler(CallbackQueryHandler(go_back, pattern="^back$"))

# Запуск бота
print("Бот запущений...")
application.run_polling()
