# Generated by Django 4.2.4 on 2023-08-16 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientId', models.TextField()),
                ('symbol', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='ScripMaster',
        ),
    ]