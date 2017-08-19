# -*- coding: UTF-8 -*-
import vk_api
import random
import time
import threading
from gtts import gTTS
import os
from valdismarkov import *
import datetime
import pdb
print("VK API loaded!")
spampoint = 0
bannedusers = open("banned.txt", "r")
adminusers = ["405452698", "300236994", "140028817"]
bannedword = ["https://", "/", "http://", "://", ".com", ".ru", ".ch", ".tk", "vk", "@", "/", "шизик шизофазия", "[", "]", "id", "|"]
banusers = bannedusers.read()
banusers = banusers.split(", ")
bannedusers.close()
curtime = datetime.datetime.now()
curseconds = (curtime-datetime.datetime(1970,1,1)).total_seconds()
from vk_api.longpoll import VkLongPoll, VkEventType
def antispam():
    global spampoint
    spampoint = 0
    threading.Timer(10, antispam).start()
    antispam()
antispam()
def auth_handler():
    vladikkey = input("Введи код)))))): ")
    remember_device = True

    return vladikkey, remember_device

def main():
    global banusers
    global adminusers
    global spampoint
    login, password = "79851081623", "MemeFox123"
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    vk = vk_session.get_api()
    
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if spampoint < 3:
                if event.text.lower() == "шизик добавь меня":
                    friendget = vk.friends.areFriends(user_ids=event.user_id)
                    friendare = friendget[0]
                    friendare = friendare['friend_status']
                    if friendare == 3:
                        vk.messages.send(peer_id=event.peer_id, message="я же тебя добавил!")
                    elif friendare == 2:
                        vk.messages.send(peer_id=event.peer_id, message="ща =)")
                        vk.friends.add(user_id=event.user_id)
                    else:
                        vk.messages.send(peer_id=event.peer_id, message="кинь заявку потом еще раз попробуй)")
                if event.text.lower() == "шизик ping":
                    vk.messages.send(peer_id=event.peer_id, message="pong") 
                elif event.text.lower() == "шизик админы":
                    admingstring = ""
                    for a in adminusers:
                        adminstring = adminstring + a + " "
                    vk.messages.send(peer_id=event.peer_id, message="админы: " + adminusers)
                elif event.text.lower() == "шизик помощь":
                    vk.messages.send(peer_id=event.peer_id, message="---START---\nшизик бот v1.0\ntype: BETA\ncodename: VALDIS\nprefix: шизик\nКоманды:\nшизофазия - бред шизика (слова он черпает от вас!)\nшизофазия вслух - голос шизика! (тоже самое что и шизофазия но в виде голосового сообщения)\nдобавь меня - бот вас добавить (сначала киньте заявку)\nдонат - все деньги идут на хостинг! а еще вас пропустят в рай без очереди ;)\n---END---")
                elif event.text.lower() == "шизик донат":
                    vk.messages.send(peer_id=event.peer_id, message="Если у тебя есть желание задонатить то:\nhttp://www.donationalerts.ru/r/feelatkeen")
                elif "шизик шизофазия: " in event.text.lower(): 
                    vk.messages.send(peer_id=event.peer_id, message='шизик шизофазия через двоеточие machine broke')
                elif event.text.lower() == "шизик шизофазия помощь":
                    vk.messages.send(peer_id=event.peer_id, message="бот набирается слов от вас и несет хуйню")
                elif "шизик шиз" in event.text.lower():
                    loadwordlist = open("shiza.txt", "r+")
                    wordstring = loadwordlist.read().lower()
                    loadwordlist.close()
                    if wordstring == "":
                        vk.messages.send(peer_id=event.peer_id, message="п-п-п-простите я знаю м-м-мало с-слов... п-п-просто общайтесь а я б-б-буду учиться... надеюсь я вас не р-р-расстроил.....")
                    else:
                        wordlist = wordstring.split()
                        worddict = dict([(wordlist[i], wordlist[i+1]) for i in range(0, len(wordlist) - 1, 2) ])
                        shizalength = random.randint(0,20)
                        sent_model = build_chain(wordlist)
                        shizasent = generate(sent_model, shizalength)
                        if shizasent == "" or shizasent == " ":
                            vk.messages.send(peer_id=event.peer_id, message="простите пожалуйста, я не знаю что сказать. попробуйте еще раз. извините за доставленные неудобства")
                        else:
                            shizasent = shizasent.replace("&quot;", '')
                            shizasent = shizasent.replace("&amp;", "")
                            shizasent = shizasent.replace("&gt;", ">")
                            shizasent = shizasent.replace("end", "")
                            shizasent = shizasent.lower()
                            print("shizasent = " + shizasent + ".")
                            if event.text.lower() == "шизик шизофазия":
                                vk.messages.send(peer_id=event.peer_id, message=shizasent)
                                try:
                                    global curseconds
                                    curseconds = curseconds + 30 * 60
                                    vk.wall.post(owner_id="-151495280", message=shizasent, publish_date=curseconds)
                                except:
                                    curseconds = curseconds + 24 * 60 * 60
                                    pass
                            if event.text.lower() == "шизик шизофазия вслух":
                                shizasent = gTTS(text=shizasent, lang='ru', slow=False)
                                shizasent.save("shiza.mp3")
                                upload = vk_api.VkUpload(vk_session)
                                sentprikol = upload.audio_message(
                                    os.path.dirname(os.path.realpath(__file__)) + "/shiza.mp3"
                                    )
                                print(sentprikol)
                                vk.messages.send(peer_id=event.peer_id, attachment="doc"+str(sentprikol[0]['owner_id'])+ "_" + str(sentprikol[0]['id']))
                                
                elif event.text.lower() == "шизик выпей амнезиак":
                    if event.user_id in adminusers:
                        vk.messages.send(peer_id=event.peer_id, message="*выпил*")
                        loadwordlist = open("shiza.txt", "w")
                        loadwordlist.write("")
                        loadwordlist.close()
                    else:
                        print(event.user_id)
                        vk.messages.send(peer_id=event.peer_id, message="иди нахуй!!!")
                elif event.text.lower() == "шизик ебани себе по голове":
                    if event.user_id in adminusers:
                        vk.messages.send(peer_id=event.peer_id, message="*ебанул*")
                        loadwordlist = open("shiza.txt", "r+")
                        prikolwordlist = loadwordlist.read()
                        loadwordlist.close()
                        todelete = ["а", "о", "е", "ё", "у"]
                        for delthing in todelete:
                            if delthing in prikolwordlist:
                                prikolwordlist = prikolwordlist.replace(delthing, "")
                        editwordlist = open("shiza.txt", "w+")
                        editwordlist.write(prikolwordlist)
                        editwordlist.close()
                    else:
                        print(event.user_id)
                        vk.messages.send(peer_id=event.peer_id, message="иди нахуй!!!")
                elif "шизик забудь:" in event.text.lower():
                    if event.user_id == "320502491":
                        vk.messages.send(peer_id=event.peer_id, message="что это значит?")
                        loadwordlist = open("shiza.txt", "r+")
                        prikolwordlist = loadwordlist.read()
                        loadwordlist.close()
                        prikolwordlist = prikolwordlist.replace(event.text.lower().replace("шизик забудь: ", ""), "")
                        editwordlist = open("shiza.txt", "w+")
                        editwordlist.write(prikolwordlist)
                        editwordlist.close()
                    else:
                        print(event.user_id)
                        vk.messages.send(peer_id=event.peer_id, message="иди нахуй!!!")
                elif "шизик убить " in event.text.lower():
                    usercmd = event.text.lower().replace("шизик убить ", "")
                    if event.user_id in adminusers:
                        vk.messages.send(peer_id=event.peer_id, message="[id" + usercmd + "|шайтан] убить")
                        banread = open("banned.txt", "r")
                        banusers = banread.read()
                        banread.close()
                        banwrite = open("banned.txt", "w")
                        banwrite.write(banusers + usercmd + ", ")
                        banwrite.close()
                        banread = open("banned.txt", "r")
                        banusers = banread.read()
                        banusers.split(", ")
                        banread.close()
                    else:
                        vk.messages.send(peer_id=event.peer_id, message="иди нахуй!!!")
                elif "шизик воскреси " in event.text.lower():
                    usercmd = event.text.lower().replace("шизик воскреси ", "")
                    if event.user_id in adminusers:
                        vk.messages.send(peer_id=event.peer_id, message="[id" + usercmd + "|нешайтан] восресить")
                        banread = open("banned.txt", "r")
                        banusers = banread.read()
                        banusers = banusers.replace(usercmd + ", ", "")
                        banread.close()
                        banwrite = open("banned.txt", "w")
                        banwrite.write(banusers)
                        banwrite.close()
                        banread = open("banned.txt", "r")
                        banusers = banread.read()
                        banusers.split(", ")
                        banread.close()
                    else:
                        vk.messages.send(peer_id=event.peer_id, message="иди нахуй!!!")
                else:
                    if str(event.user_id) in banusers or event.user_id == "441815332" or any(ext in event.text for ext in bannedword):
                        print(event.user_id + " ignore!")
                    else:
                        try:
                            prikoltexta = event.text.lower().split(" ")
                            readwordlist = open("shiza.txt", "r")
                            savedtext = readwordlist.read()
                            readwordlist.close()
                            if len(prikoltexta) < 500:
                                savedtext = savedtext.replace(",\n", " ")
                                savedtext = savedtext.replace("\n", " ")
                                savedtext = savedtext.replace(",", " ")
                                loadwordlist = open("shiza.txt", "w")
                                loadwordlist.write(savedtext + event.text.lower() + " END ")
                                loadwordlist.close()
                            else:
                                vk.messages.send(peer_id=event.peer_id, message="слишком много слов!!!! я не понимаю!!!!!!!!!!!!!!!!")
                        except:
                            loadwordlist = open("shiza.txt", "w")
                            loadwordlist.write(savedtext)
                            loadwordlist.close()
                            pass
                
                

if __name__ == '__main__':
    main()
