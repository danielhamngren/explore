# Generated by Django 3.1.2 on 2020-10-25 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0003_visit'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='places.places'),
        ),
    ]
