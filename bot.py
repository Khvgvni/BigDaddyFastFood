import logging
import csv
import os
import openpyxl
from typing import Dict
from dotenv import load_dotenv
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, ContextTypes, filters
)

load_dotenv()

# 🔑 Настройки
TOKEN = "8259299108:AAEGFbhRHAd0Zjy4yX6z2MA27QnoZas0LvI"
GROUP_CHAT_ID = -1005018392524
PRIVACY_URL = os.getenv("PRIVACY_URL", "https://docs.google.com/document/...")
ADMINS = [150203692]

# Маппинг: id сообщения в группе → id пользователя
ROUTE: Dict[int, int] = {}

# Клавиатура «завершить чат»
STOP_KB = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⛔ Завершить чат", callback_data="stop_chat")]]
)

# 📌 Медиа
WELCOME_IMG = os.path.join(os.path.dirname(__file__), "Welcome.jpg")
INVITE_IMG = os.path.join(os.path.dirname(__file__), "Invitation-new.png")

# 📌 Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 📌 Состояния
REG_NAME, REG_PHONE, TEAM_NAME, TEAM_PHONE, TEAM_ROLE = range(5)

# ---------- УТИЛИТЫ ----------
def nav_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]])

def get_user_data(user_id: int):
    try:
        with open("users.csv", "r", encoding="utf-8") as f:
            r = csv.reader(f, delimiter=";")
            next(r, None)
            for row in r:
                if len(row) >= 4 and row[2] == str(user_id):
                    return row
    except FileNotFoundError:
        return None
    return None

def is_registered(user_id: int) -> bool:
    return get_user_data(user_id) is not None

def save_post(file_id: str, caption: str):
    new_file = not os.path.exists("posts.csv")
    with open("posts.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        if new_file:
            writer.writerow(["file_id", "caption"])
        writer.writerow([file_id, caption])

def load_posts():
    posts = []
    try:
        with open("posts.csv", "r", encoding="utf-8") as f:
            r = csv.reader(f, delimiter=";")
            next(r, None)
            for row in r:
                if len(row) >= 2:
                    posts.append({"file_id": row[0], "caption": row[1]})
    except FileNotFoundError:
        pass
    return posts

# ---------- СТАРТ ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_registered(user_id):
        return await show_main_menu(update, context)

    kb = [
        [InlineKeyboardButton("🔶 Пройти регистрацию", callback_data="register")],
        [InlineKeyboardButton("🎭 Афиша", callback_data="show_afisha")]
    ]
    welcome_text = (
        "👋 Привет! Добро пожаловать в чат-бот Big Daddy!* 🎉\n\n"
        "Новый филиал Big Daddy с дополнением армянской и грузинской кухни\n\n"
        "Разные блюда на каждый день\n\n"
        "Площадка для ваших мероприятий. 🚚 * действует доставка.\n\n"
        "⌚️Время работы:10:00 – 23:00\n\n"
        "📲+791435172718\n\n"
        "🌃г.Комсомольская, 23АА\n\n"
        "Пройдите простую регистрацию, чтобы бронировать столы, получать билеты и пользоваться другими функциями.\n\n"
        f"Регистрируясь, вы соглашаетесь с [политикой конфиденциальности]({PRIVACY_URL})."
    )
    if update.message:
        await update.message.reply_text(
            welcome_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb)
        )

# ---------- МЕНЮ ----------
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    kb_buttons = [
        [
            InlineKeyboardButton("🎪 Приложение", web_app=WebAppInfo(url="https://khvgvni.github.io/BadRabbitWebApp/")),
            InlineKeyboardButton("🍽 Бронь", callback_data="book_table")
        ],
        [
            InlineKeyboardButton("🎟 Пригласительный", callback_data="invite")
        ],
        [
            InlineKeyboardButton("👥 В команду", callback_data="join_team"),
            InlineKeyboardButton("🎭 Афиша", callback_data="show_afisha")
        ],
        [
            InlineKeyboardButton("💬 Чат", callback_data="open_chat"),
            InlineKeyboardButton("❓ FAQ", callback_data="show_faq")
        ]
    ]
    
    if user_id in ADMINS:
        kb_buttons.append([InlineKeyboardButton("⚙️ Админка", callback_data="admin_panel")])
    
    kb = InlineKeyboardMarkup(kb_buttons)

    text = "🍽️ *Кафе «Big Daddy»*\n\nВыберите действие:"
    if update.message:
        await update.message.reply_text(text, reply_markup=kb, parse_mode='Markdown')
    else:
        await update.callback_query.message.reply_text(text, reply_markup=kb, parse_mode='Markdown')

