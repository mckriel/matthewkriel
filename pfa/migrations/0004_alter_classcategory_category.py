# Generated by Django 5.0.6 on 2024-05-28 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfa', '0003_alter_classinstance_weekday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classcategory',
            name='category',
            field=models.CharField(choices=[('Striking', 'Striking'), ('Grappling', 'Grappling'), ('Fitness', 'Fitness'), ('Lifestyle', 'Lifestyle')], max_length=10),
        ),
    ]
