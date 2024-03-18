import requests
# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6934287768:AAGhxy-yrKIyhD4eOzgakBMivGfps64Ddt'
group_chat_id = -1001949259483
message = 'helo'

#change these chatids to be parameters later
aswin_chat_id = 5151689696
herschelle_chat_id = 7184297938
priyansh_chat_id = 6090055937
shubh_chat_id = 1406495803
anmol_chat_id = 1312559056
krishna_chat_id = 905819833

baseURL = 'https://api.telegram.org/bot6934287768:AAGhxy-yrKIyhD4eOzgakBMivGfps64Ddtk/sendMessage?chat_id=' #+str(aswin_chat_id)+'&text='+message

mapping = {
    'herschelle': herschelle_chat_id,
    'aswin': aswin_chat_id,
    'priyansh': priyansh_chat_id,
    'shubh': shubh_chat_id,
    'anmol': anmol_chat_id,
    'krishna': krishna_chat_id
}

def sendTelegramMessage(nameList:list[str], message:str):
    print("here")
    for name in nameList:
        chat_id = mapping[name.lower().strip()]
        message = '&text='+message
        success = requests.get(baseURL+str(chat_id)+message)
        print(success)