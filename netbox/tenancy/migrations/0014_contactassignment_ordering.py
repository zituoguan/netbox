# Generated by Django 4.2.8 on 2024-01-17 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenancy', '0013_gfk_indexes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactassignment',
            options={'ordering': ('contact', 'priority', 'role', 'pk')},
        ),
    ]