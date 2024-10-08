# Generated by Django 5.1.1 on 2024-09-16 18:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_favoritebooks'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimilarityMatrix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similarity', models.FloatField(db_index=True)),
                ('large_book_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='similarity_matrix_2', to='library.book')),
                ('small_book_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='similarity_matrix', to='library.book')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
    ]
