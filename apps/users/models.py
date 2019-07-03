from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICE_LEVEL = {
    ('5队', '5队'),
    ('6队', '6队'),
    ('7队', '7队'),
    ('8队', '8队'),
}


# Create your models here.
class UserProfile(AbstractUser):
    # 姓名 手机 备用号码 分组 行业 openid
    name = models.CharField(max_length=150, verbose_name='姓名', null=True, blank=True)
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    backup_m = models.CharField(max_length=11, verbose_name='备份手机号', null=True, blank=True)
    group = models.CharField(max_length=10, verbose_name='分组')
    work = models.CharField(max_length=32, null=True, blank=True, verbose_name='行业')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='注册时间')
    openid = models.CharField(max_length=50, verbose_name='openid', null=True, blank=True, )
    # is_active = models.BooleanField(default=False, verbose_name='是否审核')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

class NoteInfo(models.Model):
    content = models.TextField(verbose_name='公告内容')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = '公告管理'
        verbose_name_plural = verbose_name

class FeedBackInfo(models.Model):
    content = models.TextField(verbose_name='反馈内容')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name='用户')
    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = '反馈管理'
        verbose_name_plural = verbose_name