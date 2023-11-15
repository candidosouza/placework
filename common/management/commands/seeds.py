from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write('Deleting existing data...')
            # Limpa os dados existentes
            call_command('flush', interactive=False)

            self.stdout.write('Seeding data...')

            # Chamar diferentes scripts de seed para cada app
            exec(open('placework/fixtures/seeds.py').read())
            # Adicione outras chamadas de seed para outros apps

            self.stdout.write('Data seeded successfully.')
        except Exception as e:
            raise e
            self.stderr.write(f'Error seeding data: {e}')
