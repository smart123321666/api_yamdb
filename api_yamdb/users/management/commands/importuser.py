import pandas as pd
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
#from users.models import CustomUser

User = get_user_model()

class Command(BaseCommand):
    help = 'Import data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        df = pd.read_csv(csv_file)

        for index, row in df.iterrows():
            User.objects.create(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )