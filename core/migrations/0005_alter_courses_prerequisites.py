# Generated by Django 5.0.4 on 2024-05-05 13:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_courses_prerequisites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='prerequisites',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.courses'),
        ),
    ]