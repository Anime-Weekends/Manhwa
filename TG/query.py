from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

from .storage import *
from bot import Bot, Vars, logger
import random

from Tools.db import *
from pyrogram.errors import FloodWait


@Bot.on_callback_query(filters.regex("close"))
async def close_handler(_, query):
  try:
    await query.message.delete()
    await query.message.reply_to_message.delete()
  except:
    pass
  
  try: await query.answer()
  except: pass

@Bot.on_callback_query(filters.regex("premuim"))
async def premuim_handler(_, query):
  """This Is Premuim Handler Of Callback Data"""
  button = query.message.reply_markup.inline_keyboard
  text = f"""
<b><i>Premium Price

Pricing Rates
  7 Days - 30 inr / 0.35 USD / NRS 40
  1 Month - 90 inr / 1.05 USD / NRS 140
  3 Months - 260 inr / 2.94 USD / NRS 350
  6 Months - 500 inr / 6.33 USD / NRS 700
  9 Months - 780 inr / 9.14 USD / NRS 1100
  12 Months - 1000 inr / 11.8 USD / NRS 1400

Want To Buy ?!
  Contact or DM - @Shanks_Kun

We Have Limited Seats For Premium Users</i></b>"""
  del button[-2]
  await retry_on_flood(query.edit_message_text)(text, reply_markup=InlineKeyboardMarkup(button))

@Bot.on_callback_query(filters.regex("^chs"))
async def ch_handler(client, query):
  """This Is Information Handler Of Callback Data"""
  reply = query.message.reply_to_message

  user_id = reply.from_user.id
  query_user_id = query.from_user.id
  if user_id != query_user_id:
    return await query.answer("Tʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ", show_alert=True)

  try:
    webs, data = searchs[query.data]
  except:
    return await query.answer("Tʜɪs ɪs ᴀɴ ᴏʟᴅ ʙᴜᴛᴛᴏɴ , ᴘʟᴇᴀsᴇ ʀᴇᴅᴏ ᴛʜᴇ sᴇᴀʀᴄʜ",
                              show_alert=True)

  try: bio_list = await webs.get_chapters(data)
  except: return await query.answer("Nᴏ ᴄʜᴀᴘᴛᴇʀs ғᴏᴜɴᴅ", show_alert=True)
  
  if not bio_list:
    return await query.answer("Nᴏ ᴄʜᴀᴘᴛᴇʀs ғᴏᴜɴᴅ", show_alert=True)

  if "poster" in bio_list:
    try:
      await query.edit_message_media(InputMediaPhoto(bio_list['poster']))
    except:
      pass

  c = query.data.replace("chs", "ch")
  chaptersList[c] = webs, bio_list, data
  sf = webs.sf
  if "msg" in bio_list:
    await retry_on_flood(query.edit_message_text
                         )(bio_list['msg'][:1022],
                           reply_markup=InlineKeyboardMarkup([[
                               InlineKeyboardButton("Cʜᴀᴘᴛᴇʀs",
                                                    callback_data=c),
                               InlineKeyboardButton("Bᴀᴄᴋ",
                                                    callback_data=f"bk.s.{sf}")
                           ]]))
  else:
    await retry_on_flood(query.edit_message_text
                         )(f"{bio_list['title']}",
                           reply_markup=InlineKeyboardMarkup([[
                               InlineKeyboardButton("Cʜᴀᴘᴛᴇʀs",
                                                    callback_data=c),
                               InlineKeyboardButton("Bᴀᴄᴋ",
                                                    callback_data=f"bk.s.{sf}")
                           ]]))



@Bot.on_callback_query(filters.regex("^ch"))
async def p_handler(client, query):
  """This Is Chapters Handler Of Callback Data"""
  if query.data in chaptersList:
    reply = query.message.reply_to_message

    user_id = reply.from_user.id
    query_user_id = query.from_user.id
    if user_id != query_user_id:
      return await query.answer("Tʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ", show_alert=True)

    webs, data, rdata = chaptersList[query.data]
    sf = webs.sf

    try: 
      chapters = await webs.iter_chapters(data)
    except TypeError: 
      chapters = webs.iter_chapters(data)

    subs_bool = get_subs(str(query.from_user.id), rdata['url'])
    if not chapters:
      return await query.answer("Nᴏ ᴄʜᴀᴘᴛᴇʀs ғᴏᴜɴᴅ", show_alert=True)

    button = []
    for chapter in chapters:
      c = f"pic|{hash(chapter['url'])}"
      chaptersList[c] = (webs, chapter)
      button.append(InlineKeyboardButton(chapter['title'], callback_data=c))

    button = split_list(button[:60])
    c = f"pg:{sf}:{hash(chapters[-1]['url'])}:"
    if len(chapters) > 60 or sf == "ck":
      pagination[c] = (webs, data, rdata)
      button.append([
          InlineKeyboardButton(">>", callback_data=f"{c}1"),
          InlineKeyboardButton("2x>", callback_data=f"{c}2"),
          InlineKeyboardButton("5x>", callback_data=f"{c}5")
      ])

    c = f"subs:{hash(rdata['url'])}"
    subscribes[c] = (webs, rdata)
    if subs_bool:
      button.insert(
        0,
        [InlineKeyboardButton("Uɴsᴜʙsᴄʀɪʙᴇ", callback_data=c)])
    else:
      button.insert(
        0,
        [InlineKeyboardButton("Sᴜʙsᴄʀɪʙᴇ", callback_data=c)])
    if sf == "ck":
      callback_data = f"sgh:{sf}:{hash(chapters[0]['url'])}"
      pagination[callback_data] = (chapters, webs, rdata, "1")
      button.append([InlineKeyboardButton("Sᴄᴀɴʟᴀᴛɪᴏɴ ɢʀᴏᴜᴘ", callback_data=callback_data)])
    else:
      callback_data = f"full:{sf}:{hash(chapters[0]['url'])}"
      pagination[callback_data] = (chapters[:60], webs)
      button.append([InlineKeyboardButton("Fᴜʟʟ ᴘᴀɢᴇ", callback_data=callback_data)])
    
    button.append(
        [InlineKeyboardButton("Bᴀᴄᴋ", callback_data=f"bk.s.{sf}")])
    await retry_on_flood(query.edit_message_reply_markup)(InlineKeyboardMarkup(button))
  else:
    try: await query.answer("This is an old button, please redo the search", show_alert=True)
    except: pass


