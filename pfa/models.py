from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
import logging

logger = logging.getLogger('pfa')

# Categories of the classes
class ClassCategory(models.Model):
    # Choice definition
    CLASS_CATEGORIES = [
        ("Striking", "Striking"),
        ("Grappling", "Grappling"),
        ("Fitness", "Fitness"),
        ("Lifestyle", "Lifestyle"),
    ]

    # Table field definition
    category = models.CharField(max_length=10, choices=CLASS_CATEGORIES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Custom methods
    def __str__(self):
        return self.category


# Training classes
class Class(models.Model):
    # Table field definition
    class_categories = models.ManyToManyField(ClassCategory)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.IntegerField(default=0)

    # Custom methods
    def __str__(self):
        return self.name


class ClassInstance(models.Model):
    # Choice definition
    DAY_OF_THE_WEEK = [
        ('1', "Monday"),
        ('2', "Tuesday"),
        ('3', "Wednesday"),
        ('4', "Thursday"),
        ('5', "Friday"),
        ('6', "Saturday"),
        ('7', "Sunday"),
    ]

    # Table field definition
    training_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=10, choices=DAY_OF_THE_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    time_span = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.training_class} | {self.get_weekday_display()} | {self.start_time} - {self.end_time}'
    
    def get_weekday_display(self):
        return dict(self.DAY_OF_THE_WEEK).get(self.weekday, "Unknown")


# Signal handlers for logging model operations
@receiver(pre_save, sender=ClassInstance)
def log_class_instance_pre_save(sender, instance, **kwargs):
    """Log before saving a ClassInstance"""
    if instance.pk:  # If this is an update
        try:
            old_instance = ClassInstance.objects.get(pk=instance.pk)
            changes = []
            
            # Compare fields to find changes
            if old_instance.training_class != instance.training_class:
                changes.append(f"training_class: {old_instance.training_class} -> {instance.training_class}")
            
            if old_instance.weekday != instance.weekday:
                changes.append(f"weekday: {old_instance.get_weekday_display()} -> {instance.get_weekday_display()}")
            
            if old_instance.start_time != instance.start_time:
                changes.append(f"start_time: {old_instance.start_time} -> {instance.start_time}")
            
            if old_instance.end_time != instance.end_time:
                changes.append(f"end_time: {old_instance.end_time} -> {instance.end_time}")
            
            logger.info(f"ABOUT TO UPDATE ClassInstance(pk={instance.pk}): {', '.join(changes)}")
            
        except ClassInstance.DoesNotExist:
            logger.warning(f"Attempted to update ClassInstance(pk={instance.pk}) but it doesn't exist")
    else:
        # This is a new instance
        logger.info(f"ABOUT TO CREATE ClassInstance: {instance.training_class} on {instance.get_weekday_display()} at {instance.start_time}-{instance.end_time}")

@receiver(post_save, sender=ClassInstance)
def log_class_instance_post_save(sender, instance, created, **kwargs):
    """Log after saving a ClassInstance"""
    if created:
        logger.info(f"CREATED ClassInstance(pk={instance.pk}): {instance}")
    else:
        logger.info(f"UPDATED ClassInstance(pk={instance.pk}): {instance}")

@receiver(pre_delete, sender=ClassInstance)
def log_class_instance_pre_delete(sender, instance, **kwargs):
    """Log before deleting a ClassInstance"""
    logger.info(f"ABOUT TO DELETE ClassInstance(pk={instance.pk}): {instance}")

@receiver(post_delete, sender=ClassInstance)
def log_class_instance_post_delete(sender, instance, **kwargs):
    """Log after deleting a ClassInstance"""
    logger.info(f"DELETED ClassInstance: {instance}")

# Similar signal handlers for Class model
@receiver(pre_save, sender=Class)
def log_class_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Class.objects.get(pk=instance.pk)
            if old_instance.name != instance.name:
                logger.info(f"ABOUT TO UPDATE Class(pk={instance.pk}): name: {old_instance.name} -> {instance.name}")
        except Class.DoesNotExist:
            logger.warning(f"Attempted to update Class(pk={instance.pk}) but it doesn't exist")
    else:
        logger.info(f"ABOUT TO CREATE Class: {instance.name}")

@receiver(post_save, sender=Class)
def log_class_post_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"CREATED Class(pk={instance.pk}): {instance.name}")
    else:
        logger.info(f"UPDATED Class(pk={instance.pk}): {instance.name}")

@receiver(pre_delete, sender=Class)
def log_class_pre_delete(sender, instance, **kwargs):
    logger.info(f"ABOUT TO DELETE Class(pk={instance.pk}): {instance.name}")

@receiver(post_delete, sender=Class)
def log_class_post_delete(sender, instance, **kwargs):
    logger.info(f"DELETED Class: {instance.name}")
