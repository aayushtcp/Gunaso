from django.apps import AppConfig


class GunasoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gunasoApp'

    # def ready(self):
    #     import gunasoApp.signals
