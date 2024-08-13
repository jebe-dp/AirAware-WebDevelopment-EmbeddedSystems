from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperUserCommand
from django.core.management import CommandError

class Command(CreateSuperUserCommand):
    help = 'Create a superuser with an additional birth_date field'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--birth_date', dest='birth_date', type=str, help='Date of birth in the format YYYY-MM-DD')

    def handle(self, *args, **options):
        birth_date = options.get('birth_date')
        if not birth_date:
            raise CommandError('You must provide a birth_date using --birth_date YYYY-MM-DD')

        super().handle(*args, **options)

        username = options.get('username')
        user = self.UserModel._default_manager.get(username=username)
        user.birth_date = birth_date
        user.save()
