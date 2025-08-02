from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait

from .storage import web_data, split_list, plugins_list, users_txt, retry_on_flood, queue, asyncio

from pyrogram.errors import FloodWait
import pyrogram.errors

from bot import Bot, Vars, logger

import random
from Tools.db import *
from Tools.my_token import *

from pyrogram.handlers import MessageHandler
import time

from asyncio import create_subprocess_exec
from os import execl
from sys import executable

import shutil, psutil, time, os, platform
import asyncio

HELP_MSG = """<blockquote><b>›› Tᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴀ ᴍᴀɴɢᴀ ᴊᴜsᴛ ᴛʏᴘᴇ ᴛʜᴇ ɴᴀᴍᴇ ᴏғ ᴛʜᴇ ᴍᴀɴɢᴀ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴋᴇᴇᴘ ᴜᴘ ᴛᴏ ᴅᴀᴛᴇ.</blockquote>
<pre>𝗙𝗢𝗥 𝗘𝗫𝗔𝗠𝗣𝗟𝗘</pre>
<blockquote>Hell's Paradise</blockquote>
<blockquote expandable><i>ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴡᴇʙsɪᴛᴇ ᴡʜᴇʀᴇ ʏᴏᴜ ᴄᴏᴜʟᴅ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ᴍᴀɴɢᴀ. ʜᴇʀᴇ ʏᴏᴜ ᴡɪʟʟ ʜᴀᴠᴇ ᴛʜᴇ ᴏᴘᴛɪᴏɴ ᴛᴏ sᴜʙsᴄʀɪʙᴇ, ᴏʀ ᴛᴏ ᴄʜᴏᴏsᴇ ᴀ ᴄʜᴀᴘᴛᴇʀ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ. ᴛʜᴇ ᴄʜᴀᴘᴛᴇʀs ᴀʀᴇ sᴏʀᴛᴇᴅ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴛʜᴇ ᴡᴇʙsɪᴛᴇ.</i></blockquote>
<blockquote><b><a href='https://t.me/EmitingStars_Botz'>‣ Uᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ : Eᴍɪᴛɪɴɢ Sᴛᴀʀs</a></b></blockquote>"""

from pyrogram import Client
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import asyncio
import time

from pyrogram.enums import ChatAction
import random

stickers = [
    "CAACAgUAAxkBAAEOXBhoCoKZ76jevKX-Vc5v5SZhCeQAAXMAAh4KAALJrhlVZygbxFWWTLw2BA"
]

welcome_text = (
    "<i><blockquote>Wᴇʟᴄᴏᴍᴇ, ʙᴀʙʏ… ɪ’ᴠᴇ ʙᴇᴇɴ ᴄʀᴀᴠɪɴɢ ʏᴏᴜʀ ᴘʀᴇsᴇɴᴄᴇ — "
    "ғᴇᴇʟs ᴘᴇʀғᴇᴄᴛ ɴᴏᴡ ᴛʜᴀᴛ ʏᴏᴜ’ʀᴇ ʜᴇʀᴇ.</blockquote></i>"
)

@Bot.on_message(filters.command("start"))
async def start(client, message):
    if Vars.IS_PRIVATE:
        if message.chat.id not in Vars.ADMINS:
            return await message.reply("<code>You cannot use me baby </code>")

    # Send typing action and welcome message
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    msg = await message.reply_text(welcome_text)
    await asyncio.sleep(0.1)

    # Show startup animation
    await msg.edit_text("<b><i><pre>Sᴛᴀʀᴛɪɴɢ...</pre></i></b>")
    await asyncio.sleep(0.1)
    await msg.delete()

    # Send sticker
    await client.send_chat_action(message.chat.id, ChatAction.CHOOSE_STICKER)
    await message.reply_sticker(random.choice(stickers))

    if len(message.command) > 1:
        if message.command[1] != "start":
            user_id = message.from_user.id
            token = message.command[1]
            if verify_token_memory(user_id, token):
                sts = await message.reply("Token verified! You can now use the bot.")
                save_token(user_id, token)
                global_tokens.pop(user_id, None)
                await asyncio.sleep(8)
                await sts.delete()
            else:
                sts = await message.reply("Invalid or expired token. Requesting a new one...")
                await get_token(message, user_id)
                await sts.delete()
            return

    # Static image URL (replace with your preferred one)
    photo = "https://i.ibb.co/PvpdSpV7/photo-2025-07-21-17-44-51-7529592614991953944.jpg"

    ping = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Vars.PING))
    await message.reply_photo(
        photo,
        caption=(
            "<pre>Hᴇʏᴏ ᴄᴜᴛɪᴇ</pre>\n"
            "<b><blockquote>I'ᴍ ʏᴏᴜʀ ᴍᴀɴɢᴀ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ. Jᴜsᴛ sᴇɴᴅ ᴍᴇ ᴀ ᴛɪᴛʟᴇ, ᴀɴᴅ ɪ’ʟʟ ғɪɴᴅ ɪᴛ ғᴏʀ ʏᴏᴜ ɪɴ ᴄʟᴇᴀʀ, ʜɪɢʜ-Qᴜᴀʟɪᴛʏ ғᴏʀᴍᴀᴛ.</b></blockquote>\n"
            f"<blockquote><b><a href='https://t.me/EmitingStars_Botz'>‣ Mᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : Eᴍɪᴛɪɴɢ Sᴛᴀʀs</a></b></blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Mᴀɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz"),
                InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl")
            ],
            [
                InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url="http://t.me/RexySama")
            ]
        ])
    )



