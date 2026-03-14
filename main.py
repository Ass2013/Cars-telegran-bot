import telebot 
import sqlite3 
from config import TOKEN
from logic import DATABASE, DatabaseManager

bot = telebot.TeleBot(TOKEN)

db = DatabaseManager(DATABASE)


@bot.message_handler(commands=['start'])
def start(message):
    # Save user in the database
    conn = db.database  # db.database is the path to the DB
    with sqlite3.connect(conn) as conn:
        cursor = conn.cursor()
        # Insert user if not exists (avoid duplicates)
        cursor.execute("""
            INSERT OR IGNORE INTO users (user_name)
            VALUES (?)
        """, (message.from_user.username,))
        conn.commit()

    # Send welcome message
    text = (
        "Hello! I'm a bot where you can save your favourite car brand and engine.\n\n"
        "Commands:\n"
        "/brand - save your favourite car brand\n"
        "/engine - save your favourite engine or electric motor\n"
        "/show - enter your username and see your saved brand + engine"
    )

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['brand'])
def brand_name(message):
    text = "What is your favourite brand?"
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, save_brand)  # Wait for user's reply

def save_brand(message):
    brand = message.text
    conn = db.database
    with sqlite3.connect(conn) as conn:
        cursor = conn.cursor()
        # Update the brand for this user
        cursor.execute("""
            UPDATE users
            SET brand_id = (SELECT brand_id FROM brands WHERE brand_name = ?)
            WHERE user_name = ?
        """, (brand, message.from_user.username))
        conn.commit()

    bot.send_message(message.chat.id, f"Your favourite brand '{brand}' has been saved!")


@bot.message_handler(commands=['engine'])
def engine_name(message):
    text = "What is your favourite engine?"
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, save_engine)  # Wait for user's reply


def save_engine(message):
    engine = message.text  # store user reply
    conn = db.database
    with sqlite3.connect(conn) as conn:
        cursor = conn.cursor()
        # Update the engine_id for this user
        cursor.execute("""
            UPDATE users
            SET engine_id = (SELECT engine_id FROM engine WHERE engine_name = ?)
            WHERE user_name = ?
        """, (engine, message.from_user.username))
        conn.commit()

    bot.send_message(message.chat.id, f"Your favourite engine '{engine}' has been saved!")


@bot.message_handler(commands=['show'])
def show_user(message):
    username = message.from_user.username  # get Telegram username
    conn = db.database
    with sqlite3.connect(conn) as conn:
        cursor = conn.cursor()
        # Get brand and engine names for this user
        cursor.execute("""
            SELECT b.brand_name, e.engine_name
            FROM users u
            LEFT JOIN brands b ON u.brand_id = b.brand_id
            LEFT JOIN engine e ON u.engine_id = e.engine_id
            WHERE u.user_name = ?
        """, (username,))
        result = cursor.fetchone()

    if result:
        brand, engine = result
        bot.send_message(
            message.chat.id,
            f"Your saved car:\nBrand: {brand}\nEngine: {engine}"
        )
    else:
        bot.send_message(
            message.chat.id,
            "You haven’t selected a brand or engine yet!"
        )


print("Bot started...")
bot.infinity_polling()