@Bot.on_callback_query(filters.regex("^pg"))
async def pg_handler(client, query):
  """This Is Pagination Handler Of Callback Data"""
  reply = query.message.reply_to_message

  user_id = reply.from_user.id
  query_user_id = query.from_user.id
  if user_id != query_user_id:
    return await query.answer("Tʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ", show_alert=True)

  data = query.data.split(":")
  page = data[-1]
  data = ":".join(data[:-1])
  data = f"{data}:"
  if data in pagination:
    webs, data, rdata = pagination[data]
    sf = webs.sf
    subs_bool = get_subs(str(query.from_user.id), rdata['url'])
    if sf == "ck":
      chapters = await webs.get_chapters(rdata, int(page))
      if not chapters:
        return await query.answer("Nᴏ ᴄʜᴀᴘᴛᴇʀs ғᴏᴜɴᴅ", show_alert=True)

      chapters = webs.iter_chapters(chapters)
    else:
      try: 
        chapters = await webs.iter_chapters(data, int(page))
      except TypeError: 
        chapters = webs.iter_chapters(data, int(page))

    if not chapters:
      return await query.answer("Nᴏ ᴄʜᴀᴘᴛᴇʀs ғᴏᴜɴᴅ", show_alert=True)

    button = []
    for chapter in chapters:
      c = f"pic|{hash(chapter['url'])}"
      chaptersList[c] = (webs, chapter)
      button.append(InlineKeyboardButton(chapter['title'], callback_data=c))

    button = split_list(button[:60])
    c = f"pg:{sf}:{hash(chapters[-1]['url'])}:"
    pagination[c] = (webs, data, rdata)
    if int(page) > 1:
      button.append([
              InlineKeyboardButton("<<", callback_data=f"{c}{int(page) - 1}"),
              InlineKeyboardButton("<2x", callback_data=f"{c}{int(page) - 2}"),
              InlineKeyboardButton("<5x", callback_data=f"{c}{int(page) - 5}")
          ])

    button.append([
          InlineKeyboardButton(">>", callback_data=f"{c}{int(page) + 1}"),
          InlineKeyboardButton("2x>", callback_data=f"{c}{int(page) + 2}"),
          InlineKeyboardButton("5x>", callback_data=f"{c}{int(page) + 5}"),
    ])

    c = f"subs:{hash(rdata['url'])}"
    subscribes[c] = (webs, rdata)
    if subs_bool:
      button.insert(
        0,
        [InlineKeyboardButton("Uɴsᴜʙsᴄʀɪʙᴇ", callback_data=c)])
    else:
      button.insert(
        0,
        [InlineKeyboardButton("Sᴜʙsᴄʀɪʙᴇ", callback_data=c)])
    if sf == "ck":
      callback_data = f"sgh:{sf}:{hash(chapters[0]['url'])}"
      pagination[callback_data] = (chapters, webs, rdata, page)
      button.append([InlineKeyboardButton("Sᴄᴀɴʟᴀᴛɪᴏɴ ɢʀᴏᴜᴘ", callback_data=callback_data)])
    else:
      callback_data = f"full:{sf}:{hash(chapters[0]['url'])}"
      if int(page) == 1:
        pagination[callback_data] = (chapters[:60], webs)
      else:
        pagination[callback_data] = (chapters, webs)
      
      button.append([InlineKeyboardButton("Fᴜʟʟ ᴘᴀɢᴇ", callback_data=callback_data)])

    button.append([InlineKeyboardButton("Bᴀᴄᴋ", callback_data=f"bk.s.{sf}")])
    await retry_on_flood(query.edit_message_reply_markup)(InlineKeyboardMarkup(button))
  else:
    try: await query.answer("Tʜɪs ɪs ᴀɴ ᴏʟᴅ ʙᴜᴛᴛᴏɴ , ᴘʟᴇᴀsᴇ ʀᴇᴅᴏ ᴛʜᴇ sᴇᴀʀᴄʜ", show_alert=True)
    except: pass


@Bot.on_callback_query(filters.regex("^sgh"))
async def cgk_handler(client, query):
  """This Is Scanlation Group Handler Of Callback Data"""
  if query.data in pagination:
    jcallback_back = query.data
    reply = query.message.reply_to_message
    user_id = reply.from_user.id
    query_user_id = query.from_user.id
    if user_id != query_user_id:
      return await query.answer("Tʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ", show_alert=True)
    
    chapters, webs, rdata, page = pagination[query.data]
    data = {}
    for chapter in chapters:
      group_name = chapter['group_name']
      if group_name:
        if group_name not in data:
          data[group_name] = []
        data[group_name].append(chapter)
      else:
        if "Unknown" not in data:
          data["Unknown"] = []
        data["Unknown"].append(chapter)

    button = []
    
    rcallback_data = f"pg:{webs.sf}:{hash(chapters[-1]['url'])}:{page}"
    pagination[rcallback_data] = (webs, chapters, rdata)
    for group_name in data.keys():
      groupLen = len(data[group_name])
      c = f"sgk|{hash(group_name)}"
      pagination[c] = (data[group_name], webs, page, rcallback_data, jcallback_back)
      button.append([InlineKeyboardButton(f"{group_name} ({groupLen})", callback_data=c)])
    
    
    button.append([InlineKeyboardButton("Bᴀᴄᴋ ᴛᴏ ᴄʜᴀᴘᴛᴇʀs", callback_data=rcallback_data)])
    await retry_on_flood(query.edit_message_reply_markup)(InlineKeyboardMarkup(button))
    
    try: await query.answer()
    except: pass
  else:
    try: await query.answer("Tʜɪs ɪs ᴀɴ ᴏʟᴅ ʙᴜᴛᴛᴏɴ , ᴘʟᴇᴀsᴇ ʀᴇᴅᴏ ᴛʜᴇ sᴇᴀʀᴄʜ", show_alert=True)
    except: pass


@Bot.on_callback_query(filters.regex("^sgk"))
async def sgk_handler(client, query):
  if query.data in pagination:
    reply = query.message.reply_to_message
    if reply:
      user_id = reply.from_user.id
      query_user_id = query.from_user.id
      if user_id != query_user_id:
        return await query.answer("Tʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ", show_alert=True)
    
    chapters, webs, page, rcallback_data, jcallback_back = pagination[query.data]
    chapters = list(reversed(chapters)) 
    button = []
    for chapter in chapters:
      c = f"pic|{hash(chapter['url'])}"
      chaptersList[c] = (webs, chapter)
      button.append(InlineKeyboardButton(chapter['title'], callback_data=c))
    
    button = split_list(button[:60])
    callback_data = f"full:{webs.sf}:{hash(chapters[0]['url'])}"
    pagination[callback_data] = (chapters, webs)
    button.append([InlineKeyboardButton("Fᴜʟʟ ᴘᴀɢᴇ", callback_data=callback_data)])
    
    button.append([InlineKeyboardButton("Bᴀᴄᴋ ᴛᴏ ɢʀᴏᴜᴘs", callback_data=jcallback_back)])
    button.append([InlineKeyboardButton("Bᴀᴄᴋ ᴛᴏ ᴄʜᴀᴘᴛᴇʀs", callback_data=rcallback_data)])
    await retry_on_flood(query.edit_message_reply_markup)(InlineKeyboardMarkup(button))
    try: await query.answer()
    except: pass
  else:
    try: await query.answer("Tʜɪs ɪs ᴀɴ ᴏʟᴅ ʙᴜᴛᴛᴏɴ , ᴘʟᴇᴀsᴇ ʀᴇᴅᴏ ᴛʜᴇ sᴇᴀʀᴄʜ", show_alert=True)
    except: pass


@Bot.on_callback_query(filters.regex("^full"))
async def full_handler(client, query):
  """This Is Full Page Handler Of Callback Data"""
  if query.data in pagination:
    reply = query.message.reply_to_message

    user_id = reply.from_user.id
    query_user_id = query.from_user.id
    if user_id != query_user_id:
      return await query.answer("Tʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ", show_alert=True)

    chapters, webs = pagination[query.data]
    added_item = []

    merge_size = uts[str(query.from_user.id)].get('setting', {}).get('megre', None)
    merge_size = int(merge_size) if merge_size else merge_size

    chapters = list(reversed(chapters)) 
    if merge_size:
      for i in range(0, len(chapters), merge_size):
        data = chapters[i:i + merge_size]
        raw_data = []
        pictures = []
        for chapter in data:
          episode_num = get_episode_number(chapter['title'])
          if not episode_num in added_item:
            pictures_ex = await webs.get_pictures(url=chapter['url'], data=chapter)
            if pictures_ex:
              if webs.bg:
                pictures_ex.remove(pictures_ex[0])

              pictures.extend(pictures_ex)
              added_item.append(episode_num)
              raw_data.append(chapter)
        if pictures:
          task_id = await queue.put((raw_data, pictures, query, None, webs), query.from_user.id)
    else:
      for data in chapters:
        episode_num = get_episode_number(data['title'])
        if not episode_num in added_item:
          pictures = await webs.get_pictures(url=data['url'], data=data)
          if not pictures:
            await retry_on_flood(sts.edit)("Nᴏ ᴘɪᴄᴛᴜʀᴇs ғᴏᴜɴᴅ")

          task_id = await queue.put((data, pictures, query, None, webs), query.from_user.id)
          added_item.append(episode_num)
    
    try: await query.answer("Aᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ", show_alert=True)
    except: pass
  else:
    try: await query.answer("Tʜɪs ɪs ᴀɴ ᴏʟᴅ ʙᴜᴛᴛᴏɴ , ᴘʟᴇᴀsᴇ ʀᴇᴅᴏ ᴛʜᴇ sᴇᴀʀᴄʜ", show_alert=True)
    except: pass


