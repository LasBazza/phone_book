# Generated by Django 3.1 on 2021-12-05 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20211205_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='companies_can_edit',
            field=models.ManyToManyField(blank=True, to='api.Company', verbose_name='Компании, которые юзер имеет право редактировать'),
        ),
    ]
