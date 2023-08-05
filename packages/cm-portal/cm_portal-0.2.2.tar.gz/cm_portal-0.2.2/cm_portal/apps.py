from django.apps import AppConfig

class CmPortalConfig(AppConfig):
    name = 'cm_portal'

    def ready(self):
        import cm_portal.signals
