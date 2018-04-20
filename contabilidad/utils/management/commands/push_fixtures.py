from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Project Utils Django Command'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
        pass
