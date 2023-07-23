# Created by cetacs on 14.12.2020
from django.core.management import BaseCommand
from django.core.management import call_command
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.migrations.loader import MigrationLoader


class Command(BaseCommand):
    def handle(self, *args, **options):
        from backend.models import User
        if not User.objects.filter(email='admin@localhost').exists():
            User.objects.create_superuser(username='admin', password='123', email='admin@localhost', is_active=True)
        return self.style.NOTICE('DONE')