@Bot.on_callback_query(filters.regex("^subs"))
async def subs_handler(client, query):
  """This Is Subscribe Handler Of Callback Data"""
  if query.data in subscribes:
    webs, data = subscribes[query.data]

    reply = query.message.reply_to_message

    user_id = reply.from_user.id
    query_user_id = query.from_user.id
    if user_id != query_user_id:
      return await query.answer("Tʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ", show_alert=True)

    reply_markup = query.message.reply_markup
    button = reply_markup.inline_keyboard

    if get_subs(str(query.from_user.id), data['url']):
      delete_sub(str(query.from_user.id), data['url'])
      button[0] = [InlineKeyboardButton("Sᴜʙsᴄʀɪʙᴇ", callback_data=query.data)]
    else:
      add_sub(str(query.from_user.id), data['url'])
      button[0] = [InlineKeyboardButton("Uɴsᴜʙsᴄʀɪʙᴇ", callback_data=query.data)]
    await retry_on_flood(query.edit_message_reply_markup)(InlineKeyboardMarkup(button))
  else:
    try: await query.answer("Tʜɪs ɪs ᴀɴ ᴏʟᴅ ʙᴜᴛᴛᴏɴ , ᴘʟᴇᴀsᴇ ʀᴇᴅᴏ ᴛʜᴇ sᴇᴀʀᴄʜ", show_alert=True)
    except: pass


@Bot.on_callback_query(filters.regex("^pic"))
async def pic_handler(client, query):
  """This Is Pictures Handler Of Callback Data"""
  if query.data in chaptersList:
    webs, data = chaptersList[query.data]
    reply = query.message.reply_to_message

    user_id = reply.from_user.id
    query_user_id = query.from_user.id
    if user_id != query_user_id:
      return await query.answer("Tʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ", show_alert=True)

    pictures = await webs.get_pictures(url=data['url'], data=data)
    if not pictures:
      return await query.answer("Nᴏ ᴘɪᴄᴛᴜʀᴇs ғᴏᴜɴᴅ", show_alert=True)

    sts = await retry_on_flood(query.message.reply_text
       )("<pre>Aᴅᴅɪɴɢ...</pre>")

    txt = f"<b><blockquote>Mᴀɴɢᴀ ɴᴀᴍᴇ : {data['manga_title']}</b></blockquote>\n<b><blockquote>Cʜᴀᴘᴛᴇʀ : - {data['title']}</b></blockquote>"

    task_id = await queue.put((data, pictures, query, sts, webs), query.from_user.id)
    button = [[
        InlineKeyboardButton(" Cᴀɴᴄᴇʟ ʏᴏᴜʀ ᴛᴀsᴋs ",
                             callback_data=f"cl:{task_id}")
    ]]
    await retry_on_flood(sts.edit)(txt, reply_markup=InlineKeyboardMarkup(button))
  else:
    try: await query.answer("Tʜɪs ɪs ᴀɴ ᴏʟᴅ ʙᴜᴛᴛᴏɴ , ᴘʟᴇᴀsᴇ ʀᴇᴅᴏ ᴛʜᴇ sᴇᴀʀᴄʜ", show_alert=True)
    except: pass


@Bot.on_callback_query(filters.regex("^cl"))
async def cl_handler(client, query):
  """This Is Cancel Handler Of Callback Data"""
  task_id = query.data.split(":")[-1]
  reply = query.message.reply_to_message

  if await queue.delete_task(task_id):
    await retry_on_flood(query.message.edit_text)("<pre>Tᴀsᴋ ᴄᴀɴᴄᴇʟʟᴇᴅ !</pre>")
  else:
    await retry_on_flood(query.answer)("Tᴀsᴋ ɴᴏᴛ ғᴏᴜɴᴅ", show_alert=True)


@Bot.on_callback_query(filters.regex("^bk"))
async def bk_handler(client, query):
  """This Is Back Handler Of Callback Data"""
  reply = query.message.reply_to_message
  try:
    user_id = reply.from_user.id
    query_user_id = query.from_user.id
    if user_id != query_user_id:
      return await query.answer("Tʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ", show_alert=True)
  except:
    pass
  
  if query.data == "bk.p":
    try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
    except: pass
    if reply and reply.text == "/updates":
      await query.edit_message_reply_markup(plugins_list("updates"))
    else:
      await query.edit_message_reply_markup(plugins_list())
  elif query.data.startswith("bk.s"):
    data = query.data
    sf = query.data.split(".")[-1]
    
    reply = reply.text
    if reply.startswith("/search"):
      search = reply.split(" ", 1)[-1]
    else:
      search = reply

    webs = get_webs(sf)
    if webs:
      photo = random.choice(Vars.PICS)
      try:
        await query.edit_message_media(InputMediaPhoto(photo))
      except:
        pass

      reply_markup = query.message.reply_markup
      if query.message.reply_to_message:
        try:
          if reply.startswith("/updates"):
            try:
              await query.message.edit_text("<pre>Uᴘᴅᴀᴛɪɴɢ...</pre>")
            except:
              pass
            
            results = await webs.get_updates()
            for result in results:
              result['title'] = result.pop('manga_title')
            
          else:
            try:
              await query.message.edit_text("<pre>Sᴇᴀʀᴄʜɪɴɢ...</pre>")
            except:
              pass
            
            results = await webs.search(search)
        except:
          return await query.edit_message_text("<pre>Nᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ</pre>", reply_markup=reply_markup)
        
        if results:
          button = []
          for result in results:
            c = f"chs|{data}{result['id']}" if "id" in result else f"chs|{data}{hash(result['url'])}"
            searchs[c] = (webs, result)
            button.append(
                [InlineKeyboardButton(result['title'], callback_data=c)])

          button.append(
              [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="bk.p")])
          await retry_on_flood(query.edit_message_text
                               )("<pre>Sᴇʟᴇᴄᴛ ᴍᴀɴɢᴀ</pre>",
                                 reply_markup=InlineKeyboardMarkup(button))
        else:
          await retry_on_flood(query.message.edit_text
                               )("<pre>Nᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ</pre>",
                                 reply_markup=reply_markup)


@Bot.on_callback_query(filters.regex("^udat"))
async def updates_handler(_, query):
  sf = query.data.split("_")[-1]
  webs = get_webs(sf)
  
  await retry_on_flood(query.edit_message_text)("<pre>Gᴇᴛᴛɪɴɢ ᴜᴘᴅᴀᴛᴇs...</pre>")
  if webs:
    results = await webs.get_updates()
    button = []
    if results:
      for result in results[:60]:
        c = f"chs|{sf}{result['id']}" if "id" in result else f"chs|{sf}{hash(result['url'])}"
        result['title'] = result.pop('manga_title')
        searchs[c] = (webs, result)
        button.append([InlineKeyboardButton(result['title'], callback_data=c)])
      
      button.append([InlineKeyboardButton("Bᴀᴄᴋ", callback_data="bk.p")])
      
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass
      
      await retry_on_flood(query.edit_message_text)("<pre>Sᴇʟᴇᴄᴛ ᴍᴀɴɢᴀ</pre>", reply_markup=InlineKeyboardMarkup(button))
      try: await query.answer()
      except: pass
    else:
      try: await query.answer("Iᴛ's ʜᴀʀᴅ ᴛᴏ ᴀᴅᴅ ᴡᴇʙsɪᴛᴇ ᴜᴘᴅᴀᴛᴇs", show_alert=True)
      except: pass
  else:
    try: await query.answer("Wᴇʙsɪᴛᴇs ɴᴏᴛ ғᴏᴜɴᴅ ᴀᴛ ᴅᴀᴛᴀʙᴀsᴇ", show_alert=True)
    except: pass


