# Generated by Django 5.0.4 on 2024-04-19 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_attendees_alter_customuser_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]