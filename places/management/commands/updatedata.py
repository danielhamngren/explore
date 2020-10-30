from django.core.management.base import BaseCommand, CommandError
from places import load

class Command(BaseCommand):
    help = 'Downloads place data from Openstreetmap and saves it in the database'

    def handle(self, *args, **options):
        load.update_data()
