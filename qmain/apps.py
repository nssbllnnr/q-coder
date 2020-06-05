from django.apps import AppConfig


class QmainConfig(AppConfig):
    name = 'qmain'

    def ready(self):
        import qmain.signals
