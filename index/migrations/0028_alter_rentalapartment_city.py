# Generated by Django 3.2.7 on 2023-05-24 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0027_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentalapartment',
            name='city',
            field=models.CharField(max_length=255),
        ),
    ]
