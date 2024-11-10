# Generated by Django 5.1.3 on 2024-11-10 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_remove_book_user_ownedbook'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='shelf',
        ),
        migrations.AddField(
            model_name='ownedbook',
            name='shelf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='books.shelf'),
        ),
    ]