@Bot.on_callback_query(filters.regex("^plugin_"))
async def cb_handler(client, query):
  data = query.data
  data = data.split("_")[-1]
  photo = random.choice(Vars.PICS)
  reply = query.message.reply_to_message

  user_id = reply.from_user.id
  query_user_id = query.from_user.id
  if user_id != query_user_id:
    return await query.answer("Tʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ", show_alert=True)

  reply = reply.text
  if reply.startswith("/search"):
    search = reply.split(" ", 1)[-1]
  else:
    search = reply
  for i in web_data.keys():
    if data == web_data[i].sf:
      try:
        await query.edit_message_media(InputMediaPhoto(photo))
      except:
        pass

      reply_markup = query.message.reply_markup
      try:
        await query.edit_message_text("<pre>Sᴇᴀʀᴄʜɪɴɢ...</pre>")
      except:
        pass

      try: results = await web_data[i].search(search)
      except: await query.edit_message_text("<pre>Nᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ</pre>", reply_markup=reply_markup)
      
      if results:
        button = []
        for result in results:
          c = f"chs|{data}{result['id']}" if "id" in result else f"chs|{data}{hash(result['url'])}"
          searchs[c] = (web_data[i], result)
          button.append(
              [InlineKeyboardButton(result['title'], callback_data=c)])

        button.append([InlineKeyboardButton("Bᴀᴄᴋ", callback_data="bk.p")])
        await retry_on_flood(query.edit_message_text
                             )("<pre>Sᴇʟᴇᴄᴛ ᴍᴀɴɢᴀ</pre>",
                               reply_markup=InlineKeyboardMarkup(button))
      else:
        await retry_on_flood(query.edit_message_text
                             )("<pre>Nᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ</pre>",
                               reply_markup=reply_markup)

      try:
        await query.answer()
      except:
        pass
      finally:
        return

  try:
    await query.answer('Tʜɪs ɪs ᴀɴ ᴏʟᴅ ʙᴜᴛᴛᴏɴ , ᴘʟᴇᴀsᴇ ʀᴇᴅᴏ ᴛʜᴇ sᴇᴀʀᴄʜ',
                       show_alert=True)
  except:
    pass
  finally:
    return


'''
@Bot.on_callback_query()
async def extra_handler(client, query):
  try: 
    await query.answer('This is an old button, please redo the search',
       show_alert=True)
  except:
    pass
'''

db_type = "uts"
name = Vars.DB_NAME

@Bot.on_callback_query(filters.regex("mus"))
async def main_user_panel(_, query):
  user_id = str(query.from_user.id)
  if not user_id in uts:
    uts[user_id] = {}
    sync(name, db_type)

  if not "setting" in uts[user_id]:
    uts[user_id]['setting'] = {}
    sync(name, db_type)

  thumbnali = uts[user_id]['setting'].get("thumb", None)
  banner1 = uts[user_id]['setting'].get("banner1", None)
  banner2 = uts[user_id]['setting'].get("banner2", None)

  if thumbnali:
    thumb = "True" if not thumbnali.startswith("http") else thumbnali
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
  
  try: await query.edit_message_media(InputMediaPhoto(thumbnali))
  except: pass

  try:
    await query.edit_message_caption(txt, reply_markup=InlineKeyboardMarkup(button))
  except FloodWait as er:
    await asyncio.sleep(er.value)
    await query.edit_message_caption(txt, reply_markup=InlineKeyboardMarkup(button))

  try: await query.answer()
  except: pass


@Bot.on_callback_query(filters.regex("^ufn"))
async def file_name_handler(_, query):
  user_id = str(query.from_user.id)
  if not user_id in uts:
    uts[user_id] = {}

    uts[user_id]['setting'] = {}

    sync(name, db_type)

  file_name = uts[user_id]['setting'].get("file_name", None)
  caption = uts[user_id]['setting'].get("caption", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  banner1 = uts[user_id]['setting'].get("banner1", None)
  banner2 = uts[user_id]['setting'].get("banner2", None)
  dump = uts[user_id]['setting'].get("dump", None)
  type = uts[user_id]['setting'].get("type", None)
  megre= uts[user_id]['setting'].get("megre", None)
  regex = uts[user_id]['setting'].get("regex", None)
  file_name_len = uts[user_id]['setting'].get("file_name_len", None)
  password = uts[user_id]['setting'].get("password", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  if thumb:
    thumb = "True" if not thumb.startswith("http") else thumb

  button = [
    [InlineKeyboardButton("Sᴇᴛ | ᴄʜᴀɴɢᴇ", callback_data="ufn_change"), InlineKeyboardButton("Dᴇʟᴇᴛᴇ", callback_data="ufn_delete")],
    [InlineKeyboardButton("Sᴇᴛ | ᴄʜᴀɴɢᴇ ", callback_data="ufn_len_change"), InlineKeyboardButton("Dᴇʟᴇᴛᴇ ʟᴇɴ", callback_data="ufn_len_delete")],
    [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="mus")]
  ]
  if query.data == "ufn":
    txt = users_txt.format(
      id = user_id,
      file_name = file_name,
      caption = caption,
      thumb = thumb,
      banner1 = banner1,
      banner2 = banner2,
      dump = dump,
      type = type,
      megre= megre,
      regex = regex,
      len = file_name_len,
      password = password
    )
    await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))

  elif query.data == "ufn_change":
    try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
    except: pass
    
    await retry_on_flood(query.edit_message_caption)("<b><pre>◈ Sᴇɴᴅ ғɪʟᴇ ɴᴀᴍᴇ</pre>\n────────────────────────────\n<b><blockquote>›› <code>{manga_title}</code> : Mᴀɴɢᴀ ɴᴀᴍᴇ\n›› <code>{chapter_num}</code> : Cʜᴀᴘᴛᴇʀ ɴᴜᴍʙᴇʀ</b></blockquote>\n────────────────────────────")
    try:
      call = await _.listen(user_id=int(user_id), timeout=60)

      uts[user_id]['setting']["file_name"] = call.text
      sync(name, db_type)

      txt = users_txt.format(
        id = user_id,
        file_name = call.text,
        caption = caption,
        thumb = thumb,
        banner1 = banner1,
        banner2 = banner2,
        dump = dump,
        type = type,
        megre= megre,
        regex = regex,
        len = file_name_len,
        password = password,
      )
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass
      
      await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
      await call.delete()
      
      try: await query.answer("Sᴜᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ")
      except: pass
    except asyncio.TimeoutError:
      txt = users_txt.format(
        id = user_id,
        file_name = file_name,
        caption = caption,
        thumb = thumb,
        banner1 = banner1,
        banner2 = banner2,
        dump = dump,
        type = type,
        megre= megre,
        regex = regex,
        len = file_name_len,
        password = password,
      )
      await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))

  elif query.data == "ufn_delete":
    if file_name:
      uts[user_id]['setting']["file_name"] = None
      sync(name, db_type)

      txt = users_txt.format(
        id = user_id,
        file_name = "None",
        caption = caption,
        thumb = thumb,
        banner1 = banner1,
        banner2 = banner2,
        dump = dump,
        type = type,
        megre= megre,
        regex = regex,
        len = file_name_len,
        password = password,
      )
      
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass
      
      await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
      
      try: await query.answer("Sᴜᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ")
      except: pass
    else:
      await retry_on_flood(query.answer)("Yᴏᴜ ʜᴀs ɴᴏᴛ sᴇᴛ ɪᴛ !", show_alert=True)

  elif query.data == "ufn_len_change":
    try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
    except: pass
    
    await retry_on_flood(query.edit_message_caption)("<pre>◈ Sᴇɴᴅ ғɪʟᴇ ɴᴀᴍᴇ ʟᴇɴ</pre>\n────────────────────────────\n<b><blockquote>›› Exᴀᴍᴘʟᴇ: 15, 20, 50</b></blockquote>\n────────────────────────────")
    try:
      call = await _.listen(int(user_id), timeout=60)
      try:
        len_ch = int(call.text)
        uts[user_id]['setting']["file_name_len"] = call.text
        sync(name, db_type)
        
        file_name_len = int(call.text)
        
        await call.delete()
        await retry_on_flood(query.answer)("Sᴜᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ")
        
      except ValueError:
        await retry_on_flood(query.answer)("Tʜɪs ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀ", show_alert=True)

    except asyncio.TimeoutError:
      await retry_on_flood(query.answer)("Tɪᴍᴇᴏᴜᴛ ")
    
    txt = users_txt.format(
      id = user_id,
      file_name = file_name,
      caption = caption,
      thumb = thumb,
      banner1 = banner1,
      banner2 = banner2,
      dump = dump,
      type = type,
      megre= megre,
      regex = regex,
      len = file_name_len,
      password = password,
    )
    try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
    except: pass
    
    await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
    

  elif query.data == "ufn_len_delete":
    if file_name_len:
      uts[user_id]['setting']["file_name_len"] = None
      sync(name, db_type)

      txt = users_txt.format(
        id = user_id,
        file_name = file_name,
        caption = caption,
        thumb = thumb,
        banner1 = banner1,
        banner2 = banner2,
        dump = dump,
        type = type,
        megre= megre,
        regex = regex,
        len = "None",
        password = password,
      )
      if not thumb:
        try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
        except: pass
      
      await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
      await retry_on_flood(query.answer)("Sᴜᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ")
    else:
      await retry_on_flood(query.answer)("Yᴏᴜ ʜᴀs ɴᴏᴛ sᴇᴛ ɪᴛ !", show_alert=True)

  try: await query.answer()
  except: pass


