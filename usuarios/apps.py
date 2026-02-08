from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    name = 'usuarios'


    def ready(self):
        import usuarios.signals
