from django.db import models


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
        return f'{self.training_class} | {self.weekday} | {self.start_time} - {self.end_time}'
