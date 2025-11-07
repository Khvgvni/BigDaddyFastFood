import logging
import csv
import os
from typing import Dict, Optional
from dotenv import load_dotenv
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo,
    ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, ContextTypes, filters
)

load_dotenv()

# === НАСТРОЙКИ И ОКРУЖЕНИЕ ===
TOKEN = os.getenv("BOT_TOKEN")  # задайте в .env
if not TOKEN:
    raise RuntimeError("Не задан BOT_TOKEN в .env")

GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID", "-1003228498870"))  # задайте реальный ID группы/канала
PRIVACY_URL = os.getenv("PRIVACY_URL", "https://example.com/privacy")
ADMINS = [int(x) for x in os.getenv("ADMINS", "150203692").split(",") if x.strip().isdigit()]

# Каталог для данных (по умолчанию – серверная директория)
DATA_DIR = os.getenv("DATA_DIR", "/srv/bigdaddycafebot/data")
os.makedirs(DATA_DIR, exist_ok=True)

# Путь к CSV с пользователями — ИМЕННО user.csv (в единственном числе)
USERS_CSV = os.path.join(DATA_DIR, "user.csv")
POSTS_CSV = os.path.join(DATA_DIR, "posts.csv")

# Маппинг: id сообщения в группе → id пользователя
ROUTE: Dict[int, int] = {}

# Клавиатура «завершить чат»
STOP_KB = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⛔ Завершить чат", callback_data="stop_chat")]]
)

# Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("bigdaddy-bot")

# Состояния
REG_NAME, REG_CONTACT, TEAM_NAME, TEAM_PHONE, TEAM_ROLE = range(5)

# ---------- УТИЛИТЫ ----------

def nav_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]])

def ensure_users_csv():
    """Создаёт файл user.csv с заголовком, если его нет."""
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["Имя", "Телефон", "UserID", "Статус"])

def get_user_data(user_id: int):
    try:
        with open(USERS_CSV, "r", encoding="utf-8") as f:
            r = csv.reader(f, delimiter=";")
            next(r, None)  # пропускаем заголовок
            for row in r:
                # Поддерживаем и 3 поля (Имя;Телефон;UserID), и 4 (…;Статус)
                if len(row) >= 3 and row[2] == str(user_id):
                    name = row[0]
                    phone = row[1]
                    status = row[3] if len(row) >= 4 else None
                    return {"name": name, "phone": phone, "user_id": int(row[2]), "status": status}
    except FileNotFoundError:
        return None
    return None

def is_registered(user_id: int) -> bool:
    return get_user_data(user_id) is not None

