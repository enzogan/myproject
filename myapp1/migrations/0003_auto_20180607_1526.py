# Generated by Django 2.0.4 on 2018-06-07 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0002_auto_20180606_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='date',
            field=models.DateField(max_length=200, verbose_name='Date'),
        ),
    ]
