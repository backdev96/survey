# Generated by Django 3.2.9 on 2021-11-20 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_alter_answer_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='option',
            new_name='answer',
        ),
    ]
