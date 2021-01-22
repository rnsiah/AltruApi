# Generated by Django 3.1.5 on 2021-01-12 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210112_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='balance',
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Balance',
                'verbose_name_plural': 'Balances',
            },
        ),
    ]
