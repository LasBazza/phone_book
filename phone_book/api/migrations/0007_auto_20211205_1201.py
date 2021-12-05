# Generated by Django 3.1 on 2021-12-05 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20211205_1133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='companies_can_edit',
            new_name='rights_to_edit_companies',
        ),
        migrations.AlterField(
            model_name='employee',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='api.company', verbose_name='Организация'),
        ),
    ]