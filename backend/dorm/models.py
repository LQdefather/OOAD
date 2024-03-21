from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
import datetime

# Create your models here.

class Team(models.Model):
    name = models.CharField('队伍名称', max_length=50)
    leader = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lead_team', 
        verbose_name='队长'
        )

    def __str__(self):
        return "队伍" + self.name

    class Meta:
        verbose_name = '队伍'
        verbose_name_plural = verbose_name

class Build(models.Model):
    def photo_upload(self, filename):
        return f'buildings/{datetime.date.today().strftime("%Y/%m/%d")}/{filename}'

    ZONE = [
        ('first phase', '一期'),
        ('second phase', '二期'),
        ('Li Yuan', '荔园'),
        ('Xin Yuan', '欣园')
    ]

    # 区分是设施还是宿舍
    TYPE = [
        ('dormitory', '宿舍'),
        ('facility', '设施')
    ]

    name = models.CharField(
        '楼栋名称',
        max_length=30
    )
    zone = models.CharField(
        '地区',
        max_length=30,
        choices=ZONE
    )
    xlocation = models.FloatField(
        '经度',
        default=0
    )
    ylocation = models.FloatField(
        '纬度',
        default=0
    )
    buildingDetails = models.TextField('建筑详情', max_length=100, null=True, blank=True)
    photo = models.ImageField(
        "图片", upload_to=photo_upload, null=True, blank=True)
    type = models.CharField(
        '类型',
        max_length=30,
        default='dormitory'
    )

    def __str__(self):
        return self.zone + self.name + '栋'

    class Meta:
        verbose_name = '楼栋'
        verbose_name_plural = verbose_name


class Dormitory(models.Model):
    def floor_plan_upload(self, filename):
        return f'floorPlan/{datetime.date.today().strftime("%Y/%m/%d")}/{filename}'
    
    def room_layout_upload(self, filename):
        return f'roomLayout/{datetime.date.today().strftime("%Y/%m/%d")}/{filename}'
    
    def interiorImage_upload(self, filename):
        return f'interiorImage/{datetime.date.today().strftime("%Y/%m/%d")}/{filename}'

    SEX = [
        ('male', '男'),
        ('female', '女')
    ]

    TYPE = [
        ('single_room', '单人间'),
        ('double_room', '两人间'),
        ('triple_room', '三人间'),
        ('quadruple_room', '四人间')
    ]

    DEGREE = [
        ('master', '硕士生'),
        ('doctor', '博士生')
    ]

    buildingPosi = models.ForeignKey(
        Build,
        on_delete=models.CASCADE,
        related_name='dormitories_posi',
        verbose_name='楼栋'
    )
    type = models.CharField('房型', max_length=42, default='quadruple_room', choices=TYPE)
    floor = models.IntegerField('楼层')
    roomNumber = models.IntegerField('房间号')
    sex = models.CharField('性别', max_length=10, choices=SEX)
    bookMarkers = models.ManyToManyField(
        Team, 
        related_name='bookmarks', 
        verbose_name='收藏队伍',
        blank=True
        )
    start = models.DateTimeField('放出时间')
    end = models.DateTimeField('结束时间')
    floorPlan = models.ImageField(
        '楼层平面图',
        upload_to=floor_plan_upload,
        null=True,
        blank=True
    )
    roomLayout = models.ImageField(
        '房间布局图',
        upload_to=room_layout_upload,
        null=True,
        blank=True
    )
    interiorImage = models.ImageField(
        '室内图片',
        upload_to=interiorImage_upload,
        null=True,
        blank=True
    )
    degree = models.CharField('学历', max_length=20, choices=DEGREE, default='master')

    def __str__(self):
        return str(self.buildingPosi) + '房间 ' + str(self.floor) + str(self.roomNumber)

    class Meta:
        verbose_name = '房间'
        verbose_name_plural = verbose_name

class Comment(MPTTModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='用户'
    )
    comment = models.TextField(
        '内容',
        max_length=200
    )
    rating = models.IntegerField(
        '评分',
        default=5,
        choices=[(i, i) for i in range(6)]
    ) # 0 - 5 not 1 - 5
    dormitory = models.ForeignKey(
        Dormitory,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='宿舍'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='回复',
        blank=True,
        null=True
    )
    time = models.DateTimeField(
        "创建时间", 
        auto_now_add=True
    )

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name


class Selection(models.Model):
    team = models.OneToOneField(
        Team,
        on_delete=models.CASCADE,
        related_name='selection',
        verbose_name='队伍',
        help_text='成功选上房间的队伍'
    )
    dormitory = models.OneToOneField(
        Dormitory,
        on_delete=models.CASCADE,
        related_name='selection',
        verbose_name='宿舍',
        help_text='被选择的宿舍'
    )

    class Meta:
        verbose_name = '选择'
        verbose_name_plural = verbose_name


class ChatRoom(models.Model):
    def roomPhoto_upload(self, filename):
        return f'chatRooms/{datetime.date.today().strftime("%Y/%m/%d")}/{filename}'

    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField('房间名', max_length=20)
    photo = models.ImageField(
        "图片", upload_to=roomPhoto_upload, default='users/default.jpeg')

    class Meta:
        verbose_name = '聊天室'
        verbose_name_plural = verbose_name


class Message(MPTTModel):
    def messagePhoto_upload(self, filename):
        return f'messagePhotos/{datetime.date.today().strftime("%Y/%m/%d")}/{filename}'

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='队伍',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='用户'
    )
    text = models.TextField(
        '文本',
        max_length=200
    )
    photo = models.ImageField(
        "图片",
        upload_to=messagePhoto_upload,
        null=True,
        blank=True
    )
    time = models.DateTimeField(
        "创建时间", 
        auto_now_add=True
    )
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='回复'
    )

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = verbose_name