# ---------- ЧАТ С АДМИНОМ ----------
async def open_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("Написать в чат", show_alert=True)
    context.user_data["in_chat"] = True
    await q.message.reply_text(
        "Напишите сообщение — я передам его администраторам.",
        reply_markup=STOP_KB
    )

async def stop_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    context.user_data["in_chat"] = False
    await q.message.reply_text(
        "Чат завершён. Нажмите «Главное меню» → «💬 Чат», чтобы начать заново.",
        reply_markup=nav_keyboard()
    )

async def user_to_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("in_chat"):
        await show_main_menu(update, context)
        return

    user = update.effective_user
    msg = update.effective_message

    try:
        header_text = f"👤 *Сообщение от пользователя:*\n" \
                     f"🆔 ID: `{user.id}`\n" \
                     f"📛 Имя: {user.full_name}\n" \
                     f"💬 Сообщение:"
        
        header_msg = await context.bot.send_message(
            GROUP_CHAT_ID, 
            header_text,
            parse_mode="Markdown"
        )

        if msg.text:
            user_msg = await context.bot.send_message(
                GROUP_CHAT_ID,
                msg.text,
                reply_to_message_id=header_msg.message_id
            )
        else:
            user_msg = await msg.copy(
                chat_id=GROUP_CHAT_ID,
                reply_to_message_id=header_msg.message_id
            )

        ROUTE[header_msg.message_id] = user.id
        ROUTE[user_msg.message_id] = user.id

        await msg.reply_text(
            "✅ Ваше сообщение отправлено администраторам. Ожидайте ответа в этом чате.",
            reply_markup=STOP_KB
        )

    except Exception as e:
        logger.error(f"Ошибка отправки в группу: {e}")
        await msg.reply_text("❌ Ошибка отправки сообщения.")

async def support_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    chat = update.effective_chat
    
    if chat.id != GROUP_CHAT_ID or not msg.reply_to_message:
        return

    target_user_id = ROUTE.get(msg.reply_to_message.message_id)
    
    if not target_user_id:
        await msg.reply_text("❌ Не удалось найти пользователя для этого сообщения")
        return

    try:
        if msg.text:
            await context.bot.send_message(
                chat_id=target_user_id,
                text=f"💬 Ответ от администратора:\n\n{msg.text}"
            )
        elif msg.photo or msg.video or msg.document:
            await msg.copy(chat_id=target_user_id)
        else:
            await context.bot.send_message(
                chat_id=target_user_id,
                text="💬 Ответ от администратора (неподдерживаемый тип сообщения)"
            )
        
        await msg.reply_text("✅ Ответ отправлен пользователю")
        
    except Exception as e:
        logger.error(f"Ошибка отправки пользователю {target_user_id}: {e}")
        await msg.reply_text("❌ Не удалось отправить сообщение пользователю")

# ---------- РЕГИСТРАЦИЯ ----------
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("✍️ Введите ваше ФИО:")
    return REG_NAME

async def reg_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["reg_name"] = update.message.text
    await update.message.reply_text("📞 Введите ваш телефон:")
    return REG_PHONE

async def reg_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["reg_phone"] = update.message.text
    user_id = update.effective_user.id

    with open("users.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([context.user_data["reg_name"], context.user_data["reg_phone"], user_id, "Black"])

    msg = (
        f"🆕 Новый пользователь зарегистрировался!\n\n"
        f"👤 {context.user_data['reg_name']}\n"
        f"📞 {context.user_data['reg_phone']}\n"
        f"🆔 {user_id}\n"
    )
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=msg)

    await update.message.reply_text("✅ Регистрация завершена!")
    await show_main_menu(update, context)
    return ConversationHandler.END

