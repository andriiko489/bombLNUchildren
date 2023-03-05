import telebot
import sqlite3
#TODO: do global and by chat users top
con = sqlite3.connect("sqlite.db", check_same_thread=False)
bot = telebot.TeleBot("", parse_mode=None)

cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS chat(id INTEGER, title TEXT, score INTEGER)")
res = cur.execute("SELECT * FROM chat")
globalCounter = 0
chats = {}
for i in res.fetchall():
    globalCounter += i[2]
    chats[i[0]] = [i[1],i[2]]
print(globalCounter)
print(chats)
@bot.message_handler(commands=['Bomb_LNU_children'])
def bomb(message):
    global globalCounter
    global chats
    global cur, con
    globalCounter += 1
    if not message.chat.id in chats.keys():
        chats[message.chat.id] = []
        chats[message.chat.id].append(message.chat.title)
        chats[message.chat.id].append(1)
        cur.execute('''INSERT INTO chat VALUES({}, "{}", {})'''.format(message.chat.id, message.chat.title, 0))
    else:
        chats[message.chat.id][1] += 1
        cur.execute('''UPDATE chat SET score = {} WHERE id = {}'''.format(chats[message.chat.id][1], message.chat.id))
    con.commit()
    bot.reply_to(message, "Бомби на дітей ЛНУ скинуто, це вже відбулося {} разів".format(globalCounter))

@bot.message_handler(commands=['top'])
def top(message):
    global cur, con
    res = cur.execute("SELECT * FROM chat ORDER BY score")
    str = 'Топ бомбардувальників дітей ЛНУ:'
    table = res.fetchall()[::-1]
    for i in range(len(table)):
        str+="\n{}. {} - {}".format(i+1, table[i][1], table[i][2])
    bot.reply_to(message, str)
bot.polling()