# Generated by Django 2.1.5 on 2019-05-03 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cm_portal', '0002_resident_philhealth'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['item_name'], 'permissions': (('can_view_csu', 'View CSU Database'),)},
        ),
    ]