# ---------- БРОНЬ ----------
async def book_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    user_data = get_user_data(update.effective_user.id)
    if not user_data:
        await q.message.reply_text("⚠️ Сначала пройдите регистрацию.", reply_markup=nav_keyboard())
        return ConversationHandler.END

    name, phone, _, status = user_data
    msg = (
        f"🍽 Новая бронь!\n\n"
        f"👤 {name}\n📞 {phone}\n⭐️ Статус: {status}\n🆔 {update.effective_user.id}"
    )
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=msg)
    await q.message.reply_text("✅ Ваша заявка отправлена администратору!", reply_markup=nav_keyboard())
    return ConversationHandler.END

# ---------- ПРИГЛАСИТЕЛЬНЫЙ ----------
async def send_invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("🎟 Ваш пригласительный!", reply_markup=nav_keyboard())

# ---------- КОМАНДА ----------
async def join_team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("✍️ Введите ваше ФИО:")
    return TEAM_NAME

async def team_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["team_name"] = update.message.text
    await update.message.reply_text("📞 Введите ваш телефон:")
    return TEAM_PHONE

async def team_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["team_phone"] = update.message.text
    await update.message.reply_text("💼 Укажите интересующую должность:")
    return TEAM_ROLE

async def team_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["team_role"] = update.message.text
    msg = (
        f"👥 Новая заявка в команду!\n\n"
        f"👤 {context.user_data['team_name']}\n"
        f"📞 {context.user_data['team_phone']}\n"
        f"💼 {context.user_data['team_role']}\n"
        f"🆔 {update.effective_user.id}"
    )
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=msg)
    await update.message.reply_text("✅ Ваша заявка отправлена!", reply_markup=nav_keyboard())
    return ConversationHandler.END

# ---------- FAQ ----------
async def show_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    faq_text = """
*Кафе "Big Daddy"* 

*Контактная информация:*

📍 *Адрес*
└─ г.Комсомольская, 23АА

📞 *Телефон*
└─ +7-914-351-727-18

🕒 *Часы работы*
└─ Ежедневно: 10:00 – 23:00

*Перед посещением обязательно ознакомьтесь с правилами:*
    """
    
    kb_buttons = [
        [InlineKeyboardButton("📜 Правила заведения", url="https://telegra.ph/Pravila-poseshcheniya-kluba-Cabinet-10-30")],
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="main_menu")]
    ]
    kb = InlineKeyboardMarkup(kb_buttons)
    
    await query.message.edit_text(faq_text, reply_markup=kb, parse_mode='Markdown')

# ---------- АФИША ----------
async def show_afisha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    posts = load_posts()
    if not posts:
        return await q.message.reply_text("🎭 Афиша пока не загружена.", reply_markup=nav_keyboard())
    for post in posts:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🍽 Забронировать стол", callback_data="book_table")]])
        await q.message.reply_photo(post["file_id"], caption=post["caption"], reply_markup=kb)

# ---------- АДМИН ПАНЕЛЬ ----------
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.callback_query.message.reply_text("⛔ Нет доступа")

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 Загрузить афишу", callback_data="upload_poster")],
        [InlineKeyboardButton("📝 Выложить пост", callback_data="upload_post")],
        [InlineKeyboardButton("📊 Выгрузить гостей", callback_data="export_guests")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ])
    await update.callback_query.message.reply_text("⚙️ Админ панель:\nВыберите действие:", reply_markup=kb)

