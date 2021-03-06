# Generated by Django 3.0.8 on 2021-06-21 18:36

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('item', '0001_initial'),
        ('restaurant', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('updated_by', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('number_of_votes', models.IntegerField(blank=True, default=0, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.Item')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Restaurant')),
            ],
            options={
                'db_table': 'vote_results',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('updated_by', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('deleted', 'deleted')], default='active', max_length=30)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.Item')),
            ],
            options={
                'db_table': 'votes',
            },
        ),
    ]
