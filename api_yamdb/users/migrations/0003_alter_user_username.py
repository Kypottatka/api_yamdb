# Generated by Django 3.2 on 2023-01-29 09:37

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator], verbose_name='Никнейм пользователя'),
        ),
    ]
