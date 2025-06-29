# Generated by Django 3.2.7 on 2023-05-10 09:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('index', '0016_auto_20230503_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentalapartment',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rentalapartment',
            name='animalsAllowed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='index.animalsallowed'),
        ),
        migrations.AlterField(
            model_name='rentalapartment',
            name='availableFrom',
            field=models.DateField(default=datetime.date(2023, 5, 10)),
        ),
        migrations.AlterField(
            model_name='rentalapartment',
            name='rentalPeriod',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='rentalapartment',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='index.apartmenttype'),
        ),
    ]