from pyrogram.errors import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, ContinuePropagation, StopPropagation

@Bot.on_message(filters.private)
async def on_private_message(client: Client, message: Message):
    if client.SHORTENER:
        if not await premium_user(message.from_user.id):
            if not verify_token(message.from_user.id):
                if message.from_user.id not in client.ADMINS:
                    return await get_token(message, message.from_user.id)

    try:
        user_id = message.from_user.id

        if AUTH_CHANNELS:
            not_joined = []
            for channel in AUTH_CHANNELS:
                try:
                    await client.get_chat_member(channel, user_id)
                except UserNotParticipant:
                    try:
                        chat = await client.get_chat(channel)
                        invite_link = chat.invite_link or await client.export_chat_invite_link(channel)
                        not_joined.append((chat.title, invite_link))
                    except Exception:
                        continue
                except (UsernameNotOccupied, ChatAdminRequired):
                    continue

            if not_joined:
                bot_info = await client.get_me()
                buttons = []

                for i in range(0, len(not_joined), 2):
                    row = []
                    for j in range(2):
                        if i + j < len(not_joined):
                            title, link = not_joined[i + j]
                            row.append(InlineKeyboardButton(f"{i + j + 1}. {title}", url=link))
                    buttons.append(row)

                buttons.append([
                    InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{bot_info.username}?start=start")
                ])

                await message.reply(
                    f"**🎭 {message.from_user.mention}, please join the required channel(s) to use this bot.**",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return

    except ContinuePropagation:
        raise
    except StopPropagation:
        raise
    except Exception as e:
        await message.reply(f"⚠️ Error occurred:\n`{e}`")
        return message.continue_propagation()

    # All checks passed, continue
    return message.continue_propagation()

@Bot.on_message(filters.command(["add", "add_premium"]) & filters.user(Bot.ADMINS))
async def add_handler(_, msg):
  sts = await msg.reply_text("<pre>Pʀᴏᴄᴇssɪɴɢ...</pre>")
  try:
    user_id = int(msg.text.split(" ")[1])
    time_limit_days = int(msg.text.split(" ")[2])
    await add_premium(user_id, time_limit_days)
    await retry_on_flood(sts.edit)("<pre>Usᴇʀ ᴀᴅᴅᴇᴅ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ sᴜᴄᴄᴇssғᴜʟʟʏ</pre>")
  except Exception as err:
    await retry_on_flood(sts.edit)(err)

@Bot.on_message(filters.command(["del", "del_premium"]) & filters.user(Bot.ADMINS))
async def del_handler(_, msg):
  sts = await msg.reply_text("<pre>Pʀᴏᴄᴇssɪɴɢ...</pre>")
  try:
    user_id = int(msg.text.split(" ")[1])
    await remove_premium(user_id)
    await retry_on_flood(sts.edit)("<pre>Usᴇʀ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴘʀᴇᴍɪᴜᴍ sᴜᴄᴄᴇssғᴜʟʟʏ.</pre>")
  except Exception as err:
    await retry_on_flood(sts.edit)(err)

@Bot.on_message(filters.command(["del_expired", "del_expired_premium"]) & filters.user(Bot.ADMINS))
async def del_expired_handler(_, msg):
  sts = await msg.reply_text("<pre>Pʀᴏᴄᴇssɪɴɢ...</pre>")
  try:
    await remove_expired_users()
    await retry_on_flood(sts.edit)("<pre>Exᴘɪʀᴇᴅ ᴜsᴇʀs ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.</pre>")
  except Exception as err:
    await retry_on_flood(sts.edit)(err)

@Bot.on_message(filters.command(["premium", "premium_users"]) & filters.user(Bot.ADMINS))
async def premium_handler(_, msg):
  sts = await msg.reply_text("<pre>Pʀᴏᴄᴇssɪɴɢ...</pre>")
  try:
    premium_users = acollection.find()
    txt = "<pre>◈ Pʀᴇᴍɪᴜᴍ ᴜsᴇʀs :-</pre>\n────────────────────────────\n"
    for user in premium_users:
      user_ids = user["user_id"]
      user_info = await _.get_users(user_ids)
      username = user_info.username
      first_name = user_info.first_name
      expiration_timestamp = user["expiration_timestamp"]
      xt = (expiration_timestamp-(time.time()))
      x = round(xt/(24*60*60))
      txt += f"<b><blockquote>›› Usᴇʀ ɪᴅ: <code>{user_ids}</code>\n›› Usᴇʀɴᴀᴍᴇ : @{username}\n›› Nᴀᴍᴇ : <code>{first_name}</code>\n›› Exᴘɪʀᴀᴛɪᴏɴ ᴛɪᴍᴇsᴛᴀᴍᴘ: {x} ᴅᴀʏs</b></blockquote>\n────────────────────────"

    await retry_on_flood(sts.edit)(txt[:1024])
  except Exception as err:
    await retry_on_flood(sts.edit)(err)


@Bot.on_message(filters.command(["broadcast", "b"]) & filters.user(Bot.ADMINS))
async def b_handler(_, msg):
  return await borad_cast_(_, msg)

@Bot.on_message(filters.command(["pbroadcast", "pb"]) & filters.user(Bot.ADMINS))
async def pb_handler(_, msg):
  return await borad_cast_(_, msg, True)

async def borad_cast_(_, message, pin=None):
  def del_users(user_id):
    try:
      user_id = str(user_id)
      del uts[user_id]
      sync(_.DB_NAME, 'uts')
    except:
      pass
    
  sts = await message.reply_text("<pre>Pʀᴏᴄᴇssɪɴɢ...</pre>")
  if message.reply_to_message:
    user_ids = get_users()
    msg = message.reply_to_message
    total = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0
    await retry_on_flood(sts.edit)("<pre>Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ...</pre>")
    for user_id in user_ids:
      try:
        docs = await msg.copy(int(user_id))
        if pin:
          await docs.pin(both_sides=True)
        
        successful += 1
      except FloodWait as e:
        await asyncio.sleep(e.value)
        
        docs = await msg.copy(int(user_id))
        if pin:
          await docs.pin(both_sides=True)
        
        successful += 1
      except pyrogram.errors.UserIsBlocked:
        del_users(user_id)
        blocked += 1
      except pyrogram.errors.PeerIdInvalid:
        del_users(user_id)
        unsuccessful += 1
      except pyrogram.errors.InputUserDeactivated:
        del_users(user_id)
        deleted += 1
      except pyrogram.errors.UserNotParticipant:
        del_users(user_id)
        blocked += 1
      except:
        unsuccessful += 1
    
    status = f"""<b><u>Broadcast Completed</u>

    Total Users: <code>{total}</code>
    Successful: <code>{successful}</code>
    Blocked Users: <code>{blocked}</code>
    Deleted Accounts: <code>{deleted}</code>
    Unsuccessful: <code>{unsuccessful}</code></b>"""
    
    await retry_on_flood(sts.edit)(status)
  else:
    await retry_on_flood(sts.edit)("<blockquote>Rᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ɪᴛ.</blockquote>")
          

    
@Bot.on_message(filters.command("restart") & filters.user(Bot.ADMINS))
async def restart_(client, message):
  msg = await message.reply_text("<pre>Rᴇsᴛᴀʀᴛɪɴɢ.....</pre>", quote=True)
  with open("restart_msg.txt", "w") as file:
    file.write(str(msg.chat.id) + ":" + str(msg.id))
    file.close()
  
  await (await create_subprocess_exec("python3", "update.py")).wait()
  execl(executable, executable, "-B", "main.py")

def humanbytes(size):    
  if not size:
      return ""
  units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
  size = float(size)
  i = 0
  while size >= 1024.0 and i < len(units):
      i += 1
      size /= 1024.0
  return "%.2f %s" % (size, units[i])

def GET_PROVIDER():
  provider = "Unknown"
  try:
      if os.path.exists('/sys/hypervisor/uuid'):
          with open('/sys/hypervisor/uuid', 'r') as f:
              uuid = f.read().lower()
              if uuid.startswith('ec2'): provider = "AWS EC2"
              elif 'azure' in uuid: provider = "Microsoft Azure"

      elif os.path.exists('/etc/google-cloud-environment'):
          provider = "Google Cloud"

      elif os.path.exists('/etc/digitalocean'):
          provider = "DigitalOcean"

      elif os.path.exists('/dev/disk/by-id/scsi-0Linode'):
          provider = "Linode"

      elif os.path.exists('/etc/vultr'):
          provider = "Vultr"

  except Exception:
      pass
  
  return provider
  
@Bot.on_message(filters.command('stats'))
async def show_ping(_, message):
  total, used, free = shutil.disk_usage(".")
  total = humanbytes(total)
  used = humanbytes(used)
  free = humanbytes(free)
  net_start = psutil.net_io_counters()

  time.sleep(2)
  net_end = psutil.net_io_counters()

  bytes_sent = net_end.bytes_sent - net_start.bytes_sent
  bytes_recv = net_end.bytes_recv - net_start.bytes_recv
  #pkts_sent = net_end.packets_sent - net_start.packets_sent
  #pkts_recv = net_end.packets_recv - net_start.packets_recv
  
  cpu_cores = os.cpu_count()
  cpu_usage = psutil.cpu_percent()
  ram_usage = psutil.virtual_memory().percent
  disk_usage = psutil.disk_usage('/').percent
  try: uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - _.PING))
  except: uptime = None

  start_t = time.time()
  st = await message.reply('**Aᴄᴄᴇꜱꜱɪɴɢ Tʜᴇ Dᴇᴛᴀɪʟꜱ.....**')    
  end_t = time.time()
  time_taken_s = (end_t - start_t) * 1000 
  
  await message.reply_text(
    text=("<pre>◈ Bᴏᴛ ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs</pre>\n────────────────────────────\n"
          f"<b><blockquote>›› Tᴏᴛᴀʟ ᴅɪsᴋ sᴘᴀᴄᴇ : {total} \n"
          f"›› Usᴇᴅ sᴘᴀᴄᴇ: {used}({disk_usage}%) \n"
          f"›› Fʀᴇᴇ sᴘᴀᴄᴇ : {free} \n"
          f"›› Cᴘᴜ ᴄᴏʀᴇs : {cpu_cores} \n"
          f"›› Cᴘᴜ ᴜsᴀɢᴇ : {cpu_usage}% \n"
          f"›› Rᴀᴍ ᴜsᴀɢᴇ : {ram_usage}%\n"
          f"›› Uᴘᴛɪᴍᴇ : {uptime}\n"
          f"›› Cʟᴏᴜᴅ ᴘʀᴏᴠɪᴅᴇʀ : {GET_PROVIDER()}\n"
          f"›› Os : {platform.system()} \n"
          f"›› Os ᴠᴇʀsɪᴏɴ : {platform.release()} \n"
          f"›› Pʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ : {platform.python_version()} \n"
          f"›› Pʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ : {_.__version__} \n"
          f"›› Tᴏᴛᴀʟ ɪ/ᴏ ᴅᴀᴛᴀ : {humanbytes(net_end.bytes_sent + net_end.bytes_recv)} \n"
          f"›› Uᴘʟᴏᴀᴅ ʀᴀᴛᴇ : {humanbytes(bytes_sent/2)}/s \n"
          f"›› Dᴏᴡɴʟᴏᴀᴅ ʀᴀᴛᴇ : {humanbytes(bytes_recv/2)}/s \n"
          f"›› Cᴜʀʀᴇɴᴛ ᴘɪɴɢ : {time_taken_s:.3f} ᴍꜱ\n"
          f"›› Qᴜᴇᴜᴇ : {queue.qsize()}</i></b>\n</b></blockquote>\n────────────────────────────"),
    quote=True
    )
  await st.delete()


