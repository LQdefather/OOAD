# Generated by Django 3.2.16 on 2023-12-24 12:13

import account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0004_auto_20231224_1212'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dorm', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.CharField(max_length=20, verbose_name='学工号')),
                ('name', models.CharField(default=None, max_length=50, verbose_name='真实姓名')),
                ('avatar', models.ImageField(default='users/default.jpeg', upload_to=account.models.Profile.avatar_upload, verbose_name='头像')),
                ('habits', models.TextField(max_length=100, verbose_name='习惯')),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], max_length=10, verbose_name='性别')),
                ('degree', models.CharField(choices=[('undergraduate', '本科生'), ('master', '硕士生'), ('doctor', '博士生')], default='undergraduate', max_length=20, verbose_name='学历')),
                ('sleep', models.TimeField(default='23:00', verbose_name='睡觉时间')),
                ('wake', models.TimeField(default='7:00', verbose_name='起床时间')),
                ('contact', models.CharField(default='', max_length=20, verbose_name='联系方式')),
                ('interests', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='兴趣爱好')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_profiles', to='dorm.team', verbose_name='队伍')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '个人形象',
                'verbose_name_plural': '个人形象',
            },
        ),
    ]
