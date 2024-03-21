from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from simpleui.admin import AjaxAdmin
from tablib import Dataset


admin.site.site_header = 'SUSDorm管理后台'  # 设置header
admin.site.site_title = 'SUSDorm管理后台'   # 设置title
admin.site.index_title = 'SUSDorm管理后台'

# Register your models here.

def is_xlsx(f):           
    first_four_bytes = f.read()[:4]     
    return first_four_bytes == b'PK\x03\x04' 

def is_xls(f):
    f.seek(512)
    bytes = f.read(8)
    f.seek(-512)
    return bytes==b'\x09\x08\x10\x00\x00\x06\x05\x00'

class UserAdmin(BaseUserAdmin, AjaxAdmin):
    
    actions = ['import_user']

    def import_user(self, request, queryset):
        upload = request.FILES['upload']
        dataset = Dataset()
        if(is_xlsx(upload)):
            data = dataset.load(upload, 'xlsx')
            if (data.headers!=['学工号', '姓名', '身份', '密码', '性别', '习惯', '学历']):
                return JsonResponse(data={
                    'status': 'error',
                    'msg': '上传文件格式错误',
                })
            for d in data.dict:
                print(d['学工号'])
                user = User.objects.create_user(
                    username = str(d['学工号']),
                    email = (str(d['学工号'])+"@sustech.edu.cn") if (d['身份']=='老师') else (str(d['学工号'])+"@mail.sustech.edu.cn"),
                    password = str(d['密码']),
                    is_staff= True if (d['身份']=='老师') else False
                )
                if (d['身份']=='老师'):
                    group = Group.objects.get(name='老师')
                    user.groups.add(group)
                else:
                    group = Group.objects.get(name='学生')
                    user.groups.add(group)
                models.Profile.objects.create(
                    user = user,
                    sid = str(d['学工号']),
                    name = d['姓名'],
                    sex = 'female' if d['性别'] == '女' else "male",
                    habits = d['习惯'],
                    degree = "doctor" if d['学历'] == '博士' else "master"
                )   
                
        else:
            return JsonResponse(data={
                    'status': 'error',
                    'msg': '请上传XLSX文件',
                })

    import_user.short_description = ' 批量导入'
    import_user.icon = 'el-icon-upload'
    import_user.type = 'info'
    import_user.enable = True
    import_user.layer = {
        'params': [{
            'type': 'file',
            'key': 'upload',
            'label': 'XLSX'
        }],
        'title': '从Excel上传用户',
        'tips': '请按指定的格式上传，系统将自动创建用户',
        'confirm_button': '导入',
        'cancel_button': '取消',
        'width': '40%',
        'labelWidth': "80px",
    }

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['sid', 'img', 'name', 'sex']
    list_filter = ['sex']
    search_field = ['sid', 'name', 'sex']

    @admin.display(description='头像', ordering='pk')
    def img(self, obj):
        div = f"<img src='{obj.avatar.url}' width='32px' alt='Avatar'>"
        return mark_safe(div)
    

@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'img', 'content', 'created_at']
    list_filter = ['created_at']
    search_field = ['content']

    @admin.display(description='用户', ordering='pk')
    def img(self, obj):
        div = f"<img src='{obj.user.profile.avatar.url}' width='32px' alt='Avatar'>"
        return mark_safe(div)