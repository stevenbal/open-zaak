from django.apps import AppConfig


class ZakenConfig(AppConfig):
    name = "openzaak.components.zaken"

    def ready(self):
        # load the signal receivers
        from . import signals  # noqa
