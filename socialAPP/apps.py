from django.apps import AppConfig


class SocialappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'socialAPP'

    def ready(self):
    	import socialAPP.signals
