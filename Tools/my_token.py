import time
import string
import random

import requests
import json

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from .db import *

tokens_collection = db["tokens"]

# Global dictionary to manage tokens in memory
global_tokens = {}

duration = Vars.DURATION
dr = Vars.DURATION
def generate_random_alphanumeric():
    """Generate a random 8-letter alphanumeric string."""
    characters = string.ascii_letters + string.digits
    random_chars = ''.join(random.choice(characters) for _ in range(8))
    return random_chars


def get_short(url):
    try:
        api_url = Vars.SHORTENER_API
        url = api_url.replace("{}", url)
        rjson = requests.get(url).json()
        return rjson["shortenedUrl"]

    except requests.RequestException as e:
        print(f"Request failed: {e}")

    return url

# Generate a token (without saving to database)
def generate_token():
    return generate_random_alphanumeric()

# Save token with expiration time in the database
def save_token(user_id, token):
    duration = dr
    expiration_time = time.time() + (duration * 3600)  # Convert hours to seconds
    tokens_collection.update_one(
        {"_id": user_id},
        {"$set": {"token": token, "expires_at": expiration_time}},
        upsert=True
    )

def verify_token_memory(user_id, token):
    # Check in global_tokens
    if user_id in global_tokens:
        token_data = global_tokens[user_id]
        if token_data["expires_at"] > time.time():
            if token_data["token"] == token:
                return True
    return False

def verify_token(user_id):
    # Verify token using the token stored in the database
    token_data = tokens_collection.find_one({"_id": user_id})
    if token_data:
        expires_at = token_data["expires_at"]
        current_timestamp = time.time()  # Get the current time as a timestamp
        if current_timestamp < expires_at:
            return True
    return False

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def get_token(message, user_id):
    new_token = generate_token()
    expiration_time = time.time() + (dr * 3600)  # Token valid for 'dr' hours
    global_tokens[user_id] = {"token": new_token, "expires_at": expiration_time}

    token_link = f"https://telegram.me/{Bot.username}?start={new_token}"
    short_token_link = get_short(token_link)

    # Button layout: 1 | 2 and 3 | 4
    button1 = InlineKeyboardButton("Vᴇʀɪғʏ ʜᴇʀᴇ", url=short_token_link)
    button2 = InlineKeyboardButton("Tᴜᴛᴏʀɪᴀʟ", url="https://t.me/+KymUiadSyutiZjM1")
    button3 = InlineKeyboardButton("Pʀᴇᴍɪᴜᴍ", callback_data="premuim")
    button4 = InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close")

    keyboard = InlineKeyboardMarkup([
        [button1, button2],
        [button3, button4]
    ])

    photo = "https://i.ibb.co/PvpdSpV7/photo-2025-07-21-17-44-51-7529592614991953944.jpg"

    await message.reply_photo(
        photo=photo,
        caption=(
            "<b><blockquote>Yᴏᴜʀ ᴛᴏᴋᴇɴ ʜᴀs ᴇxᴘɪʀᴇᴅ. ᴘʟᴇᴀsᴇ ʀᴇғʀᴇsʜ ʏᴏᴜʀ ᴛᴏᴋᴇɴ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.</b></blockquote>\n"
            "<b><blockquote>Tᴏᴋᴇɴ ᴛɪᴍᴇᴏᴜᴛ : 1 ᴅᴀʏ</b></blockquote>\n\n"
            "<b><blockquote>Wʜᴀᴛ ɪs ᴛʜᴇ ᴛᴏᴋᴇɴ ?</b></blockquote>"
            "<b><blockquote>Tʜɪs ɪs ᴀɴ ᴀᴅs ᴛᴏᴋᴇɴ. ᴘᴀssɪɴɢ ᴏɴᴇ ᴀᴅ ᴀʟʟᴏᴡs ʏᴏᴜ ᴛᴏ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ ғᴏʀ 1 ᴅᴀʏ</b></blockquote>\n"
            "<b><blockquote><spoiler>Oᴡᴇʀᴇᴅ ʙʏ : @EmitingStars_Botz</spoiler></b></blockquote>"
        ),
        reply_markup=keyboard,
        message_effect_id=5104841245755180586  # Added as requested
    )

#f
