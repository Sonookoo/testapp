# Generated by Django 4.2.7 on 2023-12-01 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acousticapp', '0002_alter_answer_mos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='mos',
            field=models.IntegerField(choices=[(None, '選択してください'), (1, '1 - とても悪い'), (2, '2 - 悪い'), (3, '3 - どちらでもない'), (4, '4 - 良い'), (5, '5 - とても良い')]),
        ),
    ]
