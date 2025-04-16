from django.core.management.base import BaseCommand
from django.utils import timezone
from pfa.models import ClassInstance
from django.db.models import F
import logging
import datetime
import json

logger = logging.getLogger('pfa')

class Command(BaseCommand):
    help = 'Detects any unexpected changes to class schedules'

    def handle(self, *args, **options):
        self.stdout.write("Running schedule change detection...")
        logger.info("AUDIT: Running schedule change detection")
        
        # Get all current classes
        current_classes = {}
        for cls in ClassInstance.objects.all():
            key = f"{cls.pk}"
            current_classes[key] = {
                'training_class': cls.training_class.name,
                'weekday': cls.weekday,
                'start_time': cls.start_time.strftime('%H:%M:%S'),
                'end_time': cls.end_time.strftime('%H:%M:%S'),
                'updated': cls.updated.isoformat(),
            }
        
        # Check if we have a previous snapshot to compare against
        try:
            with open('logs/schedule_snapshot.json', 'r') as f:
                previous_snapshot = json.load(f)
                
                # Compare current with previous
                for key, previous_data in previous_snapshot.items():
                    if key in current_classes:
                        current_data = current_classes[key]
                        
                        # Check for changes
                        changes = []
                        if previous_data['training_class'] != current_data['training_class']:
                            changes.append(f"training_class: {previous_data['training_class']} -> {current_data['training_class']}")
                        
                        if previous_data['weekday'] != current_data['weekday']:
                            changes.append(f"weekday: {previous_data['weekday']} -> {current_data['weekday']}")
                        
                        if previous_data['start_time'] != current_data['start_time']:
                            changes.append(f"start_time: {previous_data['start_time']} -> {current_data['start_time']}")
                        
                        if previous_data['end_time'] != current_data['end_time']:
                            changes.append(f"end_time: {previous_data['end_time']} -> {current_data['end_time']}")
                        
                        if changes:
                            self.stdout.write(f"Detected changes to class {key}:")
                            for change in changes:
                                self.stdout.write(f"  - {change}")
                            
                            logger.warning(f"SCHEDULE CHANGE DETECTED: Class {key} changed: {', '.join(changes)}")
                    else:
                        # Class was deleted
                        self.stdout.write(f"Class {key} ({previous_data['training_class']}) was deleted")
                        logger.warning(f"SCHEDULE CHANGE DETECTED: Class {key} ({previous_data['training_class']}) was deleted")
                
                # Check for new classes
                for key in current_classes:
                    if key not in previous_snapshot:
                        self.stdout.write(f"New class detected: {key} ({current_classes[key]['training_class']})")
                        logger.info(f"SCHEDULE CHANGE DETECTED: New class {key} ({current_classes[key]['training_class']})")
                        
        except FileNotFoundError:
            self.stdout.write("No previous snapshot found. Creating initial snapshot.")
            logger.info("AUDIT: Creating initial schedule snapshot")
        except Exception as e:
            self.stdout.write(f"Error comparing snapshots: {str(e)}")
            logger.error(f"AUDIT ERROR: Failed to compare schedule snapshots: {str(e)}", exc_info=True)
            
        # Always save current snapshot
        try:
            # Ensure logs directory exists
            import os
            os.makedirs('logs', exist_ok=True)
            
            with open('logs/schedule_snapshot.json', 'w') as f:
                json.dump(current_classes, f, indent=2)
                self.stdout.write("Schedule snapshot saved")
                logger.info("AUDIT: Schedule snapshot saved")
        except Exception as e:
            self.stdout.write(f"Error saving snapshot: {str(e)}")
            logger.error(f"AUDIT ERROR: Failed to save schedule snapshot: {str(e)}", exc_info=True)