def append_user_row(name: str, phone: str, user_id: int) -> bool:
    """
    Идемпотентная запись пользователя:
    - создаёт USERS_CSV с заголовком при необходимости
    - не добавляет дубль, если user_id уже есть
    Возвращает True, если добавили новую запись; False, если пользователь уже был.
    """
    ensure_users_csv()
    if is_registered(user_id):
        return False
    try:
        with open(USERS_CSV, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow([name, phone, user_id, "Black"])
        return True
    except Exception as e:
        logger.exception(f"Ошибка записи {USERS_CSV}: {e}")
        return False

def save_post(file_id: str, caption: str):
    new_file = not os.path.exists(POSTS_CSV)
    with open(POSTS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        if new_file:
            writer.writerow(["file_id", "caption"])
        writer.writerow([file_id, caption])

def load_posts():
    posts = []
    try:
        with open(POSTS_CSV, "r", encoding="utf-8") as f:
            r = csv.reader(f, delimiter=";")
            next(r, None)
            for row in r:
                if len(row) >= 2:
                    posts.append({"file_id": row[0], "caption": row[1]})
    except FileNotFoundError:
        pass
    return posts

# ---------- СТАРТ / МЕНЮ ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_registered(user_id):
        return await show_main_menu(update, context)

    kb = [
        [InlineKeyboardButton("🔶 Пройти регистрацию", callback_data="register")],
        [InlineKeyboardButton("🎭 Афиша", callback_data="show_afisha")]
    ]
    welcome_text = (
        "👋 Привет! Добро пожаловать в чат-бот Big Daddy! 🎉\n\n"
        "Новый филиал Big Daddy с дополнением армянской и грузинской кухни.\n"
        "Площадка для мероприятий. 🚚 Есть доставка.\n\n"
        "⌚️ Время работы: 10:00 – 23:00\n"
        "📲 +7 914 351-72-78\n"
        "🌃 ул. Комсомольская, 23А\n\n"
        "Пройдите простую регистрацию, чтобы бронировать столы, получать билеты и пользоваться другими функциями."
    )
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(kb))
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=InlineKeyboardMarkup(kb))

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    kb_buttons = [
        [
            InlineKeyboardButton("📔 Меню", web_app=WebAppInfo(url="https://app.bigdaddycafe.ru/")),
            InlineKeyboardButton("🍽 Бронь", callback_data="book_table")
        ],
        [
            InlineKeyboardButton("👥 В команду", callback_data="join_team"),
            InlineKeyboardButton("🎭 Афиша", callback_data="show_afisha")
        ],
        [
            InlineKeyboardButton("💬 Чат", callback_data="open_chat"),
            InlineKeyboardButton("❓ О нас", callback_data="show_faq")
        ]
    ]
    if user_id in ADMINS:
        kb_buttons.append([InlineKeyboardButton("⚙️ Админка", callback_data="admin_panel")])

    kb = InlineKeyboardMarkup(kb_buttons)
    text = "🍽️ Кафе «Big Daddy»\n\nВыберите действие:"

    if update.message:
        await update.message.reply_text(text, reply_markup=kb)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=kb)

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
    # Вмешиваемся ТОЛЬКО если пользователь явно в режиме чата с админом
    if not context.user_data.get("in_chat"):
        return

    user = update.effective_user
    msg = update.effective_message
    try:
        header_text = (
            "👤 Сообщение от пользователя:\n"
            f"🆔 ID: {user.id}\n"
            f"📛 Имя: {user.full_name}\n"
            "💬 Сообщение:"
        )
        header_msg = await context.bot.send_message(GROUP_CHAT_ID, header_text)
        if msg.text:
            user_msg = await context.bot.send_message(
                GROUP_CHAT_ID, msg.text, reply_to_message_id=header_msg.message_id
            )
        else:
            user_msg = await msg.copy(chat_id=GROUP_CHAT_ID, reply_to_message_id=header_msg.message_id)

        ROUTE[header_msg.message_id] = user.id
        ROUTE[user_msg.message_id] = user.id

        await msg.reply_text("✅ Ваше сообщение отправлено администраторам. Ожидайте ответа.", reply_markup=STOP_KB)
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
            await context.bot.send_message(chat_id=target_user_id, text=f"💬 Ответ от администратора:\n\n{msg.text}")
        elif msg.photo or msg.video or msg.document:
            await msg.copy(chat_id=target_user_id)
        else:
            await context.bot.send_message(chat_id=target_user_id, text="💬 Ответ от администратора (неподдерживаемый тип)")
        await msg.reply_text("✅ Ответ отправлен пользователю")
    except Exception as e:
        logger.error(f"Ошибка отправки пользователю {target_user_id}: {e}")
        await msg.reply_text("❌ Не удалось отправить сообщение пользователю")

# ---------- РЕГИСТРАЦИЯ ----------

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✍️ Введите ваше ФИО:")
    return REG_NAME

async def reg_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["reg_name"] = update.message.text.strip()
    kb = ReplyKeyboardMarkup(
        [[KeyboardButton(text="📱 Поделиться контактом", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True, selective=True
    )
    await update.message.reply_text(
        "📞 Нажмите кнопку ниже, чтобы отправить свой номер.",
        reply_markup=kb
    )
    return REG_CONTACT

async def reg_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if not contact or contact.user_id != update.effective_user.id:
        kb = ReplyKeyboardMarkup(
            [[KeyboardButton(text="📱 Поделиться контактом", request_contact=True)]],
            resize_keyboard=True, one_time_keyboard=True, selective=True
        )
        await update.message.reply_text(
            "Пожалуйста, поделитесь *собственным* номером через кнопку на клавиатуре.",
            reply_markup=kb,
            parse_mode="Markdown"
        )
        return REG_CONTACT

    name = context.user_data.get("reg_name", "").strip()
    phone = contact.phone_number
    user_id = update.effective_user.id

    created = append_user_row(name=name, phone=phone, user_id=user_id)
    if not created:  # уже был
        await update.message.reply_text("✅ Вы уже были зарегистрированы.", reply_markup=ReplyKeyboardRemove())
    else:
        await update.message.reply_text("✅ Регистрация завершена!", reply_markup=ReplyKeyboardRemove())

    # уведомление админам
    msg = (
        f"🆕 Пользователь зарегистрировался!\n\n"
        f"👤 {name}\n"
        f"📞 {phone}\n"
        f"🆔 {user_id}\n"
    )
    try:
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=msg)
    except Exception as e:
        logger.warning(f"Не смог отправить уведомление админам: {e}")

    await show_main_menu(update, context)
    context.user_data.clear()
    return ConversationHandler.END

# ---------- БРОНЬ / ПРИГЛАСИТЕЛЬНЫЙ / КОМАНДА / FAQ / АФИША ----------

async def book_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    ud = get_user_data(update.effective_user.id)
    if not ud:
        await q.message.reply_text("⚠️ Сначала пройдите регистрацию.", reply_markup=nav_keyboard())
        return

    # Формируем сообщение без обязательного статуса
    msg_lines = [
        "🍽 Новая бронь!",
        "",
        f"👤 {ud['name']}",
        f"📞 {ud['phone']}",
        f"🆔 {ud['user_id']}",
    ]

    try:
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text="\n".join(msg_lines))
    except Exception as e:
        logger.warning(f"Не удалось отправить бронь админам: {e}")

    await q.message.reply_text("✅ Ваша заявка отправлена администратору!", reply_markup=nav_keyboard())

async def send_invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("🎟 Ваш пригласительный!", reply_markup=nav_keyboard())

async def join_team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("✍️ Введите ваше ФИО:")
    return TEAM_NAME

async def team_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["team_name"] = update.message.text.strip()
    await update.message.reply_text("📞 Введите ваш телефон:")
    return TEAM_PHONE

async def team_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["team_phone"] = update.message.text.strip()
    await update.message.reply_text("💼 Укажите интересующую должность:")
    return TEAM_ROLE

async def team_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["team_role"] = update.message.text.strip()
    msg = (
        f"👥 Новая заявка в команду!\n\n"
        f"👤 {context.user_data['team_name']}\n"
        f"📞 {context.user_data['team_phone']}\n"
        f"💼 {context.user_data['team_role']}\n"
        f"🆔 {update.effective_user.id}"
    )
    try:
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=msg)
    except Exception as e:
        logger.warning(f"Не удалось отправить заявку в команду: {e}")
    await update.message.reply_text("✅ Ваша заявка отправлена!", reply_markup=nav_keyboard())
    context.user_data.clear()
    return ConversationHandler.END

