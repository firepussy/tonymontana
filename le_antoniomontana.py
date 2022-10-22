token = "1861045996:AAEmp4x_X3Kly6gKKpmlkXAgxsH2xq2ScE0"

import requests
import json
from datetime import datetime
import time

import telegram
from telegram.ext import Updater


a = open("coins.txt", "r")
a = a.read()
coins = list(map(str, a.split()))
print(coins)

def info(s):
	req = ""
	lost_dict = {}
	lost_dict["last_updated_at"] = 'not found'
	lost_dict['usd'] = 'not found'

	req = "https://api.coingecko.com/api/v3/simple/price?ids=" + s + "&vs_currencies=usd&include_last_updated_at=true"
	inf = requests.get(req)
	inf = inf.content
	inf = inf[1:-1]
	if len(inf) < 10:
		return(lost_dict)
	else:
		inf = inf[len(s)+3:]
		dict_inf = json.loads(inf)
		dict_inf["last_updated_at"] = datetime.utcfromtimestamp(dict_inf["last_updated_at"]).strftime('%Y-%m-%d %H:%M:%S')

		req_delta = ''
		time_now = int(time.time())
		time_back = time_now - 1860
		req_delta = 'https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range?vs_currency=usd&from={time_back}&to={time_now}%20'.format(coin = s, time_back = time_back, time_now = time_now)
		inf_delta = requests.get(req_delta)
		inf_delta = inf_delta.content
		dict_inf_delta = json.loads(inf_delta)
		dict_inf.update(dict_inf_delta)
		dict_inf['5min'] = "{:+.2%}".format( ((float(dict_inf['usd']) - float(dict_inf['prices'][-1][1])) / dict_inf['prices'][-1][1]) )
		dict_inf['15min'] ="{:+.2%}".format( ((float(dict_inf['usd']) - float(dict_inf['prices'][int((len(dict_inf['prices']) + 1) / 2)][1])) / dict_inf['prices'][0][1]) )
		dict_inf['30min'] ="{:+.2%}".format( ((float(dict_inf['usd']) - float(dict_inf['prices'][0][1])) / dict_inf['prices'][0][1]) )

		dict_inf['5min_num'] =  ((float(dict_inf['usd']) - float(dict_inf['prices'][-1][1])) / dict_inf['prices'][-1][1])
		dict_inf['15min_num'] = ((float(dict_inf['usd']) - float(dict_inf['prices'][int((len(dict_inf['prices']) + 1) / 2)][1])) / dict_inf['prices'][0][1])
		dict_inf['30min_num'] = ((float(dict_inf['usd']) - float(dict_inf['prices'][0][1])) / dict_inf['prices'][0][1])

		return(dict_inf)

#
#u = Updater(token, use_context=True)
#j = u.job_queue
def checker(context: telegram.ext.CallbackContext):
	res = ''
	for i in range(len(coins)):
		s = coins[i]
		inf = info(s)
		print(inf['5min_num'])
		print(inf['15min_num'])
		print(inf['30min_num'])
		if (abs(inf['5min_num']) >= 0.05 or abs(inf['15min_num']) >= 0.05 or abs(inf['30min_num']) >= 0.05):
			res += inf['5min'] + inf['15min'] + inf['30min'] + '\n'
			context.bot.send_message(message.from_user.id, 'coin {s} is doing smth: {res}'.format(s = s, res = res))
#job_minute = j.run_repeating(checker(-587721800), interval = 600)
#job_minute.enabled = True
#

bot = telebot.TeleBot("1861045996:AAEmp4x_X3Kly6gKKpmlkXAgxsH2xq2ScE0")


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Hello, I am Tony and I will help make you some money ;)")


@bot.message_handler(commands=['help'])
def help_answer(message):
	bot.reply_to(message, "If you want to add coin to watchlist – type /addcoin 'coin_name' \nIf you want to remove coin from watchlist – type /rmcoin 'coin_name'")

################

@bot.message_handler(commands=['addcoin'])
def addcoin_answer(message):
	if (message.text != "/addcoin"):
		coins.append(message.text[9::])
		a = open("coins.txt", "a")
		a.write('\n')
		a.write(coins[-1])
		bot.reply_to(message, message.text[9:] + " has been added")
	else:
		bot.reply_to(message, "Try again")



