# Generated by Django 5.1.1 on 2024-09-16 13:48

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_book_created_on_book_deleted_on_book_is_deleted_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteBooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_on', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_on', models.DateTimeField(default=None, null=True)),
                ('description', models.TextField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='users_interested_in', to='library.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='favorite_books', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
    ]
