# Generated by Django 3.2.7 on 2021-12-13 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codefun', '0004_code_postchoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='name',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]