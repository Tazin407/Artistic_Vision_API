# Generated by Django 5.0.3 on 2024-05-20 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='IGNname',
            field=models.CharField(max_length=20),
        ),
    ]
