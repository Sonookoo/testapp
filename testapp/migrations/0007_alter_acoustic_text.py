# Generated by Django 5.1.4 on 2025-01-08 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0006_acoustic_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acoustic',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='トランスクリプト(複数ファイルの場合、改行文字で区切る)'),
        ),
    ]
