# Generated by Django 5.0.6 on 2024-05-29 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfa', '0004_alter_classcategory_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classinstance',
            name='weekday',
            field=models.CharField(choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], max_length=10),
        ),
    ]