@Bot.on_callback_query(filters.regex("^ucp"))
async def caption_handler(_, query):
  user_id = str(query.from_user.id)
  if not user_id in uts:
    uts[user_id] = {}
    sync(name, db_type)

    uts[user_id]['setting'] = {}
    sync(name, db_type)

  file_name = uts[user_id]['setting'].get("file_name", None)
  caption = uts[user_id]['setting'].get("caption", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  banner1 = uts[user_id]['setting'].get("banner1", None)
  banner2 = uts[user_id]['setting'].get("banner2", None)
  dump = uts[user_id]['setting'].get("dump", None)
  type = uts[user_id]['setting'].get("type", None)
  megre= uts[user_id]['setting'].get("megre", None)
  regex = uts[user_id]['setting'].get("regex", None)
  file_name_len = uts[user_id]['setting'].get("file_name_len", None)
  password = uts[user_id]['setting'].get("password", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  if thumb:
    thumb = "True" if not thumb.startswith("http") else thumb

  button = [
    [InlineKeyboardButton("Sᴇᴛ | ᴄʜᴀɴɢᴇ", callback_data="ucp_change"), InlineKeyboardButton("Dᴇʟᴇᴛᴇ", callback_data="ucp_delete")],
    [InlineKeyboardButton("Bᴀᴄᴋ ", callback_data="mus")]
  ]

  if query.data == "ucp":
    await retry_on_flood(query.edit_message_reply_markup)(InlineKeyboardMarkup(button))

  elif query.data == "ucp_change":
    button = [
      [InlineKeyboardButton("Sᴇᴛ | ᴄʜᴀɴɢᴇ", callback_data="ucp_change"), InlineKeyboardButton("Dᴇʟᴇᴛᴇ", callback_data="ucp_delete")],
      [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="mus")]
    ]
    if not thumb:
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass
    
    await retry_on_flood(query.edit_message_caption)("<pre>◈ Sᴇɴᴅ ᴄᴀᴘᴛɪᴏɴ</pre>\n────────────────────────────\n<blockquote>Usᴇ ʜᴛᴍʟ ᴛᴀɢs ғᴏʀ ʙᴏʟᴅ, ɪᴛᴀʟɪᴄ, ᴇᴛᴄ...</blockquote>\n────────────────────────────\n<b><blockquote>›› <code>{manga_title}</code> : Mᴀɴɢᴀ ɴᴀᴍᴇ \n›› <code>{chapter_num}</code> : Cʜᴀᴘᴛᴇʀ ɴᴜᴍʙᴇʀ\n›› <code>{file_name}</code> : Fɪʟᴇ ɴᴀᴍᴇ</b></blockquote>\n────────────────────────────")
    try:
      call = await _.listen(user_id=int(user_id), timeout=60)

      uts[user_id]['setting']["caption"] = call.text
      sync(name, db_type)
      
      caption = call.text
      
      await call.delete()

    except asyncio.TimeoutError:
      await retry_on_flood(query.answer)("Tɪᴍᴇᴏᴜᴛ")

    except Exception as err:
      await retry_on_flood(query.answer)(f"{err}", show_alert=True)
    
    txt = users_txt.format(
      id=user_id,
      file_name=file_name,
      caption=caption,
      thumb=thumb,
      banner1=banner1,
      banner2=banner2,
      dump=dump,
      type=type,
      megre=megre,
      regex=regex,
      len=file_name_len,
      password=password,
    )

    if not thumb:
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass

    await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))

  elif query.data == "ucp_delete":
    if caption:
      uts[user_id]['setting']["caption"] = None
      sync(name, db_type)

      txt = users_txt.format(
        id = user_id,
        file_name = file_name,
        caption = "None",
        thumb = thumb,
        banner1 = banner1,
        banner2 = banner2,
        dump = dump,
        type = type,
        megre= megre,
        regex = regex,
        len = file_name_len,
        password = password,
      )
      if not thumb:
        try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
        except: pass

      await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
      await retry_on_flood(query.answer)("Sᴜᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ")
      
    else:
      await retry_on_flood(query.answer)("Yᴏᴜ ʜᴀs ɴᴏᴛ sᴇᴛ ɪᴛ !", show_alert=True)

  try: await query.answer()
  except: pass


