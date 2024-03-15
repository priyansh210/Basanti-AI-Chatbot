import requests
# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6934287768:AAGhxy-yrKIyhD4eOzgakBMivGfps64Ddt'
group_chat_id = -1001949259483
message = 'helo'

#change these chatids to be parameters later
aswin_chat_id = 5151689696
herschelle_chat_id = 7184297938


baseURL = 'https://api.telegram.org/bot6934287768:AAGhxy-yrKIyhD4eOzgakBMivGfps64Ddtk/sendMessage?chat_id=' #+str(aswin_chat_id)+'&text='+message

mapping = {
    'herschelle': herschelle_chat_id,
    'Herschelle': herschelle_chat_id,
    'aswin': aswin_chat_id,
    'Aswin': aswin_chat_id
}

def sendTelegramMessage(nameList:list[str], message:str):
    for name in nameList:
        
        requests.get(baseURL)