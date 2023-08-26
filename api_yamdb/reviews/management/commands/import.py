import csv
import os

from django.core.management.base import BaseCommand, CommandError

from api_yamdb.settings import BASE_DIR
from reviews.models import Category, Comment, Genre, Review, Title, User

FILE_PATH = os.path.join(
    BASE_DIR,
    'static/data'
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            with open(
                os.path.join(FILE_PATH, 'category.csv')
            ) as file_csv:
                file_read = csv.DictReader(file_csv, delimiter=',')
                for row in file_read:
                    Category.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                print('Файл category.csv успешно импортировал данные в БД')

            with open(
                os.path.join(FILE_PATH, 'genre.csv')
            ) as file_csv:
                file_read = csv.DictReader(file_csv, delimiter=',')
                for row in file_read:
                    Genre.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                print('Файл genre.csv успешно импортировал данные в БД')

            with open(
                os.path.join(FILE_PATH, 'titles.csv')
            ) as file_csv:
                file_read = csv.DictReader(file_csv, delimiter=',')
                for row in file_read:
                    Title.objects.create(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category=Category.objects.get_or_create(
                            id=row['category'],
                        )[0],
                    )
                print('Файл titles.csv успешно импортировал данные в БД')

            with open(
                os.path.join(FILE_PATH, 'genre_title.csv')
            ) as file_csv:
                file_read = csv.DictReader(file_csv, delimiter=',')
                for row in file_read:
                    title, id = Title.objects.get_or_create(
                        id=row['title_id'],
                    )
                    genre, id = Genre.objects.get_or_create(
                        id=row['genre_id'],
                    )
                    title.genre.add(genre)
                    title.save()
                print('Файл genre_title.csv успешно импортировал данные в БД')

            with open(
                os.path.join(FILE_PATH, 'users.csv')
            ) as file_csv:
                file_read = csv.DictReader(file_csv, delimiter=',')
                for row in file_read:
                    User.objects.create(
                        id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        role=row['role'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                    )
                print('Файл users.csv успешно импортировал данные в БД')

            with open(
                os.path.join(FILE_PATH, 'review.csv')
            ) as file_csv:
                file_read = csv.DictReader(file_csv, delimiter=',')
                for row in file_read:
                    Review.objects.create(
                        id=row['id'],
                        title=Title.objects.get_or_create(
                            id=row['title_id'],
                        )[0],
                        text=row['text'],
                        author=User.objects.get_or_create(
                            id=row['author'],
                        )[0],
                        score=row['score'],
                        pub_date=row['pub_date'],

                    )
                print('Файл review.csv успешно импортировал данные в БД')

            with open(
                os.path.join(FILE_PATH, 'comments.csv')
            ) as file_csv:
                file_read = csv.DictReader(file_csv, delimiter=',')
                for row in file_read:
                    Comment.objects.create(
                        id=row['id'],
                        review=Review.objects.get_or_create(
                            id=row['review_id'],
                        )[0],
                        text=row['text'],
                        author=User.objects.get_or_create(
                            id=row['author'],
                        )[0],
                        pub_date=row['pub_date'],
                    )
                print('Файл comments.csv успешно импортировал данные в БД')

        except Exception:
            raise CommandError('Произошла ошибка')

        self.stdout.write(
            self.style.SUCCESS('Данные были загружены в БД')
        )
