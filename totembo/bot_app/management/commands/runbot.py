from django.core.management.base import BaseCommand

from ...loader import bot

class Command(BaseCommand):
    help = 'Bot islep tur'


    def handle(self, *args, **options):
        from ... import handlers
        print('Bot isledi')
        bot.infinity_polling()


