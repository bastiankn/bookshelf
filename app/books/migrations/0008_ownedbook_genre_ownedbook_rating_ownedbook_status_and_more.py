# Generated by Django 5.1.3 on 2024-11-14 14:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_alter_book_cover_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ownedbook',
            name='genre',
            field=models.CharField(blank=True, choices=[('fantasy', 'Fantasy'), ('sci-fi', 'Sci-Fi'), ('romance', 'Romance'), ('mystery', 'Mystery'), ('thriller', 'Thriller'), ('non-fiction', 'Non-Fiction'), ('horror', 'Horror'), ('historical', 'Historical'), ('biography', 'Biography'), ('poetry', 'Poetry')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='ownedbook',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ownedbook',
            name='status',
            field=models.CharField(choices=[('unread', 'Unread'), ('reading', 'Currently Reading'), ('read', 'Read'), ('dtf', 'Didn`t Finish')], default='unread', max_length=20),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=15, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ownedbook',
            name='tags',
            field=models.ManyToManyField(blank=True, to='books.tag'),
        ),
    ]
