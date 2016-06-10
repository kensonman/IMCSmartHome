# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone as tz
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from os.path import isfile
import six, logging, requests, uuid, netifaces

FMT='%Y-%m-%dT%H:%M:%S%z'

class Command(BaseCommand):
	help = 'Start the telegram bot'
	logger=logging.getLogger('startbot')
	logging.basicConfig(filename='bot.log',level.logging.INFO)

	def add_arguments(self, parser):
		parser.add_argument('-conf', default='conf.py')
		parser.add_argument('-token')
		parser.add_argument('-ipaddr')
		parser.add_argument('-port', type=int)

	def ping(self, bot, update):
		bot.sendMessage(chat_id=update.message.chat_id, text='Pong')

	def help(self, bot, update):
		bot.sendMessage(chat_id=update.message.chat_id, text='''
		Available Command: 
		 /help  - Print this message
		 /ping  - Send back the pong for checking connection
		''')

	def message(self, bot, update):
		print('message....')
		self.logger.info('Received Message \"%s\" from \"%s\"'%(update.message.text,update.message.from_user))
		data=dict()
		data['UUID']=uuid.uuid4().__str__()
		data['CMD']='MSG'
		data['SNAME']='Gateway'
		data['SIP']=self.ipaddr
		data['SPORT']=getattr(settings, 'PORT', '8000')
		data['TNAME']='CCU'
		data['TIP']=self.ccu
		data['TPORT']=self.port
		data['PARAMS']=update.message.text
		data['TIME']=tz.now().strftime(FMT)
		url='http://%s:%s/cmd/'%(data['TIP'], data['TPORT'])
		print('POST to %s'%url)
		r=requests.post(url, data=data)
		if r.status_code >=200 and r.status_code<300:
			bot.sendMessage(chat_id=update.message.chat_id, text=r.text)
		else:
			bot.sendMessage(chat_id=update.message.chat_id, text='Error: %s'%r.text)

	def startbot(self, token, ccu, port):
		if not (token and ccu and port):
			print('Please specify the ipaddr and port')
			return

		self.token=token
		self.ccu=ccu
		self.port=port
		print('Gateway Token: %s'%token)
		print('CCU Addr: %s:%s'%(ccu, port))
		print('This IPAddress: %s'%self.ipaddr)
		self.updater=Updater(token=token)
		self.dispatcher=self.updater.dispatcher
		self.dispatcher.add_handler(CommandHandler('help', self.help))
		self.dispatcher.add_handler(CommandHandler('ping', self.ping))
		self.dispatcher.add_handler(MessageHandler([Filters.text], self.message))
		self.updater.start_polling()

	def handle(self, *args, **options):
		conf=options.get('conf')
		print('conf: %s'%conf)
		if conf and isfile(conf): 
			exec(open(conf, 'r').read())

		if 'TOKEN' in locals() and not options['token']:
			options['token']=locals()['TOKEN']

		if 'IPADDR' in locals() and not options['ipaddr']:
			options['ipaddr']=locals()['IPADDR']

		if 'PORT' in locals() and not options['port']:
			options['port']=locals()['PORT']

		if 'token' not in options:
			print('Please specify the token')
			return

		self.ipaddr=netifaces.ifaddresses(getattr(settings, 'BIND', 'eth0'))[2][0]['addr']
		self.startbot(options['token'], options['ipaddr'], options['port'])