@dp.message_handler()
async def addcoin_answer(message: types.Message):
        if (message.text != "/addcoin"):
		coins.append(message.text[9::])
		a = open("coins.txt", "a")
		a.write('\n')
		a.write(coins[-1])
		await bot.send_message(message.from_user.id, message.text[9:] + " has been added")
	else:
		await bot.send_message(message.from_user.id, "Try again")
    await bot.send_message(msg.from_user.id, msg.text)

###################


@bot.message_handler(commands=['allcoins'])
def allcoins_answer(message):
	res = ""
	a = open("coins.txt", "r")
	a = a.read()
	coins = list(map(str, a.split()))
	for i in range(len(coins)):
		res = res + "\n" + coins[i]
	bot.reply_to(message, res)

@bot.message_handler(commands=['rmcoin'])
def rmcoin_answer(message):
	a = open("coins.txt", "r")
	a = a.read()
	perres = message.text[8:]
	if (a.find(perres) == -1):
		bot.reply_to(message, "Try again")
	else:
		a = a.split()
		a.remove(perres)
		print(a)
		coins = a
		m = open("coins.txt", "w")
		result = ''
		for i in range(len(a)):
			result = result + "\n" + a[i]
		print(result)
		m.write(result)
		bot.reply_to(message, message.text[7:] + " has been deleted")


@bot.message_handler(commands=['coinstat'])
def _answer(message):
	if (message.text != "/coinstat"):
		s = message.text[10::]
		inf = {}
		inf = info(s)
		print(s)
		print(inf)
		bot.reply_to(message, str(inf['usd']) + ' price in usd' + '\n' + 'last updated at ' + inf['last_updated_at'] + '\ndeltas: for 5min – {min5}, for 15min – {min15}, for 30min – {min30}'.format(min5 = inf['5min'], min15 = inf['15min'], min30 = inf['30min']) + '\n' + '\n')


@bot.message_handler(commands = ['allstat'])
def allstat_answer(message):
	res = ''
	for i in range(len(coins)):
		s = coins[i]
		inf = info(s)
		print(inf['prices'])
		res += 'for {coin} {price} – price in usd  \nlast updated at: {last_updated_at} \ndeltas: for 5min – {min5}, for 15min – {min15}, for 30min – {min30}'.format(coin = s, price = inf['usd'], last_updated_at = inf['last_updated_at'], min5 = inf['5min'], min15 = inf['15min'], min30 = inf['30min']) + '\n' + '\n'
	bot.reply_to(message, res)

@bot.message_handler(commands = ['checker'])
def checker(message):
	res = ''
	for i in range(len(coins)):
		s = coins[i]
		inf = info(s)
		print(inf['5min_num'])
		print(inf['15min_num'])
		print(inf['30min_num'])
		if (abs(inf['5min_num']) >= 0.05 or abs(inf['15min_num']) >= 0.05 or abs(inf['30min_num']) >= 0.05):
			res += inf['5min'] + inf['15min'] + inf['30min'] + '\n'
			bot.reply_to(message, 'coin {s} is doing smth: {res}'.format(s = s, res = res))

bot.polling()








#######################

@dp.message_handler(commands = ['checker'])
async def checker(message):
        res = ''
        for i in range(len(coins)):
                s = coins[i]
                inf = info(s)
                print(inf['5min_num'])
                print(inf['15min_num'])
                print(inf['30min_num'])
                if (abs(inf['5min_num']) >= 0.05 or abs(inf['15min_num']) >= 0.05 or abs(inf['30min_num']) >= 0.05):
                        res += inf['5min'] + inf['15min'] + inf['30min'] + '\n'
                        await bot.send_message(message.from_user.id, 'coin {s} is doing smth: {res}'.format(s = s, res = res))

'deltas: for 5min – {min5}, for 15min – {min15}, for 30min – {min30}'.format(min5 = inf['5min'], min15 = inf['15min'], min30 = inf['30min'])
