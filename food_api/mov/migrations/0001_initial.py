# Generated by Django 4.0.4 on 2022-11-12 16:19

from django.db import migrations, models
import multiselectfield.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_bugun_yegan_foodlari',
            fields=[
                ('food_name', multiselectfield.db.fields.MultiSelectField(choices=[('Olma', 'Olma'), ('Tarvuz', 'Tarvuz'), ('Limon', 'Limon')], default='None', max_length=10)),
                ('ichimliklar', multiselectfield.db.fields.MultiSelectField(choices=[('suv', 'suv'), ('Cola', 'Cola'), ('Gazli ichimlik', 'Gazli ichimlik')], default='None', max_length=23)),
                ('user', models.CharField(blank=True, default='None', max_length=400)),
                ('id_si', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sana', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User_Hardoim_Yeydigan_Foodlari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', multiselectfield.db.fields.MultiSelectField(choices=[('Olma', 'Olma'), ('Tarvuz', 'Tarvuz'), ('Limon', 'Limon')], default='None', max_length=10)),
                ('ichimliklar', multiselectfield.db.fields.MultiSelectField(choices=[('suv', 'suv'), ('Cola', 'Cola'), ('Gazli ichimlik', 'Gazli ichimlik')], default='None', max_length=23)),
                ('Qancha_kaloriya', models.DecimalField(decimal_places=0, default='0', max_digits=34, null=True)),
                ('user', models.CharField(blank=True, default='None', max_length=400)),
            ],
            options={
                'verbose_name': 'User_hardoim_food',
            },
        ),
    ]