@Bot.on_callback_query(filters.regex("^uth"))
async def thumb_handler(_, query):
  user_id = str(query.from_user.id)
  if not user_id in uts:
    uts[user_id] = {}
    sync(name, db_type)

    uts[user_id]['setting'] = {}
    sync(name, db_type)

  file_name = uts[user_id]['setting'].get("file_name", None)
  caption = uts[user_id]['setting'].get("caption", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  banner1 = uts[user_id]['setting'].get("banner1", None)
  banner2 = uts[user_id]['setting'].get("banner2", None)
  dump = uts[user_id]['setting'].get("dump", None)
  type = uts[user_id]['setting'].get("type", None)
  megre= uts[user_id]['setting'].get("megre", None)
  regex = uts[user_id]['setting'].get("regex", None)
  file_name_len = uts[user_id]['setting'].get("file_name_len", None)
  password = uts[user_id]['setting'].get("password", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  if thumb:
    thumb = "True" if not thumb.startswith("http") else thumb
  
  button = [
    [
      InlineKeyboardButton("Sᴇᴛ | ᴄʜᴀɴɢᴇ", callback_data="uth_change"),
      InlineKeyboardButton("Cᴏɴsᴛᴀɴᴛ", callback_data="uth_constant")
    ],
    [
      InlineKeyboardButton("Dᴇʟᴇᴛᴇ", callback_data="uth_delete"),
      InlineKeyboardButton("Bᴀᴄᴋ", callback_data="mus"),
    ]
  ]
  
  if query.data == "uth":
    txt = users_txt.format(
      id = user_id,
      file_name = file_name,
      caption = caption,
      thumb = thumb,
      banner1 = banner1,
      banner2 = banner2,
      dump = dump,
      type = type,
      megre= megre,
      regex = regex,
      len = file_name_len,
      password = password,
    )
    txt += "\n<blockquote><b>Cᴏɴsᴛᴀɴᴛ :- ᴛʜᴇ ᴘᴀʀᴄᴛɪᴄᴜʟᴀʀ ᴘᴏsᴛᴇʀ ᴏғ ᴍᴀɴɢᴀ ᴡɪʟʟ ᴀᴅᴅᴇᴅ ᴀs ғɪʟᴇ ᴛʜᴜᴍʙɴᴀʟɪ</b></blockquote>"
    
    if thumb:
      try: await query.edit_message_media(InputMediaPhoto(thumb))
      except: pass
    else:
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass

    await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
  
  elif query.data == "uth_constant":
    uts[user_id]['setting']["thumb"] = "constant"
    sync(name, db_type)
    
    txt = users_txt.format(
      id = user_id,
      file_name = file_name,
      caption = caption,
      thumb = "constant",
      banner1 = banner1,
      banner2 = banner2,
      dump = dump,
      type = type,
      megre= megre,
      regex = regex,
      len = file_name_len,
      password = password
    )
    try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
    except: pass
    
    await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
    await retry_on_flood(query.answer)("Sᴜᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ")
    
  elif query.data == "uth_change":
    await retry_on_flood(query.edit_message_caption)("<pre>◈ Sᴇɴᴅ ᴛʜᴜᴍʙɴᴀɪʟ</pre>\n────────────────────────────\n<blockquote><b>›› Yᴏᴜ ᴄᴀɴ sᴇɴᴅ ʟɪɴᴋs ᴏʀ ɪᴍᴀɢᴇs ᴅᴏᴄs..</blockquote></b>\n────────────────────────────")
    try:
      call = await _.listen(user_id=int(user_id), timeout=60)
      call_type = call.photo or call.document or None
      if call_type:
        call_type = call_type.file_id
        uts[user_id]['setting']["thumb"] = call_type
        sync(name, db_type)

      elif not call_type:
        call_type = call.text
        uts[user_id]['setting']["thumb"] = call_type
        sync(name, db_type)

      else:
        await retry_on_flood(query.answer)("Tʜɪs ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ᴛʜᴜᴍʙɴᴀɪʟ", show_alert=True)
        return

      thumb = "True" if not str(call_type).startswith("http") else call_type

      txt = users_txt.format(
        id = user_id,
        file_name = file_name,
        caption = caption,
        thumb = thumb,
        banner1 = banner1,
        banner2 = banner2,
        dump = dump,
        type = type,
        megre= megre,
        regex = regex,
        len = file_name_len,
        password = password,
      )
      if thumb:
        try: await query.edit_message_media(InputMediaPhoto(thumb))
        except: pass

      await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
      
      await call.delete()
      await retry_on_flood(query.answer)("Sᴜᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ")
    except asyncio.TimeoutError:
      await retry_on_flood(query.answer)("Tɪᴍᴇᴏᴜᴛ")
    except Exception as err:
      await retry_on_flood(query.answer)(f"{err}", show_alert=True)

  elif query.data == "uth_delete":
    if thumb:
      uts[user_id]['setting']["thumb"] = None
      sync(name, db_type)

      txt = users_txt.format(
        id=user_id,
        file_name=file_name,
        caption=caption,
        thumb="None",
        banner1=banner1,
        banner2=banner2,
        dump=dump,
        type=type,
        megre=megre,
        regex=regex,
        len=file_name_len,
        password=password,
      )
      
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass
      await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
    else:
      await retry_on_flood(query.answer)("Yᴏᴜ ʜᴀs ɴᴏᴛ sᴇᴛ ɪᴛ !", show_alert=True)

  try: await query.answer()
  except: pass


@Bot.on_callback_query(filters.regex("^ubn"))
async def banner_handler(_, query):
  user_id = str(query.from_user.id)

  if not user_id in uts:
    uts[user_id] = {}
    sync(name, db_type)

    uts[user_id]['setting'] = {}
    sync(name, db_type)

  file_name = uts[user_id]['setting'].get("file_name", None)
  caption = uts[user_id]['setting'].get("caption", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  banner1 = uts[user_id]['setting'].get("banner1", None)
  banner2 = uts[user_id]['setting'].get("banner2", None)
  dump = uts[user_id]['setting'].get("dump", None)
  type = uts[user_id]['setting'].get("type", None)
  megre= uts[user_id]['setting'].get("megre", None)
  regex = uts[user_id]['setting'].get("regex", None)
  file_name_len = uts[user_id]['setting'].get("file_name_len", None)
  password = uts[user_id]['setting'].get("password", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  if thumb:
    thumb = "True" if not thumb.startswith("http") else thumb

  button = [
    [InlineKeyboardButton("Sᴇᴛ | ᴄʜᴀɴɢᴇ 1", callback_data="ubn_set1"), InlineKeyboardButton("Dᴇʟᴇᴛᴇ 1", callback_data="ubn_delete1")],
    [InlineKeyboardButton("Sᴇᴛ | ᴄʜᴀɴɢᴇ 2 ", callback_data="ubn_set2"), InlineKeyboardButton("Dᴇʟᴇᴛᴇ 2", callback_data="ubn_delete2")],
    [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="mus")]
  ]
  if query.data == "ubn":
    await retry_on_flood(query.edit_message_reply_markup)(InlineKeyboardMarkup(button))

  if query.data.startswith("ubn_set"):
    if banner1:
      try: await query.edit_message_media(InputMediaPhoto(banner1))
      except: pass
    elif banner2:
      try: await query.edit_message_media(InputMediaPhoto(banner2))
      except: pass
    elif not thumb:
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass
    
    await retry_on_flood(query.edit_message_caption)("<pre>◈ Sᴇɴᴅ ʙᴀɴɴᴇʀ\n────────────────────────────\n<blockquote><b>›› Yᴏᴜ ᴄᴀɴ sᴇɴᴅ ʟɪɴᴋs ᴏʀ ɪᴍᴀɢᴇs ᴅᴏᴄs..</blockquote></b>\n────────────────────────────")
    try:
      call = await _.listen(user_id=int(user_id), timeout=60)
      call_type = call.photo or call.document or None
      if call_type:
        banner = call.photo.file_id
      elif not call_type:
        banner = call.text
      else:
        await retry_on_flood(query.answer)("ᴛʜɪs ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ᴛʜᴜᴍʙɴᴀɪʟ")
        return

      if query.data == "ubn_set1":
        uts[user_id]['setting']["banner1"] = banner
        sync(name, db_type)

        banner = banner if banner.startswith("http") else "True"
        txt = users_txt.format(
          id=user_id,
          file_name=file_name,
          caption=caption,
          thumb=thumb,
          banner1=banner,
          banner2=banner2,
          dump=dump,
          type=type,
          megre=megre,
          regex=regex,
          len=file_name_len,
          password=password,
        )

      elif query.data == "ubn_set2":
        uts[user_id]['setting']["banner2"] = banner
        sync(name, db_type)

        banner = banner if banner.startswith("http") else "True"
        txt = users_txt.format(
          id=user_id,
          file_name=file_name,
          caption=caption,
          thumb=thumb,
          banner1=banner1,
          banner2=banner,
          dump=dump,
          type=type,
          megre=megre,
          regex=regex,
          len=file_name_len,
          password=password,
        )
        if not thumb:
          try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
          except: pass

        await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
    except asyncio.TimeoutError:
      await retry_on_flood(query.answer)("Tɪᴍᴇᴏᴜᴛ")
    except Exception as err:
      await retry_on_flood(query.answer)(f"{err}", show_alert=True)

  elif query.data == "ubn_delete1":
    if banner1:
        uts[user_id]['setting']["banner1"] = None
        sync(name, db_type)

        txt = users_txt.format(
          id=user_id,
          file_name=file_name,
          caption=caption,
          thumb=thumb,
          banner1="None",
          banner2=banner2,
          dump=dump,
          type=type,
          megre=megre,
          regex=regex,
          len=file_name_len,
          password=password,
        )
        if not thumb:
          try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
          except: pass

        await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
        await retry_on_flood(query.answer)("Sᴜᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ")
    else:
      await retry_on_flood(query.answer)("Yᴏᴜ ʜᴀs ɴᴏᴛ sᴇᴛ ɪᴛ !", show_alert=True)

  elif query.data == "ubn_delete2":
    if banner2:
      uts[user_id]['setting']["banner2"] = None
      sync(name, db_type)

      txt = users_txt.format(
        id=user_id,
        file_name=file_name,
        caption=caption,
        thumb=thumb,
        banner1=banner1,
        banner2="None",
        dump=dump,
        type=type,
        megre=megre,
        regex=regex,
        len=file_name_len,
        password=password,
      )
      if not thumb:
        try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
        except: pass

      await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
      await retry_on_flood(query.answer)("Sᴜᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ")
    else:
      await retry_on_flood(query.answer)("Yᴏᴜ ʜᴀs ɴᴏᴛ sᴇᴛ ɪᴛ !", show_alert=True)

  try: await query.answer()
  except: pass

@Bot.on_callback_query(filters.regex("^udc"))
async def dump_handler(_, query):
  user_id = str(query.from_user.id)
  if not user_id in uts:
    uts[user_id] = {}
    sync(name, db_type)

    uts[user_id]['setting'] = {}
    sync(name, db_type)

  file_name = uts[user_id]['setting'].get("file_name", None)
  caption = uts[user_id]['setting'].get("caption", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  banner1 = uts[user_id]['setting'].get("banner1", None)
  banner2 = uts[user_id]['setting'].get("banner2", None)
  dump = uts[user_id]['setting'].get("dump", None)
  type = uts[user_id]['setting'].get("type", None)
  megre= uts[user_id]['setting'].get("megre", None)
  regex = uts[user_id]['setting'].get("regex", None)
  file_name_len = uts[user_id]['setting'].get("file_name_len", None)
  password = uts[user_id]['setting'].get("password", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  if thumb:
    thumb = "True" if not thumb.startswith("http") else thumb

  button = [
    [InlineKeyboardButton("Sᴇᴛ | ᴄʜᴀɴɢᴇ", callback_data="udc_change"), InlineKeyboardButton("Dᴇʟᴇᴛᴇ", callback_data="udc_delete")],
    [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="mus")]
  ]
  if query.data == "udc":
    await retry_on_flood(query.edit_message_reply_markup)(InlineKeyboardMarkup(button))
  elif query.data == "udc_change":
    await retry_on_flood(query.edit_message_caption)("<pre>◈ Sᴇɴᴅ ᴅᴜᴍᴘ ᴄʜᴀɴɴᴇʟ<pre>\n────────────────────────────<b><blockquote>›› Yᴏᴜ ᴄᴀɴ sᴇɴᴅ ᴜsᴇʀɴᴀᴍᴇ (ᴡɪᴛʜᴏᴜᴛ @) ᴏʀ ᴄʜᴀɴɴᴇʟ ɪᴅ ᴏʀ ғᴏʀᴡᴀʀᴅ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴄʜᴀɴɴᴇʟ..</blockquote></b>\n────────────────────────────")
    try:
      call = await _.listen(user_id=int(user_id), timeout=60)
      if call.text:
        dump = call.text
      elif call.forward_from_chat:
        dump = call.forward_from_chat.id

      uts[user_id]['setting']["dump"] = dump
      sync(name, db_type)
      
      txt = users_txt.format(
          id=user_id,
          file_name=file_name,
          caption=caption,
          thumb=thumb,
          banner1=banner1,
          banner2=banner2,
          dump=dump,
          type=type,
          megre=megre,
          regex=regex,
          len=file_name_len,
          password=password,
      )
      if not thumb:
        try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
        except: pass

      await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
      await call.delete()
      await retry_on_flood(query.answer)("Sᴜᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ")
    except asyncio.TimeoutError:
      await retry_on_flood(query.answer)("Tɪᴍᴇᴏᴜᴛ")
    except Exception as err:
      await retry_on_flood(query.answer)(f"{err}", show_alert=True)
  elif query.data == "udc_delete":
    if dump:
      uts[user_id]['setting']["dump"] = None
      sync(name, db_type)
      
      txt = users_txt.format(
        id=user_id,
        file_name=file_name,
        caption=caption,
        thumb=thumb,
        banner1=banner1,
        banner2=banner2,
        dump="None",
        type=type,
        megre=megre,
        regex=regex,
        len=file_name_len,
        password=password,
      )
      if not thumb:
        try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
        except: pass
      
      await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
      await retry_on_flood(query.answer)("Sᴜᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ")
    else:
      await retry_on_flood(query.answer)("Yᴏᴜ ʜᴀs ɴᴏᴛ sᴇᴛ ɪᴛ !", show_alert=True)

  try: await query.answer()
  except: pass

@Bot.on_callback_query(filters.regex("^u_file_type"))
async def type_handler(_, query):
  user_id = str(query.from_user.id)
  if not user_id in uts:
    uts[user_id] = {}
    sync(name, db_type)

    uts[user_id]['setting'] = {}
    sync(name, db_type)

  file_name = uts[user_id]['setting'].get("file_name", None)
  caption = uts[user_id]['setting'].get("caption", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  banner1 = uts[user_id]['setting'].get("banner1", None)
  banner2 = uts[user_id]['setting'].get("banner2", None)
  dump = uts[user_id]['setting'].get("dump", None)
  type = uts[user_id]['setting'].get("type", None)
  megre= uts[user_id]['setting'].get("megre", None)
  regex = uts[user_id]['setting'].get("regex", None)
  file_name_len = uts[user_id]['setting'].get("file_name_len", None)
  password = uts[user_id]['setting'].get("password", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  if thumb:
    thumb = "True" if not thumb.startswith("http") else thumb

  if not "type" in uts[user_id]['setting']:
    uts[user_id]['setting']["type"] = []
    sync(name, db_type)

  type = uts[user_id].get("setting", {}).get("type", [])

  button = [[]]
  if "PDF" in type:
    button[0].append(InlineKeyboardButton("Pᴅғ", callback_data="u_file_type_pdf"))
  else:
    button[0].append(InlineKeyboardButton("Pᴅғ", callback_data="u_file_type_pdf"))
  if "CBZ" in type:
    button[0].append(InlineKeyboardButton("Cʙᴢ", callback_data="u_file_type_cbz"))
  else:
    button[0].append(InlineKeyboardButton("Cʙᴢ", callback_data="u_file_type_cbz"))

  button.append([InlineKeyboardButton("Bᴀᴄᴋ", callback_data="mus")])

  if query.data == "u_file_type":
    await retry_on_flood(query.edit_message_reply_markup)(InlineKeyboardMarkup(button))

  elif query.data == "u_file_type_pdf":
    if "PDF" in type:
      uts[user_id]['setting']["type"].remove("PDF")
      sync(name, db_type)

      button[0][0] = InlineKeyboardButton("Pᴅғ", callback_data="u_file_type_pdf")

    else:
      uts[user_id]['setting']["type"].append("PDF")
      sync(name, db_type)

      button[0][0] = InlineKeyboardButton("Pᴅғ", callback_data="u_file_type_pdf")

    type = uts[user_id].get("setting", {}).get("type", "None")
    txt = users_txt.format(
      id=user_id,
      file_name=file_name,
      caption=caption,
      thumb=thumb,
      banner1=banner1,
      banner2=banner2,
      dump=dump,
      type=type,
      megre=megre,
      regex=regex,
      len=file_name_len,
      password=password,
    )
    if not thumb:
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass

    await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))

  elif query.data == "u_file_type_cbz":
    if "CBZ" in type:
      uts[user_id]['setting']["type"].remove("CBZ")
      sync(name, db_type)

      button[0][1] = InlineKeyboardButton("Cʙᴢ", callback_data="u_file_type_cbz")

    else:
      uts[user_id]['setting']["type"].append("CBZ")
      sync(name, db_type)

      button[0][1] = InlineKeyboardButton("Cʙᴢ", callback_data="u_file_type_cbz")

    type = uts[user_id].get("setting", {}).get("type", "None")
    txt = users_txt.format(
      id=user_id,
      file_name=file_name,
      caption=caption,
      thumb=thumb,
      banner1=banner1,
      banner2=banner2,
      dump=dump,
      type=type,
      megre=megre,
      regex=regex,
      len=file_name_len,
      password=password,
    )
    if not thumb:
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass

    await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))

  try: await query.answer()
  except: pass

@Bot.on_callback_query(filters.regex("^umegre"))
async def megre_handler(_, query):
  user_id = str(query.from_user.id)
  if not user_id in uts:
    uts[user_id] = {}
    sync(name, db_type)

    uts[user_id]['setting'] = {}
    sync(name, db_type)

  file_name = uts[user_id]['setting'].get("file_name", None)
  caption = uts[user_id]['setting'].get("caption", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  banner1 = uts[user_id]['setting'].get("banner1", None)
  banner2 = uts[user_id]['setting'].get("banner2", None)
  dump = uts[user_id]['setting'].get("dump", None)
  type = uts[user_id]['setting'].get("type", None)
  megre= uts[user_id]['setting'].get("megre", None)
  regex = uts[user_id]['setting'].get("regex", None)
  file_name_len = uts[user_id]['setting'].get("file_name_len", None)
  password = uts[user_id]['setting'].get("password", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  if thumb:
    thumb = "True" if not thumb.startswith("http") else thumb
  button = [
    [InlineKeyboardButton("Sᴇᴛ | ᴄʜᴀɴɢᴇ", callback_data="umegre_change"), InlineKeyboardButton("Dᴇʟᴇᴛᴇ", callback_data="umegre_delete")],
    [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="mus")]
  ]
  if query.data == "umegre":
    await retry_on_flood(query.edit_message_reply_markup)(InlineKeyboardMarkup(button))

  elif query.data == "umegre_change":
    if not thumb:
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass
    
    await retry_on_flood(query.edit_message_caption)("<pre>◈ Sᴇɴᴅ ᴍᴇɢʀᴇ sɪᴢᴇ</pre>\n────────────────────────────\n<b><blockquote>›› Iᴛ's ɴᴜᴍʙᴇʀ ғᴏʀ ᴍᴇɢʀᴇ. ɪ.ᴇ 2, 3 ,4 ,5, ᴇᴛᴄ...</blockquote></b>\n────────────────────────────")
    try:
      call = await _.listen(user_id=int(user_id), timeout=60)
      call_int = int(call.text)

      uts[user_id]['setting']["megre"] = call.text
      sync(name, db_type)
      
      megre = call.text 
      await call.delete()
    except ValueError:
      await retry_on_flood(query.answer)("Tʜɪs ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀ", show_alert=True)
    except asyncio.TimeoutError:
      await retry_on_flood(query.answer)("Tɪᴍᴇᴏᴜᴛ")
    except Exception as err:
      await retry_on_flood(query.answer)(f"{err}", show_alert=True)
    
    txt = users_txt.format(
      id=user_id,
      file_name=file_name,
      caption=caption,
      thumb=thumb,
      banner1=banner1,
      banner2=banner2,
      dump=dump,
      type=type,
      megre=megre,
      regex=regex,
      len=file_name_len,
      password=password,
    )
    if not thumb:
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass

    await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
    await retry_on_flood(query.answer)("Sᴜᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ")

  elif query.data == "umegre_delete":
    if megre:
      uts[user_id]['setting']["megre"] = None
      sync(name, db_type)

      txt = users_txt.format(
        id=user_id,
        file_name=file_name,
        caption=caption,
        thumb=thumb,
        banner1=banner1,
        banner2=banner2,
        dump=dump,
        type=type,
        megre="None",
        regex=regex,
        len=file_name_len,
        password=password,
      )

      if not thumb:
        try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
        except: pass

      await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
      await retry_on_flood(query.answer)("Sᴜᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ")
    else:
      await retry_on_flood(query.answer)("Yᴏᴜ ʜᴀs ɴᴏᴛ sᴇᴛ ɪᴛ !", show_alert=True)

  try: await query.answer()
  except: pass

@Bot.on_callback_query(filters.regex("^upass"))
async def password_handler(_, query):
  user_id = str(query.from_user.id)
  if not user_id in uts:
    uts[user_id] = {}
    sync(name, db_type)
    uts[user_id]['setting'] = {}
    sync(name, db_type)

  file_name = uts[user_id]['setting'].get("file_name", None)
  caption = uts[user_id]['setting'].get("caption", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  banner1 = uts[user_id]['setting'].get("banner1", None)
  banner2 = uts[user_id]['setting'].get("banner2", None)
  dump = uts[user_id]['setting'].get("dump", None)
  type = uts[user_id]['setting'].get("type", None)
  megre= uts[user_id]['setting'].get("megre", None)
  regex = uts[user_id]['setting'].get("regex", None)
  file_name_len = uts[user_id]['setting'].get("file_name_len", None)
  password = uts[user_id]['setting'].get("password", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  if thumb:
    thumb = "True" if not thumb.startswith("http") else thumb

  button = [
    [InlineKeyboardButton("Sᴇᴛ | ᴄʜᴀɴɢᴇ", callback_data="upass_change"), InlineKeyboardButton("Dᴇʟᴇᴛᴇ", callback_data="upass_delete")],
    [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="mus")]
  ]

  if query.data == "upass":
    await retry_on_flood(query.edit_message_reply_markup)(InlineKeyboardMarkup(button))
  elif query.data == "upass_change":
    await retry_on_flood(query.edit_message_caption)("<pre>◈ Sᴇɴᴅ ᴘᴀssᴡᴏʀᴅ</pre>\n────────────────────────────\n<b><blockquote>›› Iᴛ's ᴘᴀssᴡᴏʀᴅ ғᴏʀ ᴘᴅғ.</blockquote></b>\n────────────────────────────")
    try:
      call = await _.listen(user_id=int(user_id), timeout=60)
      password = call.text
      
      uts[user_id]['setting']["password"] = password
      sync(name, db_type)
      
      await call.delete()
    except asyncio.TimeoutError:
      await retry_on_flood(query.answer)("Tɪᴍᴇᴏᴜᴛ")
    except Exception as err:
      await retry_on_flood(query.answer)(f"{err}", show_alert=True)
    
    txt = users_txt.format(
      id=user_id,
      file_name=file_name,
      caption=caption,
      thumb=thumb,
      banner1=banner1,
      banner2=banner2,
      dump=dump,
      type=type,
      megre=megre,
      regex=regex,
      len=file_name_len,
      password=password,
    )
    if not thumb:
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass

    await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
    await retry_on_flood(query.answer)("🎼 Sucessfully Added 🎼")

  elif query.data == "upass_delete":
    if password:
      uts[user_id]['setting']["password"] = None
      sync(name, db_type)

      txt = users_txt.format(
        id=user_id,
        file_name=file_name,
        caption=caption,
        thumb=thumb,
        banner1=banner1,
        banner2=banner2,
        dump=dump,
        type=type,
        megre=megre,
        regex=regex,
        len=file_name_len,
        password="None",
      )
      if not thumb:
        try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
        except: pass

      await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
    else:
      await retry_on_flood(query.answer)("Yᴏᴜ ʜᴀs ɴᴏᴛ sᴇᴛ ɪᴛ !", show_alert=True)

  try: await query.answer()
  except: pass

@Bot.on_callback_query(filters.regex("^uregex"))
async def regex_handler(_, query):
  user_id = str(query.from_user.id)
  if not user_id in uts:
    uts[user_id] = {}
    sync(name, db_type)

    uts[user_id]['setting'] = {}
    sync(name, db_type)

  file_name = uts[user_id]['setting'].get("file_name", None)
  caption = uts[user_id]['setting'].get("caption", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  banner1 = uts[user_id]['setting'].get("banner1", None)
  banner2 = uts[user_id]['setting'].get("banner2", None)
  dump = uts[user_id]['setting'].get("dump", None)
  type = uts[user_id]['setting'].get("type", None)
  megre= uts[user_id]['setting'].get("megre", None)
  regex = uts[user_id]['setting'].get("regex", None)
  file_name_len = uts[user_id]['setting'].get("file_name_len", None)
  password = uts[user_id]['setting'].get("password", None)
  thumb = uts[user_id]['setting'].get("thumb", None)
  if thumb:
    thumb = "True" if not thumb.startswith("http") else thumb

  button = [
    [InlineKeyboardButton(i, callback_data=f"uregex_set_{i}") for i in range(1, 5)],
    [InlineKeyboardButton("Dᴇʟᴇᴛᴇ", callback_data="uregex_delete")],
    [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="mus")]
  ]
  if query.data == "uregex":
    await retry_on_flood(query.edit_message_reply_markup)(InlineKeyboardMarkup(button))
  elif query.data.startswith("uregex_set"):
    regex = query.data.split("_")[-1]

    uts[user_id]['setting'][f"regex"] = regex
    sync(name, db_type)

    txt = users_txt.format(
        id=user_id,
        file_name=file_name,
        caption=caption,
        thumb=thumb,
        banner1=banner1,
        banner2=banner2,
        dump=dump,
        type=type,
        megre=megre,
        regex=regex,
        len=file_name_len,
        password=password,
    )
    if not thumb:
      try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
      except: pass

    await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
  elif query.data == "uregex_delete":
    if regex:
      uts[user_id]['setting']["regex"] = None
      sync(name, db_type)

      txt = users_txt.format(
        id=user_id,
        file_name=file_name,
        caption=caption,
        thumb=thumb,
        banner1=banner1,
        banner2=banner2,
        dump=dump,
        type=type,
        megre=megre,
        regex="None",
        len=file_name_len,
        password=password,
      )
      if not thumb:
        try: await query.edit_message_media(InputMediaPhoto(random.choice(Vars.PICS)))
        except: pass

      await retry_on_flood(query.edit_message_caption)(txt, reply_markup=InlineKeyboardMarkup(button))
    else:
      await retry_on_flood(query.answer)("Yᴏᴜ ʜᴀs ɴᴏᴛ sᴇᴛ ɪᴛ !", show_alert=True)