@Bot.on_message(filters.command("shell") & filters.user(Bot.ADMINS))
async def shell(_, message):
  cmd = message.text.split(maxsplit=1)
  if len(cmd) == 1:
    return await message.reply("<code>No command to execute was given.</code>")

  cmd = cmd[1]
  proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await proc.communicate()
  stdout = stdout.decode().strip()
  stderr = stderr.decode().strip()
  reply = ""
  if len(stdout) != 0:
    reply += f"<b>Stdout</b>\n<blockquote>{stdout}</blockquote>\n"
  if len(stderr) != 0:
    reply += f"<b>Stderr</b>\n<blockquote>{stderr}</blockquote>"

  if len(reply) > 3000:
    file_name = "shell_output.txt"
    with open(file_name) as out_file:
      await message.reply_document(out_file)
      out_file.close()
    os.remove(file_name)
  elif len(reply) != 0:
    await message.reply(reply)
  else:
    await message.reply("No Reply")
  
@Bot.on_message(filters.command("export") & filters.user(Bot.ADMINS))
async def export_(_, message):
  cmd = message.text.split(maxsplit=1)
  if len(cmd) == 1:
    return await message.reply("<pre>Fɪʟᴇ ɴᴀᴍᴇ ɴᴏᴛ ɢɪᴠᴇɴ.</pre>")
  
  sts = await message.reply("<pre>Fɪʟᴇ ɴᴀᴍᴇ ɴᴏᴛ ɢɪᴠᴇɴ.</pre>")
  try:
    file_name = cmd[1]
    if "*2" in file_name:
      file_name = file_name.replace("*2", "")
      file_name = f"__{file_name}__"
    
    if os.path.exists(file_name):
      await message.reply_document(file_name)
    else:
      await sts.edit("<pre>Fɪʟᴇ ɴᴏᴛ ғᴏᴜɴᴅ</pre>")
  except Exception as err:
    await sts.edit(err)
  

