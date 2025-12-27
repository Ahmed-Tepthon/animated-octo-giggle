import time, os, json, re, requests, asyncio, logging
from pyrogram import Client, filters, idle, enums
from redis_mock import RedisMock

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

r = RedisMock()

to_config = """
from redis_mock import RedisMock
r = RedisMock()
"""

token = '8564243133:AAEx8UTZKQOxtAr2jMRDkFCsjivv-aiLuiQ'
owner_id = 8087077168
Dev_Zaid = token.split(':')[0]

# Pre-set critical data
r.set(f'{Dev_Zaid}botowner', str(owner_id))
r.set(f'{Dev_Zaid}:botkey', '⇜')
r.set(f'{Dev_Zaid}botname', 'Dark')

to_config += f"\ntoken = '{token}'"
to_config += f"\nDev_Zaid = token.split(':')[0]"
to_config += f"\nsudo_id = {owner_id}"
try:
    username = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()["result"]["username"]
    to_config += f"\nbotUsername = '{username}'"
except:
    to_config += f"\nbotUsername = 'DarkTepbot'"

to_config += "\nfrom kvsqlite.sync import Client as DB"
to_config += "\nytdb = DB('ytdb.sqlite')"
to_config += "\nsounddb = DB('sounddb.sqlite')"
to_config += "\nwsdb = DB('wsdb.sqlite')"

with open('config.py','w+') as w:
    w.write(to_config)

app = Client(
    f'{Dev_Zaid}r3d', 
    api_id=38699092, 
    api_hash='480f2b2d941c5c49ddc34e6d8c5db3fd',
    bot_token=token,
    plugins={"root": "Plugins"},
)

@app.on_message(filters.all, group=-2000)
async def debug_all(c, m):
    try:
        logger.info(f"!!! DEBUG !!! Process message: {m.text or '[No Text]'} | From: {m.from_user.id if m.from_user else 'unknown'}")
        
        # Emergency bypass for all group locks/checks
        if m.chat and m.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            r.set(f'{m.chat.id}:enable:{Dev_Zaid}', "True")
            r.delete(f'{m.chat.id}:mute:{Dev_Zaid}')
            if m.from_user:
                r.delete(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}')
                r.delete(f'{m.from_user.id}:mute:{Dev_Zaid}')
                if m.from_user.id == owner_id:
                    r.set(f'{m.chat.id}:rankADMIN:{m.from_user.id}{Dev_Zaid}', "True")
        
        if m.text == "/test":
            await m.reply("البوت شغال وبيرد على الديباج!")
            return m.stop_propagation()
        
        if m.text == "تفعيل":
            r.set(f'{m.chat.id}:enable:{Dev_Zaid}', "True")
            await m.reply("تم تفعيل المجموعة بنجاح!")
            return m.stop_propagation()
            
        if m.text == "ايدي":
            await m.reply(f"ايديك: {m.from_user.id}")
            return m.stop_propagation()
            
    except Exception as e:
        logger.error(f"Error in debug_all: {e}")
        
    return m.continue_propagation()

@app.on_message(filters.private & filters.command("start"), group=-1500)
async def start_priv(c, m):
    pass

async def start_bot():
    logger.info("Starting bot...")
    
    # Start a dummy web server for Render's web service requirement
    from aiohttp import web
    async def hello(request):
        return web.Response(text="Bot is running!")
    
    app_web = web.Application()
    app_web.add_routes([web.get('/', hello)])
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    asyncio.create_task(site.start())
    logger.info(f"Web server started on port 8000")

    await app.start()
    logger.info(f"Bot started as @{app.me.username}")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
