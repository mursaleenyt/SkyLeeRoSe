import speedtest
import requests
import datetime
import platform
import time

from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
from platform import python_version
from telegram import __version__
from spamwatch import __version__ as __sw__
from pythonping import ping as ping3
from telegram import Message, Chat, Update, Bot, MessageEntity
from datetime import datetime
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from skylee import dispatcher, OWNER_ID
from skylee.modules.helper_funcs.filters import CustomFilters
from skylee.modules.helper_funcs.alternate import typing_action
from skylee.modules.helper_funcs.alternate import send_message


@run_async
@typing_action
def ping(update, context):
	start_time = time.time()
	test = send_message(update.effective_message, "Pong!")
	end_time = time.time()
	ping_time = float(end_time - start_time)
	context.bot.editMessageText(chat_id=update.effective_chat.id, message_id=test.message_id,
						text=tl(update.effective_message, "Pong!\nKecepatannya: {0:.2f} detik").format(round(ping_time, 2) % 60))

#Kanged from PaperPlane Extended userbot
def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2**10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"

@run_async
@typing_action
def get_bot_ip(update, context):
    """ Sends the bot's IP address, so as to be able to ssh in if necessary.
        OWNER ONLY.
    """
    res = requests.get("http://ipinfo.io/ip")
    update.message.reply_text(res.text)



@run_async
@typing_action
def speedtst(update, context):
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    update.effective_message.reply_text("Download "
                   f"{speed_convert(result['download'])} \n"
                   "Upload "
                   f"{speed_convert(result['upload'])} \n"
                   "Ping "
                   f"{result['ping']} \n"
                   "ISP "
                   f"{result['client']['isp']}")


@run_async
@typing_action
def system_status(update, context):
    uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    status = "<b>======[ SYSTEM INFO ]======</b>\n\n"
    status += "<b>System uptime:</b> <code>"+str(uptime)+"</code>\n"

    uname = platform.uname()
    status += "<b>System:</b> <code>"+str(uname.system)+"</code>\n"
    status += "<b>Node name:</b> <code>"+str(uname.node)+"</code>\n"
    status += "<b>Release:</b> <code>"+str(uname.release)+"</code>\n"
    status += "<b>Version:</b> <code>"+str(uname.version)+"</code>\n"
    status += "<b>Machine:</b> <code>"+str(uname.machine)+"</code>\n"
    status += "<b>Processor:</b> <code>"+str(uname.processor)+"</code>\n\n"

    mem = virtual_memory()
    cpu = cpu_percent()
    disk = disk_usage('/')
    status += "<b>CPU usage:</b> <code>"+str(cpu)+" %</code>\n"
    status += "<b>Ram usage:</b> <code>"+str(mem[2])+" %</code>\n"
    status += "<b>Storage used:</b> <code>"+str(disk[3])+" %</code>\n\n"
    status += "<b>Python version:</b> <code>"+python_version()+"</code>\n"
    status += "<b>Library version:</b> <code>"+str(__version__)+"</code>\n"
    status += "<b>Spamwatch API:</b> <code>"+str(__sw__)+"</code>\n"
    context.bot.sendMessage(update.effective_chat.id, status, parse_mode=ParseMode.HTML)


IP_HANDLER = CommandHandler("ip", get_bot_ip, filters=Filters.chat(OWNER_ID))
PING_HANDLER = CommandHandler("ping", ping, filters=CustomFilters.sudo_filter)
SPEED_HANDLER = CommandHandler("speedtest", speedtst, filters=CustomFilters.sudo_filter) 
SYS_STATUS_HANDLER = CommandHandler("sysinfo", system_status, filters=CustomFilters.sudo_filter)

dispatcher.add_handler(IP_HANDLER)
dispatcher.add_handler(SPEED_HANDLER)
dispatcher.add_handler(PING_HANDLER)
dispatcher.add_handler(SYS_STATUS_HANDLER)
