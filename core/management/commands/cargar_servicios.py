# BaseCommand: la clase base de Django para crear comandos propios de manage.py
from django.core.management.base import BaseCommand, CommandError
# User: el modelo de usuarios; el dueño de los servicios debe existir ya (tu superusuario)
from django.contrib.auth.models import User
# Servicio: el modelo de core/models.py
from core.models import Servicio

# DATOS: los 5 servicios de ejemplo; cámbialos desde /admin cuando quieras (título, descripción, precio, categoría)
DATOS = [
    ('Tutorías de programación', 'Clases personalizadas de Python y desarrollo web para principiantes.', '150.00', 'Tutorías'),
    ('Diseño de logotipos', 'Logotipo profesional con tres propuestas y archivos listos para imprimir.', '300.00', 'Diseño'),
    ('Repostería por encargo', 'Pasteles y postres para fiestas, con sabores y decoración a elección.', '120.00', 'Repostería'),
    ('Reparación de computadoras', 'Mantenimiento preventivo, limpieza y formateo de equipos.', '250.00', 'Soporte técnico'),
    ('Edición de video', 'Edición básica de videos cortos para redes sociales.', '200.00', 'Multimedia'),
]

# Command: Django busca esta clase al correr "python manage.py cargar_servicios"
class Command(BaseCommand):
    # help: el texto que aparece con "python manage.py cargar_servicios --help"
    help = 'Carga 5 servicios de ejemplo (equivale a darlos de alta en /admin). Se puede correr varias veces sin duplicar.'

    # add_arguments: opción para elegir el usuario dueño; si no se indica, se usa el primer superusuario
    def add_arguments(self, parser):
        parser.add_argument('--usuario', help='username del propietario (por defecto, el primer superusuario)')

    # handle: lo que se ejecuta al correr el comando
    def handle(self, *args, **opciones):
        # elige al propietario: el indicado, o el primer superusuario
        if opciones['usuario']:
            propietario = User.objects.filter(username=opciones['usuario']).first()
        else:
            propietario = User.objects.filter(is_superuser=True).order_by('id').first()
        # si no hay usuario, explica cómo crearlo en vez de fallar con un error confuso
        if propietario is None:
            raise CommandError('No hay usuario. Crea uno primero con: python manage.py createsuperuser')
        creados = 0
        for titulo, descripcion, precio, categoria in DATOS:
            # get_or_create: si ya existe un servicio con ese título y dueño, no lo duplica
            _, nuevo = Servicio.objects.get_or_create(
                propietario=propietario, titulo=titulo,
                defaults={'descripcion': descripcion, 'precio': precio, 'categoria': categoria},
            )
            creados += nuevo
        self.stdout.write(self.style.SUCCESS(f'Listo: {creados} servicios nuevos para "{propietario.username}" (total ahora: {Servicio.objects.count()}).'))
