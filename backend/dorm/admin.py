from django.contrib import admin
from . import models
from import_export.admin import ExportActionModelAdmin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from django.shortcuts import render
from django.http import HttpResponseRedirect
import datetime
from django.utils import timezone
from django.utils.safestring import mark_safe

# Register your models here.

@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader']
    search_fields = ['name']

@admin.register(models.Build)
class BuildAdmin(admin.ModelAdmin):
    list_filter = ['zone']
    list_display = ['name', 'zone', 'xlocation', 'ylocation']
    search_fields = ['name', 'xlocation', 'ylocation']


@admin.register(models.Dormitory)
class DormitoryAdmin(admin.ModelAdmin):
    list_filter = ['buildingPosi', 'type', 'sex']
    list_display = ['roomNumber', 'buildingPosi', 'type', 'sex']
    # list_filter = ['type', 'sex']
    # list_display = ['roomNumber', 'type', 'sex']
    search_fields = ['roomNumber']

    # 增加按钮，支持批量修改时间
    actions = ['open_time', 'close_time']  

    def open_time(self, request, queryset):
        if 'apply' in request.POST:
            open_time = request.POST['open_time']
            format_string = '%Y-%m-%dT%H:%M'
            # convert to datetime
            open_time = datetime.datetime.strptime(open_time, format_string)
            open_time = timezone.make_aware(open_time, timezone=timezone.get_current_timezone())
            count = 0
            for dorm_pk in request.POST['dorm'].split(','):
                if dorm_pk != '':
                    dorm = models.Dormitory.objects.get(pk=dorm_pk)
                    dorm.start = open_time
                    dorm.save()
                    count += 1
            self.message_user(request,
                              "Changed open time on {} rooms.".format(count))
            return HttpResponseRedirect(request.get_full_path())
    
        return render(
            request,
            'open_time.html',
            context={'queryset': queryset
                     }
        )
        # queryset.update(type='A')
    open_time.short_description = "修改开放时间"

    def close_time(self, request, queryset):
        if 'apply' in request.POST:
            close_time = request.POST['close_time']
            format_string = '%Y-%m-%dT%H:%M'
            # convert to datetime
            close_time = datetime.datetime.strptime(close_time, format_string)
            close_time = timezone.make_aware(close_time, timezone=timezone.get_current_timezone())
            count = 0
            for dorm_pk in request.POST['dorm'].split(','):
                if dorm_pk != '':
                    dorm = models.Dormitory.objects.get(pk=dorm_pk)
                    dorm.end = close_time
                    dorm.save()
                    count += 1
            self.message_user(request,
                              "Changed close time on {} rooms.".format(count))
            return HttpResponseRedirect(request.get_full_path())
    
        return render(
            request,
            'close_time.html',
            context={'queryset': queryset
                     }
        )
    close_time.short_description = "修改关闭时间"


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'img', 'dormitory', 'comment', 'rating', 'time', 'parent']
    search_fields = ['text']
    list_filter = ['dormitory', 'rating']

    @admin.display(description='用户', ordering='pk')
    def img(self, obj):
        div = f"<img src='{obj.user.profile.avatar.url}' width='32px' alt='Avatar'>"
        return mark_safe(div)

class SelectionResource(resources.ModelResource):
    team = fields.Field(
        column_name='team',
        attribute='team',
        widget=ForeignKeyWidget(models.Team, 'name')
    )
    dormitory = fields.Field()

    class Meta:
        model = models.Selection
        fields = ('team', 'dormitory')

    def dehydrate_dormitory(self, select):
        return select.dormitory.__str__()

@admin.register(models.Selection)
class SelectionAdmin(ExportActionModelAdmin):
    resource_classes = [SelectionResource]

    list_display = ['pk', 'team', 'dormitory']


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'team', 'img', 'text', 'time']
    search_field = ['text']
    list_filter = ['team']

    @admin.display(description='用户', ordering='pk')
    def img(self, obj):
        div = f"<img src='{obj.user.profile.avatar.url}' width='32px' alt='Avatar'>"
        return mark_safe(div)