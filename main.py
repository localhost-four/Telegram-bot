
import os

os.system('pip install telebot')
os.system('pip install climage')
os.system('pip install pymorphy2')
os.system('pip install psutil')
os.system('pip install re')
os.system('pip install sys')
os.system('pip install re')
os.system('pip install random')
os.system('pip install traceback')

import telebot
import re
import random
import time
import sys
import climage
import pymorphy2
from telebot import types
import traceback

morph = pymorphy2.MorphAnalyzer()

global Hash
Hash = ['<', '#', '>']

h = 1
lim_1 = 1

#SYSTEM CONTROLL
sys_names = [os.getenv, os.environ, os.error, os.name, os.getcwd()]
for i in sys_names:
  if not i == None and not i == '' and not i == ' ':
    try:
      Hash.extend(i)
      print(f'[+] {len(i)}')
    except:
      pass
os.system("cls")
key = os.environ['token_key']
client = telebot.TeleBot(str(key))

print(str(client.get_me()))

import requests


while True:
  try:

    def install(url):
      from urllib.request import urlopen
      from bs4 import BeautifulSoup
      H8 = [None]
      try:
          html = urlopen(url).read()

          soup = BeautifulSoup(html, features="html.parser")

          # kill all script and style elements
          for script in soup(["script", "style"]):
              script.extract()    # rip it out


          # get text
          text = soup.get_text()
          text = text[:8200]

          # break into lines and remove leading and trailing space on each
          lines = (line.strip() for line in text.splitlines())
          # break multi-headlines into a line each
          chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
          # drop blank lines
          #text = '\n'.join(chunk for chunk in chunks if chunk)

          Hash.extend(chunk for chunk in chunks if chunk)

          return f'{text} \n \n #include > bit {len(text)}'
      except:
          try:
              import requests
              r = requests.get(url)
              if r.status_code == 200:
                  # get the response text. in this case it is HTML
                  html = r.text

                  # parse the HTML
                  soup = BeautifulSoup(html, "html.parser")

                  text = soup.body.get_text().strip()
                  text = text[:8200]
                  # print the HTML as text
                  Hash.extend(text)

                  return f'{text} \n \n #get > bit {len(text)}'

              else:
                  return None
          except: return None

    def extract_links(text1):
      links = []
      for word in text1:
          match = re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', word)
          if match:
              links.append(match.group())
      return links
    
    def create_req(text1):
      links = extract_links(text1)
      print(links)
      if links:
        text = []
        for link in links:
          text.append(install(link))
        
        return text
      
      else:
        result = '+'.join(''.join(word.split()) for word in text1)
        print(result)
        return install(f'https://www.google.com/search?q={result}')
    
    def send_react(chat_id, message_id, token):
      
      emo = ["🔥", "🤗", "😎"]
      url = f'https://api.telegram.org/bot{TOKEN}/setMessageReaction'
      data = {
          'chat_id': chat_id,
          'message_id': message_id,
          'reaction': [
              {
                  'type': 'emoji',
                  #'emoji': '🔥' # Обычный вариант с одним смайлом.
                  'emoji': choice(emo) # Вариант со списком из смайликов.
              }
          ],
          'is_big': False
      }
      response = requests.post(url, json=data)
      result = response.json()
      
    
    def get_updates(token):
      url = f"https://api.telegram.org/bot{token}/getUpdates"
      response = requests.get(url)
  
      if response.status_code == 200:
          data = response.json()
          if data['ok'] == True:
              updates = data['result']
              for update in updates:
                try:
                  chat_id = update['message']['chat']['id']
                  text = update['message']['text']
                  return f"Chat ID: {chat_id}, Message: {text}"
                except: pass
                  
      return None

    print(get_updates(os.environ['token_key']))
    
    def decode_text(text):
    
      try:
        decoded_text = text.encode('latin1', errors='ignore')
  
        decoded_text = decoded_text.decode('utf-8', errors='ignore')
      
        decoded_text = decoded_text.decode('cp1252', errors='ignore')

        if len(decoded_text) >= 1:
          return decoded_text
        else: 
          return text
      except:
        return text

    @client.message_handler(commands=['bump'])
    def broadcast(message):
        markup = types.ForceReply(selective=False)

        # Получаем информацию о каждом пользователе
        users = client.get_updates()
        for user in users:
            if user.message:
                chat_id = user.message.chat.id
                try:  
                    client.send_message(chat_id, f'Topics: \n [+] {str(list(Hash[::-1])[:18])}', reply_markup=markup, parse_mode="Markdown")
                except Exception as e:
                    print(f"Error sending message to {chat_id}: {str(e)}")

    @client.chat_join_request_handler()
    @client.message_handler(commands=['new'])
    def greeting(message):

      try:
        client.reply_to(message.chat.id,
                        f'Topics: \n [+] {str(list(Hash[::-1])[:18])}')
      except:
        client.send_message(message.chat.id,
                            f'Topics: \n [+] {str(list(Hash[::-1])[:18])}', parse_mode="Markdown")
    

    @client.callback_query_handler(func=lambda call: True)
    @client.message_handler(commands=['start', 'help'])
    def start(message: telebot.types.Message):
      bot_username = client.get_me().username

      
      
      client.set_my_commands(commands=[
          types.BotCommand(command='start', description='register user'),
          types.BotCommand(command='help', description='show commands list'),
          types.BotCommand(command='new', description='list top'),
          types.BotCommand(command='id', description='show profile'),
          types.BotCommand(command='bump', description='update chats'),
          types.BotCommand(command='invite', description='list of active'),
          types.BotCommand(command='vote', description='vote for one of the answer options')
      ])
      
        
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

      btn1 = types.KeyboardButton('/new')
      btn2 = types.KeyboardButton('/id')
      btn3 = types.KeyboardButton('/help')

      markup.add(btn1, btn2, btn3)

      
      try:
        client.reply_to(message,
                        f"Welcome, we are waiting for your messages... ",
                        reply_markup=markup, parse_mode="Markdown")
      except:
        client.send_message(message,
                            f"Welcome, we are waiting for your messages... ",
                            reply_markup=markup, parse_mode="Markdown")
  
      get = get_updates(os.environ['token_key'])
      
      if None in get:
        try:
          client.reply_to(message,
                          "There are no missed messages on the server", parse_mode="Markdown")
        except:
          client.send_message(message,
                             "There are no missed messages on the server", parse_mode="Markdown")
      else:
        try:
          client.reply_to(message,
                          "last request: " + str(get), parse_mode="Markdown")
        except:
          client.send_message(message,
                             "last request: " + str(get), parse_mode="Markdown")
        
  
        

      markup = types.InlineKeyboardMarkup()

      btn_new = types.InlineKeyboardButton(text='Copy Text', url=f'https://t.me/share/url?url=' + f'Topics: \n [+] {str(list(Hash[::1])[:12])}')

      markup.add(btn_new)
      
      try:
        try:
          all_users = client.get_chat_members(message.chat.id)  # Получаем список всех участников чата
        except:
          all_users = client.get_chat_members(message)
    
        for user in all_users:
          try:
            client.send_message(user.user.id,
                                f'Topics: \n [+] {str(list(Hash[::1])[:28])}', reply_markup=markup, parse_mode="Markdown")  # Отправляем сообщение каждому участнику
          except:
            try:
              client.send_message(user,
                                  f'Topics: \n [+] {str(list(Hash[::1])[:28])}', reply_markup=markup, parse_mode="Markdown")
            except:
              pass
    
      except:
        pass
    
      try:
        chats = client.get_updates()
    
        for chat in chats:
          try:
            client.send_message(user.user.id,
                                f'Topics: \n [+] {str(list(Hash[::-1])[:3])}', reply_markup=markup)  # Отправляем сообщение каждому участнику
          except:
            try:
              client.send_message(user,
                                  f'Topics: \n [+] {str(list(Hash[::-1])[:3])}', reply_markup=markup, parse_mode="Markdown")
            except:
              pass
      except:
        pass
  
    
    @client.message_handler(commands=["id"])
    def add_channel_handler(message):
      # Разделяем текст на username или link
    
      parts = message.text.split()
      if len(parts) < 2:
        parts = [message.chat.id]
      else:
        del parts[0]
    
      chat = str(client.get_chat(max(parts)))  #.lower
      try:
        client.reply_to(message.chat.id, str(chat), parse_mode="Markdown")
      except:
        client.send_message(message.chat.id, str(chat), parse_mode="Markdown")  
    
    @client.inline_handler(lambda query: len(query.query) > 0)
    def query_text(inline_query):
        keyboard = []
      
        for code in ['hello', 'bye']:
            
            try:
                keyboard.append(telebot.type(code, f'{code}', telebot.types.InputTextMessageContent(f'{code}')))
            except: pass
          
            try:
                client.answer_inline_query(inline_query.id, keyboard)#, is_personal=True)
            except Exception as e:
              print(f"Err_sys: {e}")
    
      
        for code in list(Hash[::-1])[:32]:
            
            try:
                keyboard.append(telebot.types.InlineQueryResultArticle(code, f'{code}', telebot.types.InputTextMessageContent(f'{code}')))
            except: pass
        
            try:
                client.answer_inline_query(inline_query.id, keyboard)#, is_personal=True)
            except: pass

    try:
      client.remove_webhook()
    except: pass

    @client.message_handler(commands=['vote'])
    def vote(message):
      try:
        options = ['Cool', 'Normal', 'Bad']
        client.send_poll(message.chat.id, 'Vote for one of the answer options:', options)
      except: pass


    @client.message_handler(content_types = ['text'])
    def text(message):
        chat_id = message.chat.id
        message_id = message.message_id

        send_react(chat_id, message_id) # Обращение к функции send_react()
    
    
    @client.message_handler(commands=['invite'])
    def invite(message):
        try:
          invite_link = client.export_chat_invite_link(message.chat.id)
        except:
          try:
            invite_link = client.get_chat_invite_link(message.chat.id)
          except: 
            invite_link = f'https://t.me/{client.get_me().username}?text=/invite'

        invite_text = "  Invitation list: "
        try:
          
          chat_id = message.chat.id
          invites = client.get_chat_administrators(chat_id)
          for invite in invites:
            try:
              invite_text += f"  User: {invite.user.username}"
            except: pass
  
          invite_text += f" Other: {client.get_chat_members_count(chat_id)}"
        except: 
          for i in [message.from_user.id, message.chat.id]:
            try:
              invite_text += client.get_chat(i)
            except: pass
          
            
  
        markup = types.InlineKeyboardMarkup()
        try:
          webApp = types.WebAppInfo(invite_link)
          btn_new = types.InlineKeyboardButton(text='Open in', web_app=webApp)
        except: 
          btn_new = types.InlineKeyboardButton(text='Open in', url=invite_link)
  
        markup.add(btn_new)
      
        try:
          client.reply_to(message, str(invite_text), reply_markup=markup, parse_mode="Markdown")
        except:
          client.send_message(message, str(invite_text), reply_markup=markup, parse_mode="Markdown")  
    
    @client.message_handler()  #func=lambda message: True)
    def echo(message):
      try:
        Hash.extend(client.get_channel(message.chat.id))
      except: pass
      
      try: 
        send_react(message.chat.id, message.message_id, os.environ['token_key'])
      except: pass

      try:
        for messages in client.get_chat_history(message.chat.id, limit=8):
          Hash.extend(messages.text)
      except: pass
      
      try:
        invite_link = client.export_chat_invite_link(message.chat.id)
      except:
        try:
          invite_link = client.get_chat_invite_link(message.chat.id)
        except: 
          invite_link = f'https://t.me/{client.get_me().username}'


      
      try:
        messages = client.read_all_group_messages(message.chat.id)
        for msg in messages:
          Hash.extend(msg.text)
      except:
        pass

      try:
        H = str(client.get_chat_description(chat_id))
        Hash.extend(str(H).split())
      except: pass

      try:
        H = str(client.get_me()).lower()
        Hash.extend(str(H).split())
      except: pass

      try:
        H = str(
            client.get_chat_member(chat_id=message.chat.id,
                                   user_id=message.from_user.id)).lower()
        Hash.extend(str(H).split())
      except: pass

      try:
        H = str(client.get_chat(message.chat.id)).lower()
        Hash.extend(str(H).split())
      except: pass

      
      
      import psutil
      for pid in Hash:
        try:
          # Получите объект процесса для указанного идентификатора процесса
          process = psutil.Process(pid)
    
          # Получите строку профиля пользователя
          profile_string = process.cmdline()
    
          # Разделите строку профиля пользователя на отдельные слова
          words = profile_string.split()
          Hash.extend(str(words).split())
        except:
          pass

      def read_blacklist(file_name):
        try:
            with open(file_name, 'r') as file:
                blacklist = file.readlines()  # Читаем файл и разбиваем по строкам

            return blacklist
        except:
            return []
      
      H8 = []
      try:
        H8.extend(read_blacklist('blackword.txt'))
      except: pass

      try:
        H8.extend(read_blacklist('bad_word.txt'))
      except: pass

      text = str(message.text.lower())
      do = True
      for i in H8:
        if str(i.lower()) in text:
          print('OK')

          try: client.send_message(message.chat.id, f"User {message.from_user.username} uses invalid words")
          except: pass
          
          try:
            client.delete_message(message.chat.id, message.message_id)
          except: pass

          try: 
            client.kick_chat_member(message.chat.id, message.from_user.id)
          except: pass

          try:
            client.restrict_chat_member(message.chat.id, message.from_user.id, until_date=60)
          except: pass
          
          try:
            for admin in client.get_chat_administrators(message.chat.id):
              try: client.send_message(admin, f"User {message.from_user.username} uses invalid words")
              except: pass
          except:             
            try: client.leave_chat(message.chat.id)
            except: pass
              
          try: client.idle()
          except: pass

          do = False
          break
        
       

      if do:    
        #AI - Printer
        try:
          j2 = ''
          j1 = []
          text1 = []
          text1 = text.split()
      
          glob = False
          pull = False
          setx = False
      
          #del text1[0]
          try:
            lim_1 = len(min(text1))
          except:
            try:
              lim_1 = len(max(text1)) / 2
            except:
              lim_1 = len(text1) / 2
      
          if round(int(lim_1)) <= 1:
            try:
              lim_1 = len(max(text1)) / 2
            except:
              lim_1 = len(text1) / 2
      
          if len(text1) >= 800:
            del text1[:400]
      
          for i in text1:
            while text1.count(
                i
            ) > 1 or i == None or i == '' or i == ' ' or fr"\[^\s]+" in i or not i == 'none':
              try:
                text1.remove(i)
              except:
                text1.append(i)
                break
      
          while round(int(lim_1)) <= 10:
      
            try:
              client.send_chat_action(message.chat.id, 'typing')
            except:
              pass
      
            lim_1 = round(lim_1 + 1)
      
            if round(int(lim_1)) >= 60:
              break
      
            if 'fix' in text1:
              text1.remove('fix')
              text = ' '.join(text1)
      
            if 'glob' in text1:
              text1.remove('glob')
              glob = True
      
            if 'pull' in text1:
              text1.remove('pull')
              pull = True
      
            if 'set' in text1:
              text1.remove('set')
              setx = True
      
            #install
            #print(h ,'/1000')
      
            if len(j1) >= 1 or round(int(lim_1)) >= 60 or not round(int(lim_1)) > 0:
              break
            else:
              for lim_number in range(len(max(text1)) + 1, round(lim_1 - 1)):
                for j in Hash:
                  j0 = str(j[0:lim_number]).lower()
                  try:
                    if glob:
                      sum1 = set(j) & set(text)
                      sum2 = set(j0) & set(text)
                    else:
                      sum1 = []
                      sum2 = []
      
                    if len(sum1) > lim_number or len(sum2) > lim_number or str(
                        j0) in text or str(j0) in text1 or str(
                            j) in text1 or text1.count(str(j)) > 0 or text1.count(
                                str(j0)) > 0:
                      if len(j) > 1 and not j1.count(j) > 0 and not j1.count(j0) > 0:
                        j2 = re.findall(fr'({j0}[^\s]+)', text)
                        if len(j) < len(j2) and not len(j2) == len(
                            text1) and not j2 == text1 or len(j2) > 0:
                          j1.extend(j2)
                        else:
                          j1.append(j)
      
                  except:
                    pass
      
                  ai = []
                  ai.extend(re.findall(fr"|".join(map(re.escape, j)), text))
                  ai.extend(re.findall(fr"|".join(map(re.escape, j0)), text))
      
                  for i in ai:
                    while ai.count(i) > 1 or i == None or i == '' or i == ' ':
                      try:
                        ai.remove(i)
                      except:
                        ai.append(i)
                        break
      
                  if len(ai) >= 1:
                    for lim_number in range(0,
                                            len(max(text1)) + 1 or round(lim_1 - 1)):
                      for i in ai:
                        j0 = str(i[0:lim_number]).lower()
                        try:
                          if glob:
                            sum1 = set(i) & set(text)
                            sum2 = set(j0) & set(text)
                          else:
                            sum1 = []
                            sum2 = []
      
                          if len(sum1) > lim_number or len(sum2) > lim_number or str(
                              j0) in text or str(
                                  j0) in text1 or str(i) in text1 or text1.count(
                                      str(i)) > 0 or text1.count(str(j0)) > 0:
                            if len(i) > 1 and not j1.count(i) > 0 and not j1.count(
                                j0) > 0:
                              j2 = re.findall(fr'({j0}[^\s]+)', text)
                              #print(j2)
                              if len(i) < len(j2) and not len(j2) == len(
                                  text1) and not j2 == text1 or len(j2) > 0:
                                j1.extend(j2)
                              else:
                                j1.append(i)
                        except:
                          pass
      
        #FILE OPEN
            if len(j1) >= 1 or round(int(lim_1)) >= 60 or not round(int(lim_1)) > 0:
              break
            else:
              for lim_number in range(len(max(text1)) + 1, round(lim_1 - 1)):
                #SYSTEM SEARCH
                for i in range(len(os.getcwd())):
                  try:
      
                    with os.scandir(os.getcwd()[0:i+1]) as listOfEntries:
                      for file in listOfEntries:
                        
                        if not file.is_file():
                          for file in os.listdir(file):
                            try:
                              with open(file, encoding='latin1') as file1:
                                for j in file1.readlines():
                                  j0 = str(j[0:lim_number]).lower()
                                  try:
                                    if glob:
                                      sum1 = set(j) & set(text)
                                      sum2 = set(j0) & set(text)
                                    else:
                                      sum1 = []
                                      sum2 = []
      
                                    if len(sum1) > lim_number or len(
                                        sum2) > lim_number or str(j0) in text or str(
                                            j0
                                        ) in text1 or str(j) in text1 or text1.count(
                                            str(j)) > 0 or text1.count(str(j0)) > 0:
                                      if len(j) > 1 and not j1.count(
                                          j) > 0 and not j1.count(j0) > 0:
                                        j2 = re.findall(fr'({j0}[^\s]+)', text)
                                        if len(j) < len(j2) and not len(j2) == len(
                                            text1) and not j2 == text1 or len(
                                                j2) > 0:
                                          j1.extend(j2)
                                        else:
                                          j1.append(j)
      
                                  except:
                                    pass
      
                                ai = []
                                ai.extend(
                                    re.findall(fr"|".join(map(re.escape, j)), text))
                                ai.extend(
                                    re.findall(fr"|".join(map(re.escape, j0)), text))
      
                                for i in ai:
                                  while ai.count(
                                      i) > 1 or i == None or i == '' or i == ' ':
                                    try:
                                      ai.remove(i)
                                    except:
                                      ai.append(i)
                                      break
      
                                if len(ai) >= 1:
                                  for lim_number in range(
                                      0,
                                      len(max(text1)) + 1 or round(lim_1 - 1)):
                                    for i in ai:
                                      j0 = str(i[0:lim_number]).lower()
      
                                      try:
                                        if glob:
                                          sum1 = set(i) & set(text)
                                          sum2 = set(j0) & set(text)
                                        else:
                                          sum1 = []
                                          sum2 = []
      
                                        if len(sum1) > lim_number or len(
                                            sum2
                                        ) > lim_number or str(j0) in text or str(
                                            j0
                                        ) in text1 or str(i) in text1 or text1.count(
                                            str(i)) > 0 or text1.count(str(j0)) > 0:
                                          if len(i) > 1 and not j1.count(
                                              j) > 0 and not j1.count(j0) > 0:
                                            j2 = re.findall(fr'({j0}[^\s]+)', text)
                                            #print(j2)
                                            if len(i) < len(
                                                j2) and not len(j2) == len(
                                                    text1
                                                ) and not j2 == text1 or len(j2) > 0:
                                              j1.extend(j2)
                                            else:
                                              j1.append(i)
                                      except:
                                        pass
                            except:
                              pass
                        else:
                          try:
                            with open(file, encoding='latin1') as file1:
                              for j in file1.readlines():
                                j0 = str(j[0:lim_number]).lower()
                                try:
                                  if glob:
                                    sum1 = set(j) & set(text)
                                    sum2 = set(j0) & set(text)
                                  else:
                                    sum1 = []
                                    sum2 = []
      
                                  if len(sum1) > lim_number or len(
                                      sum2) > lim_number or str(j0) in text or str(
                                          j0
                                      ) in text1 or str(j) in text1 or text1.count(
                                          str(j)) > 0 or text1.count(str(j0)) > 0:
                                    if len(j) > 1 and not j1.count(
                                        j) > 0 and not j1.count(j0) > 0:
                                      j2 = re.findall(fr'({j0}[^\s]+)', text)
                                      if len(j) < len(j2) and not len(j2) == len(
                                          text1) and not j2 == text1 or len(j2) > 0:
                                        j1.extend(j2)
                                      else:
                                        j1.append(j)
      
                                except:
                                  pass
      
                              ai = []
                              ai.extend(
                                  re.findall(fr"|".join(map(re.escape, j)), text))
                              ai.extend(
                                  re.findall(fr"|".join(map(re.escape, j0)), text))
      
                              for i in ai:
                                while ai.count(
                                    i) > 1 or i == None or i == '' or i == ' ':
                                  try:
                                    ai.remove(i)
                                  except:
                                    ai.append(i)
                                    break
      
                              if len(ai) >= 1:
                                for lim_number in range(
                                    0,
                                    len(max(text1)) + 1 or round(lim_1 - 1)):
                                  for i in ai:
                                    j0 = str(i[0:lim_number]).lower()
      
                                    try:
                                      if glob:
                                        sum1 = set(i) & set(text)
                                        sum2 = set(j0) & set(text)
                                      else:
                                        sum1 = []
                                        sum2 = []
      
                                      if len(sum1) > lim_number or len(
                                          sum2) > lim_number or str(
                                              j0) in text or str(j0) in text1 or str(
                                                  i) in text1 or text1.count(
                                                      str(i)) > 0 or text1.count(
                                                          str(j0)) > 0:
                                        if len(i) > 1 and not j1.count(
                                            j) > 0 and not j1.count(j0) > 0:
                                          j2 = re.findall(fr'({j0}[^\s]+)', text)
                                          #print(j2)
                                          if len(i) < len(j2) and not len(j2) == len(
                                              text1) and not j2 == text1 or len(
                                                  j2) > 0:
                                            j1.extend(j2)
                                          else:
                                            j1.append(i)
                                            
                                    except Exception as e: print(f"An error occurred: {e}")
                                      
                          except Exception as e: print(f"OPEN ERR: {e}")
      
                  except: pass
      
          # CLEAN LINES
            if len(Hash) >= 800:
              del j1[:400]
      
            if len(j1) >= 800:
              del j1[:400]
      
            for i in Hash:
              while Hash.count(
                  i
              ) > 1 or i == None or i == '' or i == ' ' or fr"\[^\s]+" in i or not i == 'none' or bool(
                  list(filter(lambda x: x[0].lower() in str(i), Hash))):
                try:
                  Hash.remove(i)
                except:
                  Hash.append(i)
                  break
      
            for i in j1:
              while j1.count(
                  i
              ) > 1 or i == None or i == '' or i == ' ' or fr"\[^\s]+" in i or not i == 'none' or bool(
                  list(filter(lambda x: x[0].lower() in str(i), j1))):
                try:
                  j1.remove(i)
                except:
                  j1.append(i)
                  break
      
        # SYSTEM FILE
      
          math = ''
          add = 0
          text1.append(text)
      
          for i in text1:
      
            # CODE !
            try:
              math = str(eval(str(i))).split()
              if not math == '' and not math == ' ' and not math == 'None':
                j1.extend(math)
                add = 1
            except:
              pass
      
            try:
              math = str(sum(str(i))).split()
              if not math == '' and not math == ' ' and not math == 'None':
                j1.append(math)
                add = 2
            except:
              pass
      
            try:
              math = str(dict(str(i))).split()
              if not math == '' and not math == ' ' and not math == 'None':
                j1.append(math)
                add = 4
            except:
              pass
      
            try:
              math = str(os.getenv(str(i)))
              if not math == '' and not math == ' ' and not math == 'None':
                j1.append(math)
                add = 4
            except:
              pass
      
            try:
              math = str(setattr(str(i))).split()
              if not math == '' and not math == ' ' and not math == 'None':
                j1.append(math)
                add = 5
            except:
              pass
      
            try:
              math = str(ord(str(i))).split()
              if not math == '' and not math == ' ' and not math == 'None':
                j1.append(math)
                add = 10
            except:
              pass
      
            try:
              math = str(chr(str(i))).split()
              if not math == '' and not math == ' ' and not math == 'None':
                j1.append(math)
                add = 10
            except:
              pass
      
            # OPEN FILE !
      
            try:
              with open(i, encoding='latin1') as file1:
                try:
                  j1.append(file1.readline(int(''.join(math))))
                except:
                  for j in file1.readlines():
                    j1.append(str(j)[:32])
            except:
              pass
      
            try:
              os.open(i)
      
            except:
              pass
      
            try:
              os.openpty(i)
      
            except:
              pass
      
            try:
              os.start(i)
      
            except:
              pass
      
            try:
              j1.append(climage.convert(str(i), palette='tango'))
              #print('\n')
      
            except:
              pass
      
            try:
              math = str(getattr(str(i))).split()
              if not math == '' and not math == ' ' and not math == 'None':
                j1.extend(math)
      
            except:
              pass
      
            try:
              math = str(globals(str(i))).split()
              if not math == '' and not math == ' ' and not math == 'None':
                j1.extend(math)
      
            except:
              pass
      
          if 'task' in text1:
            try:
              j1.clear()
              j1.append('  || Build: ' + ' '.join(j2))
              j1.append('  || limit: ' + str(int(lim_1)))
      
              j1.append('  || Core1: ' + str(j))
              j1.append('  || Core2: ' + str(i))
      
              j1.append('  || File: ' + str(file))
      
            except:
              pass
      
          if 'cloud' in text1:
            try:
              j1.clear()
              try:
                j1.extend(Hash)
              except:
                for i in Hash:
                  try:
                    j1.append(i)
                  except:
                    pass
            except:
              pass
      
          if 'del' in text1:
      
            try:
              if len(text1) >= 1:
                while j1.count(max(text1)) > 0 or Hash.count(max(text1)) > 0:
                  try:
                    j1.remove(max(text1))
                  except:
                    pass
      
                  try:
                    Hash.remove(max(text1))
                  except:
                    pass
      
                  try:
                    os.rmdir(max(text1))  # *, dir_fd=None
                  except:
                    pass
      
                  try:
                    os.remove(max(text1))  #*, dir_fd=None)
                  except:
                    pass
      
                  try:
                    os.close(max(text1))
                  except:
                    pass
      
                  try:
                    os.get_blocking(max(text1))
                  except:
                    pass
      
            except:
              pass
      
          if 'boot' in text1 or 'clean' in text1:
            try:
              j1.clear()
              Hash.clear()
              run(lim_1)
            except:
              pass
      
          if 'save' in text1:
            try:
              j1.clear()
              if len(text1) >= 1 and len(Hash) >= 1:
                with open(max(text1), "+a") as f:
                  j1.append(str(f.name))
                  f.write(f'\n \n # <!-- Cloud {max(text1)} --> \n \n')
                  try:
                    f.write('\n'.join(Hash))
                  except:
                    for i in Hash:
                      f.write('\n' + str(i))
                  f.write('\n \n')
                j1.append(str(os.stat(str(f.name))))
              else:
                j1.clear()
      
            except:
              pass
      
          if 'cls' in text1 or 'clear' in text1:
            try:
              os.system("cls")
      
            except:
              pass
      
          #Close Progressbar
      
          if len(j1) >= 1:
      
            for i in Hash:
      
              while Hash.count(
                  i
              ) > 1 or i == None or i == '' or i == ' ' or fr"\[^\s]+" in i or not i == 'none' or bool(
                  list(filter(lambda x: x[0].lower() in str(i), Hash))):
                try:
                  Hash.remove(i)
                except:
                  Hash.append(i)
                  break
      
            for i in j1:
      
              while j1.count(
                  i
              ) > 1 or i == None or i == '' or i == ' ' or fr"\[^\s]+" in i or not i == 'none' or bool(
                  list(filter(lambda x: x[0].lower() in str(i), j1))):
                try:
                  j1.remove(i)
                except:
                  j1.append(i)
                  break
      
          else:
            H8 = [create_req(text1)]
            if None in H8:
              if len(text1) >= 1 and len(text) >= 3 and len(j1) <= len(text):
                #print('add')
                Hash.extend(text1)
        
                H8 = ['maybe', 'norm', 'no idea', 'note', 'good', 'fine too']
        
              else:
                if len(re.findall('[a-z]+', text)) >= 1:
                  H8 = [
                      'I need a description', 'What is this?', 'hard to guess',
                      'What did you mean?', 'small string here',
                      f'more into {max(text1)}', 'awesome?'
                  ]
                else:
                  H8 = ['...', '..', '.']
            print(H8)
            j1.append(f' {random.choice(H8)} \n')
      
          #print(' ------------------------ ')
      
          if j1 == text1 or j1 in text1:
            j1 = j1[::-1]
      
          if not pull:
            try:
              j1 = sorted(j1, key=len, reverse=True)[:len(text1)]
            except:
              pass
      
          if setx:
            for i in text1:
              try:
                j1 = j1[:len(j1) % round(float(i))]
              except:
                pass
          else:
            j1 = j1[:len(j1) % 25]
      
          for word in j1:
            try:
              j2.append(morph.parse(word)[0].normal_form)
            except:
              pass
          try:
            j1 = random.choice(j2)
          except:
            if len(j1) >= 1:
              pass
            else:
              j1 = sorted(j2, key=len, reverse=True)[:len(text1)]
            #print("\b" + '\033[1;44m' + ' '.join(j1))
      
          #print('1: & 2: Exit')
          #print('Build: ', j1)
          #print('limit 10: ', lim_1)
      
        except Exception as err:
          j1 = str("\b" + ' AI: ' + str(err) + f'/n Err: {traceback.format_exc()}')
      
        j1 = j1[:820]
  
        markup = types.InlineKeyboardMarkup()
        try:
          webApp = types.WebAppInfo(invite_link)
          btn_new = types.InlineKeyboardButton(text='Open in', web_app=webApp)
        except: 
          btn_new = types.InlineKeyboardButton(text='Open in', url=invite_link)
        
        markup.add(btn_new)
  
        try:
          try:
            client.reply_to(message, decode_text(''.join(j1)), reply_markup=markup, parse_mode="Markdown")
          except:
            client.send_message(message.chat.id, decode_text(''.join(j1)), reply_markup=markup, parse_mode="Markdown")
        except:       
          try:
            client.reply_to(message, ''.join(j1), parse_mode="Markdown")
          except:
            client.send_message(message.chat.id, ''.join(j1), parse_mode="Markdown")

        try: 
          client.forward_message('-1001832648686', message.chat.id, message.message_id)
        except: pass
      
        try:
          client.send_message('-1001832648686', ''.join(j1), parse_mode="Markdown")
        except: pass
  
        try:
          try:
            all_users = client.get_chat_members(message.chat.id)  # Получаем список всех участников чата
          except:
            all_users = client.get_chat_members(message)
      
          for user in all_users:
            try:
              client.send_message(user.user.id,
                                  f'Topics: \n [+] {str(list(Hash[::-1])[:3])}', parse_mode="Markdown")  # Отправляем сообщение каждому участнику
            except:
              try:
                client.send_message(user,
                                    f'Topics: \n [+] {str(list(Hash[::-1])[:3])}', parse_mode="Markdown")
              except:
                pass
      
        except:
          pass
      
        try:
          chats = client.get_updates()
      
          for chat in chats:
            try:
              client.send_message(user.user.id,
                                  f'Topics: \n [+] {str(list(Hash[::-1])[:3])}', parse_mode="Markdown")  # Отправляем сообщение каждому участнику
            except:
              try:
                client.send_message(user,
                                    f'Topics: \n [+] {str(list(Hash[::-1])[:3])}', parse_mode="Markdown")
              except:
                pass
      
        except:
          pass

    
    if __name__ == "__main__":
      try:
        print('[***]start!')
        try:
          client.polling(none_stop=True, interval=1,
                         timeout=1)  #, long_polling_timeout = 5)
        except:
          try:
            client.polling(none_stop=True)
          except:
            client.infinity_polling(interval=1, timeout=1)
        
    
      except:
        print('[+]FIX!')
        try:
          client.run_until_disconnected()
        except: pass
  
  
  except Exception as err:
    print("\b" + ' SYSTEM_ERR: ' + str(err))
    print('Err:', traceback.format_exc())