@Bot.on_message(filters.command("import") & filters.user(Bot.ADMINS))
async def import_(_, message):
  cmd = message.text.split(maxsplit=1)
  if len(cmd) == 1:
    return await message.reply("<pre>Fɪʟᴇ ɴᴀᴍᴇ ɴᴏᴛ ɢɪᴠᴇɴ.</pre>")

  sts = await message.reply("<pre>Pʀᴏᴄᴇssɪɴɢ...</pre>")
  try:
    file_name = cmd[1]
    if "*2" in file_name:
      file_name = file_name.replace("*2", "")
      file_name = f"__{file_name}__"

    if not os.path.exists(file_name):
      await message.download(file_name, file_name=file_name)
    else:
      await sts.edit("<pre>Fɪʟᴇ ᴘᴀᴛʜ ғᴏᴜɴᴅ</pre>")
  except Exception as err:
    await sts.edit(err)

@Bot.on_message(filters.command(["clean", "c"]) & filters.user(Bot.ADMINS))
async def clean(_, message):
  directory = '/app'
  ex = (".mkv", ".mp4", ".zip", ".pdf", ".png", ".epub", ".temp")
  protected_dirs = (".git", "venv", "env", "__pycache__")  # Directories to SKIP
  sts = await message.reply_text("<pre>Cʟᴇᴀɴɪɴɢ ғɪʟᴇs...</pre>")
  deleted_files = []
  removed_dirs = []
  
  if os.path.exists("Process"):
    shutil.rmtree("Process")
  elif os.path.exists("./Process"):
    shutil.rmtree("./Process")
    
  try:
    for root, dirs, files in os.walk(directory, topdown=False):
      # Skip protected directories (e.g., .git)
      dirs[:] = [d for d in dirs if d not in protected_dirs]
      for file in files:
        if file.lower().endswith(ex):
          file_path = os.path.join(root, file)
          try:
            os.remove(file_path)
            deleted_files.append(file_path)
          except Exception as e:
            pass

        elif file.lower().startswith("vol"):
          file_path = os.path.join(root, file)
          try:
            os.remove(file_path)
            deleted_files.append(file_path)
          except Exception as e:
            pass

      for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        try:
          if not os.listdir(dir_path):  # Check if empty
            os.rmdir(dir_path)
            removed_dirs.append(dir_path)

          elif dir_path == "/app/Downloads":
            os.rmdir("/app/Downloads")
            removed_dirs.append("/app/Downloads")

          elif dir_path == "/app/downloads":
            os.rmdir("/app/downloads")
            removed_dirs.append("/app/downloads")

          try:
            dir_path = int(dir_path)
            os.rmdir(dir_path)
            removed_dirs.append(dir_path)
          except:
            pass
        except Exception as e:
          pass

    msg = "<pre>Cʟᴇᴀɴɪɴɢ ʟᴏɢs :</pre>\n"
    if deleted_files:
      msg += f"Dᴇʟᴇᴛᴇᴅ {len(deleted_files)} Fɪʟᴇs :\n" + "\n".join(deleted_files[:10])  # Show first 10
      if len(deleted_files) > 10:
        msg += f"\n... ᴀɴᴅ {len(deleted_files) - 10} ᴍᴏʀᴇ."
      else:
        msg += "<b><blockquote>✔ Nᴏ ғɪʟᴇs ᴅᴇʟᴇᴛᴇᴅ.</b></blockquote>"

    if removed_dirs:
      msg += f"\n\nRᴇᴍᴏᴠᴇᴅ {len(removed_dirs)} ᴇᴍᴘᴛʏ ᴅɪʀᴇᴄᴛᴏʀɪᴇs :\n" + "\n".join(removed_dirs[:5])
      if len(removed_dirs) > 5:
        msg += f"\n... ᴀɴᴅ {len(removed_dirs) - 5} ᴍᴏʀᴇ."

    await sts.edit(msg[:4096])  # Telegram's max message length
  except Exception as err:
    await sts.edit(f"❌ Error: {str(err)}")

