# Generated by Django 3.1.5 on 2021-01-08 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qrs'),
        ),
    ]