async def upload_poster(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.callback_query.message.reply_text("⛔ Нет доступа")
    await update.callback_query.message.reply_text("📤 Отправь изображение для афиши:")
    context.user_data["upload_mode"] = "poster"
    context.user_data["poster_stage"] = "waiting_photo"

async def upload_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.callback_query.message.reply_text("⛔ Нет доступа")
    await update.callback_query.message.reply_text("📤 Отправь изображение для поста:")
    context.user_data["upload_mode"] = "post"
    context.user_data["post_stage"] = "waiting_photo"

async def handle_admin_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    mode = context.user_data.get("upload_mode")

    if mode == "poster":
        stage = context.user_data.get("poster_stage")
        if stage == "waiting_photo" and update.message.photo:
            file_id = update.message.photo[-1].file_id
            context.user_data["temp_poster"] = file_id
            context.user_data["poster_stage"] = "waiting_caption"
            await update.message.reply_text("✍️ Введи текст для афиши")
        elif stage == "waiting_caption" and update.message.text:
            save_post(context.user_data["temp_poster"], update.message.text)
            context.user_data["upload_mode"] = None
            context.user_data["poster_stage"] = None
            await update.message.reply_text("✅ Афиша сохранена!")

    elif mode == "post":
        stage = context.user_data.get("post_stage")
        if stage == "waiting_photo" and update.message.photo:
            file_id = update.message.photo[-1].file_id
            context.user_data["temp_post"] = file_id
            context.user_data["post_stage"] = "waiting_caption"
            await update.message.reply_text("✍️ Введи текст для поста")
        elif stage == "waiting_caption" and update.message.text:
            caption = update.message.text
            file_id = context.user_data["temp_post"]

            save_post(file_id, caption)

            users = []
            try:
                with open("users.csv", "r", encoding="utf-8") as f:
                    r = csv.reader(f, delimiter=";")
                    next(r, None)
                    for row in r:
                        if len(row) >= 3 and row[2].isdigit():
                            users.append(int(row[2]))
            except FileNotFoundError:
                pass

            sent, failed = 0, 0
            for uid in users:
                try:
                    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🍽 Забронировать стол", callback_data="book_table")]])
                    await context.bot.send_photo(chat_id=uid, photo=file_id, caption=caption, reply_markup=kb)
                    sent += 1
                except Exception as e:
                    failed += 1
                    logger.warning(f"Не удалось отправить пост {uid}: {e}")

            context.user_data["upload_mode"] = None
            context.user_data["post_stage"] = None
            await update.message.reply_text(f"✅ Пост опубликован! (OK: {sent}, ошибок: {failed})")

async def export_guests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.callback_query.message.reply_text("⛔ Нет доступа")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Guests"
    ws.append(["ФИО", "Телефон", "Telegram ID", "Статус"])

    try:
        with open("users.csv", "r", encoding="utf-8") as f:
            r = csv.reader(f, delimiter=";")
            next(r, None)
            for row in f:
                ws.append(row.strip().split(";"))
    except FileNotFoundError:
        return await update.callback_query.message.reply_text("⚠️ Список гостей пуст.")

    file_path = "guests.xlsx"
    wb.save(file_path)
    await update.callback_query.message.reply_document(open(file_path, "rb"))
    os.remove(file_path)

# ---------- MAIN ----------
def main():
    application = Application.builder().token(TOKEN).build()

    # Чат с админом
    application.add_handler(CallbackQueryHandler(open_chat, pattern="^open_chat$"))
    application.add_handler(CallbackQueryHandler(stop_chat, pattern="^stop_chat$"))
    application.add_handler(MessageHandler(
        filters.ChatType.PRIVATE & ~filters.COMMAND & filters.TEXT, 
        user_to_support
    ), group=1)
    
    application.add_handler(MessageHandler(
        filters.Chat(GROUP_CHAT_ID) & filters.REPLY & ~filters.COMMAND, 
        support_to_user
    ))
    
    # Регистрация
    reg_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(register, pattern="^register$")],
        states={
            REG_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_name)],
            REG_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_phone)],
        },
        fallbacks=[],
    )

    # Команда
    team_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(join_team, pattern="^join_team$")],
        states={
            TEAM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, team_name)],
            TEAM_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, team_phone)],
            TEAM_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, team_role)],
        },
        fallbacks=[],
    )
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(reg_conv)
    application.add_handler(team_conv)

    # Основные обработчики
    application.add_handler(CallbackQueryHandler(book_table, pattern="^book_table$"))
    application.add_handler(CallbackQueryHandler(send_invite, pattern="^invite$"))
    application.add_handler(CallbackQueryHandler(show_afisha, pattern="^show_afisha$"))
    application.add_handler(CallbackQueryHandler(show_faq, pattern="^show_faq$"))

    # Админ
    application.add_handler(CallbackQueryHandler(export_guests, pattern="^export_guests$"))
    application.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_panel$"))
    application.add_handler(CallbackQueryHandler(upload_poster, pattern="^upload_poster$"))
    application.add_handler(CallbackQueryHandler(upload_post, pattern="^upload_post$"))
    application.add_handler(MessageHandler(filters.PHOTO | filters.TEXT, handle_admin_messages))

    # Главное меню
    application.add_handler(CallbackQueryHandler(show_main_menu, pattern="^main_menu$"))

    application.run_polling()

if __name__ == "__main__":
    main()
