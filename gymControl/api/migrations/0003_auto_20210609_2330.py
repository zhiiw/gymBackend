# Generated by Django 2.2.14 on 2021-06-09 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210609_2321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maintenance',
            old_name='id',
            new_name='ordinalNum',
        ),
        migrations.AlterField(
            model_name='student',
            name='classStart',
            field=models.DateTimeField(blank=True, db_column='classStart', null=True),
        ),
    ]
