# Generated by Django 4.2.7 on 2023-12-01 16:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0005_alter_mostest_description_alter_mostest_instruction'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('acousticapp', '0003_alter_answer_mos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='今回のテストで何かコメントありましたらお書きください！')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.mostest')),
            ],
        ),
    ]
