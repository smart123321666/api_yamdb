import os
import sqlite3

import pandas as pd
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title


class Command(BaseCommand):
    help = 'The Zen of Python'

    def add_arguments(self, parser):
        parser.add_argument('path', action='store')

    def handle(self, *args, **options):
        path = options['path']
        files_csv = os.listdir(path)
        files_csv.remove('users.csv')
        files_csv.sort()
        category, comments, genre, genre_title, review, titles = files_csv
        print(files_csv)

        category_path = path + '/' + category
        df_category = pd.read_csv(category_path)
        for index, row in df_category.iterrows():
            Category.objects.create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
        print('Import catecory done')

        genre_path = path + '/' + genre
        df_genre = pd.read_csv(genre_path)
        for index, row in df_genre.iterrows():
            Genre.objects.create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
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

        review_path = path + '/' + review
        df_review = pd.read_csv(review_path)
        for index, row in df_review.iterrows():
            Review.objects.create(
                id=row['id'],
                text=row['text'],
                author=row['author_id'],
                score=row['score'],
                pub_date=row['pub_date'],
                title_id=row['title_id'],
            )
        print('Import review done')

        comments_path = path + '/' + comments
        df_comments = pd.read_csv(comments_path)
        for index, row in df_comments.iterrows():
            Comment.objects.create(
                id=row['id'],
                text=row['text'],
                author=row['author_id'],
                pub_date=row['pub_date'],
                review_id=row['review_id'],
            )
        print('Import comments done')

        genre_title_path = path + '/' + genre_title
        df_genre_title = pd.read_csv(genre_title_path)
        database_name = 'db.sqlite3'
        conn = sqlite3.connect(database_name)
        df_genre_title.to_sql(
            'reviews_title_genre',
            conn,
            index=False,
            if_exists='replace'
        )
        conn.close()
        print('Import genre_titl done')
