# Generated by Django 5.1.7 on 2025-05-04 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='cart', max_length=20),
        ),
    ]
