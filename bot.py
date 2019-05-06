from telegram.ext import CommandHandler, MessageHandler, Filters, Updater,CallbackQueryHandler
import telegram
import datetime
from datetime import timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os,sys

updater = Updater(token='849919118:AAFxrD4ytO252jC5y4ZYAQuijJJUzDQ6A3Y')
dispatcher = updater.dispatcher

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('QRReviews-fe5cd1a8da85.json',scope)

users ={}
anonim={}
source={}

yes_button = telegram.InlineKeyboardButton(text='Да',callback_data='YES')
not_button = telegram.InlineKeyboardButton(text='Нет',callback_data='NOT')

hig_button = telegram.InlineKeyboardButton(text='🔥',callback_data='hig')
mid_button = telegram.InlineKeyboardButton(text='👌',callback_data='mid')
bot_button = telegram.InlineKeyboardButton(text='👎',callback_data='bot')
# for sheet in sheets.worksheets():
# 	print(sheet)

#get_worksheet(0)

def update_table(anon,u_id,mark,name="None"):
	try:
		gc = gspread.authorize(credentials)
		sheet=gc.open('Фидбек').sheet1
		if anon:
			sheet.append_row([source[u_id],users[u_id],str(mark)])
		else:
			sheet.append_row([source[u_id],users[u_id],str(mark),name])
	except:
		os.startfile(sys.argv[0])
		os.abort()


def lisingToAll(bot, update):
	print(update.message.text)
	dex = True
	for val in users.keys():
		if val==update.message.chat_id:
			dex = False
	if dex:
		users[update.message.chat_id] = update.message.text
		bot.send_message(chat_id=update.message.chat_id,
				 text='Оцени наш сервис:',
				 reply_markup=telegram.InlineKeyboardMarkup([[hig_button,mid_button,bot_button]])
				 )
	elif(users[update.message.chat_id]=="215661"):
		users[update.message.chat_id] = update.message.text
		bot.send_message(chat_id=update.message.chat_id,
					 text='Привет, здесь ты можешь оставить свой отзыв.'+'\n'+'Хочешь остаться анонимным, наш бот скроет твой nickname?',
					 reply_markup=telegram.InlineKeyboardMarkup([[yes_button,not_button]])
					 )			
	else:
		bot.send_message(chat_id=update.message.chat_id,
				 text='Оцени наш сервис:',
				 reply_markup=telegram.InlineKeyboardMarkup([[hig_button,mid_button,bot_button]])
				 )
		
def callback_query_handler(bot, update):
	cqd = update.callback_query.data
	if cqd == 'YES':
		anonim[update.callback_query.message.chat_id] = True
		bot.send_message(chat_id=update.callback_query.message.chat_id,text="Твой отзыв скрыт, напиши мне его:")
		bot.deleteMessage(update.callback_query.message.chat_id,update.callback_query.message.message_id)
	elif cqd == 'NOT':
		anonim[update.callback_query.message.chat_id] = False
		bot.send_message(chat_id=update.callback_query.message.chat_id,text="Напишите мне отзыв")
		bot.deleteMessage(update.callback_query.message.chat_id,update.callback_query.message.message_id)
	elif cqd == 'hig':
		bot.send_message(chat_id=update.callback_query.message.chat_id,text="Спасибо! Что помогаешь нам стать лучше!")
		bot.send_message(chat_id=update.callback_query.message.chat_id,text="Напиши любое сообщение чтобы запустить чат-бот заново")
		update_table(anonim[update.callback_query.message.chat_id],update.callback_query.message.chat_id,5,update.callback_query.message.chat.username);
		users[update.callback_query.message.chat_id] = "215661"
		bot.deleteMessage(update.callback_query.message.chat_id,update.callback_query.message.message_id)
	elif cqd == 'mid':
		bot.send_message(chat_id=update.callback_query.message.chat_id,text="Спасибо! Что помогаешь нам стать лучше!")
		bot.send_message(chat_id=update.callback_query.message.chat_id,text="Напиши любое сообщение чтобы запустить чат-бот заново")
		update_table(anonim[update.callback_query.message.chat_id],update.callback_query.message.chat_id,4,update.callback_query.message.chat.username);
		users[update.callback_query.message.chat_id] = "215661"
		bot.deleteMessage(update.callback_query.message.chat_id,update.callback_query.message.message_id)
	elif cqd == 'bot':
		bot.send_message(chat_id=update.callback_query.message.chat_id,text="Спасибо! Что помогаешь нам стать лучше!")
		bot.send_message(chat_id=update.callback_query.message.chat_id,text="Напиши любое сообщение чтобы запустить чат-бот заново")
		update_table(anonim[update.callback_query.message.chat_id],update.callback_query.message.chat_id,3,update.callback_query.message.chat.username);
		users[update.callback_query.message.chat_id] = "215661"
		bot.deleteMessage(update.callback_query.message.chat_id,update.callback_query.message.message_id)

def main_menu(bot, update):
	utm=update.message.text.split(' ')
	if len(utm)>1:
		source[update.message.chat_id]=utm[1]
	else:
		source[update.message.chat_id]="None"
	bot.send_message(chat_id=update.message.chat_id,
					 text='Привет, здесь ты можешь оставить свой отзыв.'+'\n'+'Хочешь остаться анонимным, наш бот скроет твой nickname?',				
					 reply_markup=telegram.InlineKeyboardMarkup([[yes_button,not_button]])
					 )	

dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))
dispatcher.add_handler(MessageHandler(Filters.text, lisingToAll))
dispatcher.add_handler(CommandHandler('start', main_menu))

if __name__ == '__main__':
	updater.start_webhook(listen='0.0.0.0', port=5000, webhook_url="https://testingheroku12354.herokuapp.com/")
