from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Crea un superusuario automáticamente'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@ejemplo.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✅ Superusuario creado exitosamente'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ El superusuario ya existe'))