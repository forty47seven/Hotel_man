# Generated by Django 4.0.4 on 2022-08-25 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('total', models.IntegerField(verbose_name='Amount available')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('check_in_date', models.DateField(default='0001-01-01', null=True)),
                ('book_date', models.DateField(default='0001-01-01', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=3)),
                ('status', models.CharField(choices=[('v', 'vacant'), ('o', 'occupied'), ('b', 'booked')], default='v', max_length=1)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.category')),
                ('occupant', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['room_number', 'category', 'status', 'occupant'],
            },
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hall', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('status', models.CharField(choices=[('v', 'vacant'), ('o', 'occupied'), ('b', 'booked')], default='v', max_length=1)),
                ('occupant', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GymUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_group', models.CharField(choices=[('d', 'diamond'), ('p', 'platinum'), ('g', 'gold')], max_length=1)),
                ('trainer', models.CharField(choices=[('t', 'Trent'), ('m', 'Mandy'), ('J', 'Jake'), ('b', 'Brad'), ('e', 'Erika')], max_length=1)),
                ('date_joined', models.DateField(auto_now=True)),
                ('subscription', models.CharField(choices=[('w', 'week'), ('m', 'month'), ('y', 'year')], max_length=1)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.customer')),
            ],
            options={
                'ordering': ['membership_group', 'trainer'],
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='hall',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.SET_DEFAULT, to='base.hall'),
        ),
        migrations.AddField(
            model_name='customer',
            name='room',
            field=models.ForeignKey(default=39, on_delete=django.db.models.deletion.SET_DEFAULT, to='base.room'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user_link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
