from django.db import models
from django.conf import settings
import datetime
from dorm.models import Team
from taggit.managers import TaggableManager

# Create your models here.

class Profile(models.Model):
    def avatar_upload(self, filename):
        return f'users/{self.user}/{datetime.date.today().strftime("%Y/%m/%d")}/{filename}'

    SEX = [
        ('male', '男'),
        ('female', '女'),
    ]

    DEGREE = [
        ('undergraduate', '本科生'),
        ('master', '硕士生'),
        ('doctor', '博士生')
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    sid = models.CharField('学工号', max_length=20)
    name = models.CharField('真实姓名',
        max_length=50, default=user.name)
    avatar = models.ImageField(
        "头像", upload_to=avatar_upload, default='users/default.jpeg')
    habits = models.TextField("习惯", max_length=100)
    sex = models.CharField('性别', choices=SEX, max_length=10)
    degree  = models.CharField('学历', choices=DEGREE, max_length=20, default='undergraduate')
    sleep = models.TimeField('睡觉时间', default='23:00')
    wake = models.TimeField('起床时间', default='7:00')
    interests = TaggableManager('兴趣爱好', blank=True)
    contact = models.CharField('联系方式', max_length=20, default='')
    team = models.ForeignKey(Team, verbose_name="队伍", related_name="member_profiles", on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'

    class Meta:
        verbose_name = '个人形象'
        verbose_name_plural = verbose_name

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', verbose_name='用户')
    content = models.TextField('通知内容')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return f'Notification for user {self.user.username}'

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']