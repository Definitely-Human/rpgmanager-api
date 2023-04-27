"""
Django command to wait for database to be available.
"""
from typing import Any, Optional
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args: Any, **options: Any):
        pass