# Generated by Django 5.1.4 on 2025-01-08 06:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('testapp', '0007_alter_acoustic_text'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='回答日')),
                ('mos', models.IntegerField(choices=[(None, '選択してください'), (1, '1 - 非常に不自然(bad)'), (2, '2 - 不自然(poor)'), (3, '3 - 普通(fair)'), (4, '4 - 自然(good)'), (5, '5 - 非常に自然(excellent)')])),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('target_audio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.acoustic')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='気づいたこと、疑問点、改善点ありましたらコメントお願いします。')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.mostest')),
            ],
        ),
    ]
