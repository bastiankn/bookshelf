# Generated by Django 5.1.3 on 2024-11-14 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_book_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(blank=True, upload_to='book_covers/'),
        ),
    ]
