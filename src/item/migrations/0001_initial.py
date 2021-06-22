# Generated by Django 3.0.8 on 2021-06-21 18:36

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('updated_by', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('name', models.CharField(max_length=50)),
                ('week_day', models.CharField(choices=[('sunday', 'sunday'), ('monday', 'monday'), ('tuesday', 'tuesday'), ('wednesday', 'wednesday'), ('thursday', 'thursday'), ('friday', 'friday'), ('saturday', 'saturday')], default='sunday', max_length=50)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('status', models.CharField(choices=[('active', 'active'), ('archived', 'archived'), ('deleted', 'deleted')], default='active', max_length=30)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Restaurant')),
            ],
            options={
                'verbose_name': 'Menu Hour',
                'verbose_name_plural': 'Menu Hours',
                'db_table': 'menu_hours',
                'unique_together': {('restaurant', 'name', 'week_day')},
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('updated_by', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('name', models.CharField(max_length=255)),
                ('image', models.TextField(blank=True, null=True)),
                ('price', models.FloatField()),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('deleted', 'deleted')], default='inactive', max_length=30)),
                ('menu_hours', models.ManyToManyField(to='item.MenuHours')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Restaurant')),
            ],
            options={
                'db_table': 'items',
            },
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['-created_at'], name='items_created_1ba901_idx'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['status'], name='items_status_bc9bcb_idx'),
        ),
    ]
