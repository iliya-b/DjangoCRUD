import time

import telebot
from django.core.management.base import BaseCommand

from DjangoCRUD import settings
from rcoffee.models import Team, User


class Command(BaseCommand):
    help = 'Adds team'

    def add_arguments(self, parser):
        parser.add_argument('--password', type=str, required=True)
        parser.add_argument('--name', type=str, required=True)
        parser.add_argument('--admin', type=int, default=None)

    def handle(self, *args, **options):
        admin_id = User.objects.get(pk=options['admin']) if options['admin'] else None
        team = Team.objects.create(name=options.get('name'),
                                   password=options.get('password'),
                                   admin=admin_id)
        self.stdout.write(self.style.SUCCESS(str(team)))
