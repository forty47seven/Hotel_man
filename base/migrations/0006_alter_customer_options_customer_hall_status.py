# Generated by Django 4.0.4 on 2022-08-30 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_customer_gym_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['full_name']},
        ),
        migrations.AddField(
            model_name='customer',
            name='hall_status',
            field=models.BooleanField(default=False),
        ),
    ]
