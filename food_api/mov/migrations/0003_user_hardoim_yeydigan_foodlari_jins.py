# Generated by Django 4.0.4 on 2022-11-12 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mov', '0002_user_hardoim_yeydigan_foodlari_height_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_hardoim_yeydigan_foodlari',
            name='jins',
            field=models.CharField(choices=[('Erkak', 'Erkak'), ('Ayol', 'Ayol')], default='.', max_length=12),
        ),
    ]
