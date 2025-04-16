from django.core.management.base import BaseCommand
from django.utils import timezone
from pfa.models import ClassInstance
import logging
import datetime

logger = logging.getLogger('pfa')

class Command(BaseCommand):
    help = 'Checks for class instances that have been modified recently'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days to look back for modifications'
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - datetime.timedelta(days=days)
        
        # Find all classes modified in the last N days
        modified_classes = ClassInstance.objects.filter(updated__gte=cutoff_date)
        
        if modified_classes.exists():
            self.stdout.write(f"Found {modified_classes.count()} classes modified in the last {days} days:")
            logger.info(f"AUDIT: Found {modified_classes.count()} classes modified in the last {days} days")
            
            for cls in modified_classes:
                self.stdout.write(f"  - {cls} (last updated: {cls.updated})")
                logger.info(f"AUDIT: Class {cls.pk} ({cls}) was last updated on {cls.updated}")
        else:
            self.stdout.write(f"No classes have been modified in the last {days} days.")
            logger.info(f"AUDIT: No classes have been modified in the last {days} days")