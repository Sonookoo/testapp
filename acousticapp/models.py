from django.conf import settings
from django.db import models

from testapp.models import Acoustic, MosTest

class Answer(models.Model):
    MOS_CHOICES = [
        (None, '選択してください'),
        (1, '1 - 非常に不自然(bad)'),
        (2, '2 - 不自然(poor)'),
        (3, '3 - 普通(fair)'),
        (4, '4 - 自然(good)'),
        (5, '5 - 非常に自然(excellent)'),
    ]
    target_audio = models.ForeignKey(to=Acoustic, on_delete=models.CASCADE)
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="回答日", auto_now_add=True)
    mos = models.IntegerField(choices=MOS_CHOICES, blank=False, null=False)

class Comment(models.Model):
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(to=MosTest, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="気づいたこと、疑問点、改善点ありましたらコメントお願いします。", blank=True, null=True)