# Generated by Django 2.1.7 on 2019-04-01 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autotext', '0003_auto_20190319_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='webography',
            name='name',
            field=models.TextField(default='Webography <built-in function id>', null=True),
        ),
    ]
