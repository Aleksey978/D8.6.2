from django.core.management.base import BaseCommand, CommandError
from news_portal.models import Post, Category


class Command(BaseCommand):
    help = 'Удаление постов конкретной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все посты в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            print(options['category'])
            category = Category.objects.get(category_name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category}'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {options["category"]}'))