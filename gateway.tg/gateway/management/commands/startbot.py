from django.core.management.base import BaseCommand, CommandError
from telegram.ext import Updater
from os.path import isfile
import six

class Command(BaseCommand):
	help = 'Start the telegram bot'

	def add_arguments(self, parser):
		parser.add_argument('-conf')
		parser.add_argument('-token')
		parser.add_argument('-ipaddr')
		parser.add_argument('-port', type=int)

	def handle(self, *args, **options):
		conf=options.get('conf', None)
		if conf and isfile(conf): 
			exec(open(conf, 'r').read())

		if 'TOKEN' in locals() and 'token' not in options:
			options['token']=locals()['TOKEN']

		if 'IPADDR' in locals() and 'ipaddr' not in options:
			options['ipaddr']=locals()['IPADDR']

		if 'PORT' in locals() and 'port' not in options:
			options['port']=locals()['PORT']

		print('Gateway Token: %s'%options['token'])
		print('CCU Addr: %s:%s'%(options['ipaddr'], options['port']))
