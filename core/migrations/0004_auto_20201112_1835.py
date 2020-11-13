# Generated by Django 3.1.2 on 2020-11-12 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20201112_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.CharField(choices=[('Created', 'Created'), ('Validated', 'Validated'), ('Activated', 'Activated'), ('Cancelled', 'Cancelled'), ('Terminated', 'Terminated')], default='Created', max_length=10),
        ),
    ]