def remove_dir(path):
    try:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                    for dir in dirs:
                        os.rmdir(os.path.join(root, dir))
            os.rmdir(path)
    except Exception as err:
        return err


@Bot.on_message(filters.command("updates"))
async def updates_(_, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<pre>Yᴏᴜ ᴄᴀɴɴᴏᴛ ᴜsᴇ ᴍᴇ ʙᴀʙʏ</pre>")
  try:
    await message.reply_photo(
      photo=random.choice(Vars.PICS),
      caption="<pre>Cʜᴏᴏsᴇ sɪᴛᴇs</pre>",
      reply_markup=plugins_list("updates"),
      quote=True,
    )
  except FloodWait as err:
    await asyncio.sleep(err.value)
    await message.reply_photo(
      photo=random.choice(Vars.PICS),
      caption="<pre>Cʜᴏᴏsᴇ sɪᴛᴇs</pre>",
      reply_markup=plugins_list("updates"),
      quote=True,
    )
  except:
    await message.reply_photo(
      photo=random.choice(Vars.PICS),
      caption="<pre>Cʜᴏᴏsᴇ sɪᴛᴇs</pre>",
      reply_markup=plugins_list("updates"),
      quote=True,
    )
  
@Bot.on_message(filters.command("queue"))
async def queue_msg_handler(client, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<pre>ʏᴏᴜ ᴄᴀɴɴᴏᴛ ᴜsᴇ ᴍᴇ ʙᴀʙʏ</pre>")

  await message.reply(f"<blockquote><b>›› Yᴏᴜʀ ǫᴜᴇᴜᴇ : {queue.get_count_(message.from_user.id)}\n\n›› Tᴏᴛᴀʟ ǫᴜᴇᴜᴇ sɪᴢᴇ : {int(queue.qsize())+1}</b></blockquote>")

@Bot.on_message(filters.command(["us", "user_setting", "user_panel"]))
async def userxsettings(client, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<pre>Yᴏᴜ ᴄᴀɴɴᴏᴛ ᴜsᴇ ᴍᴇ ʙᴀʙʏ</pre>")
  
  sts = await message.reply("<pre>Pʀᴏᴄᴇssɪɴɢ...</pre>")
  try:
    db_type = "uts"
    name = Vars.DB_NAME
    user_id = str(message.from_user.id)
    if not user_id in uts:
      uts[user_id] = {}
      sync(name, db_type)

    if not "setting" in uts[user_id]:
      uts[user_id]['setting'] = {}
      sync(name, db_type)

    thumbnali = uts[user_id]['setting'].get("thumb", None)
    if thumbnali:
      thumb = "True" if not thumbnali.startswith("http") else thumbnali
    else:
      thumb = thumbnali

    banner1 = uts[user_id]['setting'].get("banner1", None)
    banner2 = uts[user_id]['setting'].get("banner2", None)
    if banner1:
      banner1 = "True" if not banner1.startswith("http") else banner1

    if banner2:
      banner2 = "True" if not banner2.startswith("http") else banner2

    txt = users_txt.format(
      id=user_id,
      file_name=uts[user_id]['setting'].get("file_name", "None"),
      caption=uts[user_id]['setting'].get("caption", "None"),
      thumb=thumb,
      banner1=banner1,
      banner2=banner2,
      dump=uts[user_id]['setting'].get("dump", "None"),
      type=uts[user_id]['setting'].get("type", "None"),
      megre=uts[user_id]['setting'].get("megre", "None"),
      regex=uts[user_id]['setting'].get("regex", "None"),
      len=uts[user_id]['setting'].get("file_name_len", "None"),
      password=uts[user_id]['setting'].get("password", "None"),
    )

    button = [
      [
        InlineKeyboardButton("Fɪʟᴇ ɴᴀᴍᴇ", callback_data="ufn"),
        InlineKeyboardButton("Cᴀᴘᴛɪᴏɴ‌", callback_data="ucp")
      ],
      [
        InlineKeyboardButton("Tʜᴜᴍʙɴᴀʟɪ", callback_data="uth"),
        InlineKeyboardButton("Rᴇɢᴇx", callback_data="uregex")
      ],
      [
        InlineKeyboardButton("Bᴀɴɴᴇʀ", callback_data="ubn"),
      ],
      [
        InlineKeyboardButton("Pᴀssᴡᴏʀᴅ", callback_data="upass"),
        InlineKeyboardButton("Mᴇɢʀᴇ sɪᴢᴇ", callback_data="umegre")
      ],
      [
        InlineKeyboardButton("Fɪʟᴇ ᴛʏᴘᴇ", callback_data="u_file_type"),
      ],
    ]
    if not Vars.CONSTANT_DUMP_CHANNEL:
      button[-1].append(InlineKeyboardButton("Dᴜᴍᴘ ᴄʜᴀɴɴᴇʟ", callback_data="udc"))
    
    button.append([InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close")])
    if not thumbnali:
      thumbnali = random.choice(Vars.PICS)
    try:
      await message.reply_photo(thumbnali, caption=txt, reply_markup=InlineKeyboardMarkup(button))
    except FloodWait as err:
      await asyncio.sleep(err.value)
      await message.reply_photo(thumbnali, caption=txt, reply_markup=InlineKeyboardMarkup(button))
    except:
      await message.reply_photo(photo=random.choice(Vars.PICS), caption=txt, reply_markup=InlineKeyboardMarkup(button))

    await sts.delete()
  except Exception as err:
    logger.exception(err)
    await sts.edit(err)

@Bot.on_message(filters.command("help"))
async def help(client, message):
    if Vars.IS_PRIVATE and message.chat.id not in Vars.ADMINS:
        return await message.reply("<code>You cannot use me baby </code>")

    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/RexySama"),
            InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close")
        ]]
    )

    await message.reply_photo(
        photo="https://telegra.ph/HgBotz-08-01-5",  # Replace with your actual image URL or local path
        caption=HELP_MSG,
        message_effect_id=5104841245755180586, 
        reply_markup=buttons
    )

# Add a callback handler for the "Close" button
@Bot.on_callback_query(filters.regex("close"))
async def close_button(client, callback_query):
    try:
        await callback_query.message.delete()
    except:
        await callback_query.answer("Can't delete the message", show_alert=True)



@Bot.on_message(filters.command(["deltask", "cleantasks", "del_tasks", "clean_tasks"]))
async def deltask(client, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<pre>Yᴏᴜ ᴄᴀɴɴᴏᴛ ᴜsᴇ ᴍᴇ ʙᴀʙʏ</pre>")

  user_id = message.from_user.id
  numb = 0
  if user_id in queue._user_data:
    for task_id in queue._user_data[user_id]:
      await queue.delete_task(task_id)
      numb += 1
    await message.reply(f"<pre>Aʟʟ ᴛᴀsᴋs ᴅᴇʟᴇᴛᴇᴅ :- {numb}</pre>")
  else:
    await message.reply("<pre>Nᴏ ᴛᴀsᴋs ғᴏᴜɴᴅ</pre>")


@Bot.on_message(filters.command("subscribe"))
async def subs(_, message):
  if _.IS_PRIVATE:
    if message.chat.id not in _.ADMINS:
      return await message.reply("<pre>Yᴏᴜ ᴄᴀɴɴᴏᴛ ᴜsᴇ ᴍᴇ ʙᴀʙʏ</pre>")
  
  sts = await message.reply_text("<pre>Gᴇᴛᴛɪɴɢ ʏᴏᴜʀ sᴜʙsᴄʀɪʙᴇ ʟɪsᴛ...</pre>")
  txt = "<b><blockquote>◈ Sᴜʙsᴄʀɪʙɪɴɢ ʟɪsᴛ :-</b></blockquote>\n────────────────────────────\n"
  try:
    subs_list = get_subs(message.from_user.id)
    for sub in subs_list:
      txt += f"<blockquote>›› <code>{sub}</code></blockquote>\n────────────────────────────\n"
    
    txt += f"<blockquote>=> <code>Tᴏᴛᴀʟ sᴜʙsᴄʀɪʙᴇ :- {len(subs_list)}</code></blockquote>\n────────────────────────────"
    txt += f"\n<b>Tᴏ ᴜɴsᴜʙsᴄʀɪʙᴇ :-</b>\n<blockquote><code>/unsubscribe</code> ᴜʀʟ</blockquote>\n────────────────────────────"
    await retry_on_flood(sts.edit)(txt[:1024])
  except Exception as err:
    await retry_on_flood(sts.edit)(err)

@Bot.on_message(filters.command("unsubscribe"))
async def unsubs(_, message):
  if _.IS_PRIVATE:
    if message.chat.id not in _.ADMINS:
      return await message.reply("<pre>Yᴏᴜ ᴄᴀɴɴᴏᴛ ᴜsᴇ ᴍᴇ ʙᴀʙʏ</pre>")
  
  sts = await message.reply_text("<pre>Pʀᴏᴄᴇssɪɴɢ ᴛᴏ ᴜɴsᴜʙsᴄʀɪʙᴇ...</pre>")
  try:
    txt = message.text.split(" ")[1]
    if txt in dts:
      if message.from_user.id in dts[txt]['users']:
        dts[txt]['users'].remove(message.from_user.id)
        sync(_.DB_NAME, 'dts')
        await retry_on_flood(sts.edit)("<pre>Sᴜᴄᴇssғᴜʟʟʏ ᴜɴsᴜʙsᴄʀɪʙᴇ</pre>")
      else:
        await retry_on_flood(sts.edit)("<b><blockquote>Yᴏᴜ ᴀʀᴇ ɴᴏᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴛʜɪs ᴍᴀɴɢᴀ | ᴍᴀɴʜᴡᴀ</b></blockquote></code>")
    else:
      await retry_on_flood(sts.edit)("<pre>Mᴀɴɢᴀ ɴᴏᴛ ғᴏᴜɴᴅ</pre>")
  except Exception as err:
    await retry_on_flood(sts.edit)(err)


@Bot.on_message(filters.command("search"))
async def search_group(client, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<pre>Yᴏᴜ ᴄᴀɴɴᴏᴛ ᴜsᴇ ᴍᴇ ʙᴀʙʏ</pre>")
  
  if client.SHORTENER:
    if not await premium_user(message.from_user.id):
      if not verify_token(message.from_user.id):
        if not message.from_user.id in client.ADMINS:
          return await get_token(message, message.from_user.id)
    
  try: txt = message.text.split(" ")[1]
  except: return await message.reply("<b><blockquote>Fᴏʀᴍᴀᴛ :-<code>/search Bleach</code></b></blockquote>")
  photo = random.choice(Vars.PICS)

  try: 
    await message.reply_photo(photo, caption="<pre>Sᴇʟᴇᴄᴛ sᴇᴀʀᴄʜ ᴡᴇʙsɪᴛᴇ</pre>", reply_markup=plugins_list(), quote=True)
  except ValueError: 
    await message.reply_photo(photo, caption="<pre>Sᴇʟᴇᴄᴛ sᴇᴀʀᴄʜ ᴡᴇʙsɪᴛᴇ</pre>", reply_markup=plugins_list(), quote=True)


@Bot.on_message(filters.text & filters.private)
async def search(client, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<pre>Yᴏᴜ ᴄᴀɴɴᴏᴛ ᴜsᴇ ᴍᴇ ʙᴀʙʏ</pre>")

  txt = message.text
  photo = random.choice(Vars.PICS)
  button = []
  if not txt.startswith("/"):
    try: await message.reply_photo(photo, caption="<pre>Sᴇʟᴇᴄᴛ sᴇᴀʀᴄʜ ᴡᴇʙsɪᴛᴇ</pre>", reply_markup=plugins_list(), quote=True)
    except ValueError: await message.reply_photo(photo, caption="<pre>Sᴇʟᴇᴄᴛ sᴇᴀʀᴄʜ ᴡᴇʙsɪᴛᴇ</pre>", reply_markup=plugins_list(), quote=True)
