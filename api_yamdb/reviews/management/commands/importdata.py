import os
import pandas as pd
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title


class Command(BaseCommand):
    help = 'The Zen of Python'

    def add_arguments(self, parser):
        parser.add_argument('path', action='store')

    def handle(self, *args, **options):
        path = options['path']
        files_csv = os.listdir(path)
        files_csv.remove('users.csv')
        category, comments, genre, genre_title, review, titles = files_csv
        category_path = path + '/' + category
        df_category = pd.read_csv(category_path)
        """ for index, row in df_category.iterrows():
            Category.objects.create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
        print('Import catecory done') """
        genre_path = path + '/' + genre
        df_genre = pd.read_csv(genre_path)
        """ for index, row in df_genre.iterrows():
            Genre.objects.create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            ) """
        print('Import genre done')
        titles_path = path + '/' + titles
        df_titles = pd.read_csv(titles_path)
        for index, row in df_titles.iterrows():
            Title.objects.create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category'],
            )
        print('Import titles done')
        genre_title_path = path + '/' + genre_title
        df_genre_title = pd.read_csv(genre_title_path)
        for index, row in df_genre_title.iterrows():
            Title.objects.create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category'],
            )
        print('Import titles done')
        #print(df)