async def show_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    faq_text = (
        "Кафе \"Big Daddy\"\n\n"
        "Контактная информация:\n\n"
        "📍 Адрес\nул. Комсомольская, 23А\n\n"
        "📞 Телефон\n+7-914-351-72-71\n\n"
        "🕒 Часы работы\nЕжедневно: 10:00 – 23:00\n\n"
        "Перед посещением и доставкой обязательно ознакомьтесь с правилами:"
    )
    kb_buttons = [
        [InlineKeyboardButton("📜 Правила заведения", url="https://telegra.ph/Tut-skoro-budut-pravila-dostavki-11-010")],
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="main_menu")]
    ]
    await query.message.edit_text(faq_text, reply_markup=InlineKeyboardMarkup(kb_buttons))

async def show_afisha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    posts = load_posts()
    if not posts:
        return await q.message.reply_text("🎭 Афиша пока не загружена.", reply_markup=nav_keyboard())
    for post in posts:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🍽 Забронировать стол", callback_data="book_table")]])
        await q.message.reply_photo(post["file_id"], caption=post["caption"], reply_markup=kb)

# ---------- АДМИН ----------

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
    # Личный чат админа, чтобы не мешать пользователям
    if update.effective_user.id not in ADMINS or update.effective_chat.type != "private":
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

            # Рассылка
            users = []
            try:
                with open(USERS_CSV, "r", encoding="utf-8") as f:
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
    try:
        await update.callback_query.message.reply_document(
            document=open(USERS_CSV, "rb"),
            filename="guests.csv",
            caption="📊 Список гостей"
        )
    except FileNotFoundError:
        await update.callback_query.message.reply_text("⚠️ Список гостей пуст.")

# ---------- MAIN ----------

def main():
    # на всякий случай — гарантируем наличие файла с заголовком
    ensure_users_csv()

    application = Application.builder().token(TOKEN).build()

    # Чат с админом
    application.add_handler(CallbackQueryHandler(open_chat, pattern="^open_chat$"))
    application.add_handler(CallbackQueryHandler(stop_chat, pattern="^stop_chat$"))
    application.add_handler(
        MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND & filters.TEXT, user_to_support),
        group=2,  # после разговоров; не перебивает регистрацию
    )

    # Ответы админов из группы пользователям
    application.add_handler(
        MessageHandler(filters.Chat(GROUP_CHAT_ID) & filters.REPLY & ~filters.COMMAND, support_to_user)
    )

    # РЕГИСТРАЦИЯ
    reg_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(register, pattern="^register$")],
        states={
            REG_NAME:    [MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, reg_name)],
            REG_CONTACT: [MessageHandler(filters.ChatType.PRIVATE & filters.CONTACT, reg_contact)],
        },
        fallbacks=[],
    )

    # В КОМАНДУ
    team_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(join_team, pattern="^join_team$")],
        states={
            TEAM_NAME: [MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, team_name)],
            TEAM_PHONE: [MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, team_phone)],
            TEAM_ROLE: [MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, team_role)],
        },
        fallbacks=[],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(reg_conv, group=0)
    application.add_handler(team_conv, group=0)

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
    application.add_handler(
        MessageHandler(
            filters.ChatType.PRIVATE & (filters.PHOTO | filters.TEXT) & ~filters.COMMAND,
            handle_admin_messages
        ),
        group=3,  # ещё позже
    )

    # Главное меню
    application.add_handler(CallbackQueryHandler(show_main_menu, pattern="^main_menu$"))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()