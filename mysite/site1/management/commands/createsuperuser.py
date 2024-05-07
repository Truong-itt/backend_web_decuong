from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

class Command(createsuperuser.Command):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        # role 
        parser.add_argument('--role', type=str, help='Role of the user')
        # first_name 
        parser.add_argument('--first_name', type=str, help='First_name of the user')
        # last_name
        parser.add_argument('--lastname', type=str, help='Last name of the user')
        # id_user
        parser.add_argument('--id_user', type=str, help='Id of the user')

    def handle(self, *args, **options):
        # role 
        role = options.get('role')
        if not role:
            raise CommandError("Role is required")
        try:
            role = int(role)
        except ValueError:
            raise CommandError("Role must be an integer")
        options['role'] = role  
        # first_name
        first_name = options.get('first_name')
        if not first_name:
            raise CommandError("First_name is required")
        options['first_name'] = first_name
        # last_name
        last_name = options.get('last_name')
        if not last_name:
            raise CommandError("Last_name is required")
        options['last_name'] = last_name
        # id_user
        id_user = options.get('id_user')
        if not id_user:
            raise CommandError("Id_user is required")
        options['id_user'] = id_user
        super().handle(*args, **options)
        
