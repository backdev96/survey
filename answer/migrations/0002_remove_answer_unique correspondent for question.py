# Generated by Django 3.2.9 on 2021-11-21 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('answer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='answer',
            name='unique correspondent for question',
        ),
    ]
