from django.conf import settings
from django.db import models

# Create your models here.

class MosTest(models.Model):
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="制作日", auto_now_add=True)
    updated_by = models.DateTimeField(verbose_name="更新日", auto_now=True)
    test_name = models.CharField(verbose_name="テスト名", max_length=100)
    description = models.TextField(verbose_name="テストの概要", blank=True, null=True)
    instruction = models.TextField(verbose_name="テストの指示", blank=True, null=True)

    def __str__(self):
        return self.test_name


class Acoustic(models.Model):
    def user_directory_path(instance, filename):
    # アップロード先のディレクトリを ユーザーごと/テストごと/ に変更する関数
        return f'file/user_{instance.mos_test.created_by}/test_{instance.mos_test.test_name}/{filename}'
    
    mos_test = models.ForeignKey(to=MosTest, on_delete=models.CASCADE)
    acoustic_model_name = models.CharField(verbose_name="音響モデル名", max_length=100)
    audio = models.FileField(upload_to=user_directory_path)
    text = models.TextField(verbose_name="トランスクリプト(複数ファイルの場合、改行文字で区切る)", blank=True, null=True)