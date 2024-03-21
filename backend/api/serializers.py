from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .utils.validators import validate_password
from dorm import models as dorm_models
from account import models as account_models
from taggit_serializer.serializers import (TagListSerializerField,
                                TaggitSerializer)
from django.utils import timezone
from taggit.models import Tag


class LoginSerializer(serializers.Serializer):
    """
    获取用户名和密码并尝试验证
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # 从request中拿到用户名和密码
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # 验证用户
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # 用户验证失败，提示，vailidationerror
                msg = '用户名或密码错误'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = '用户名和密码都需要填写'
            raise serializers.ValidationError(msg, code='authorization')
        # 如果用户，放在serializer都数据里
        # 在view中写
        attrs['user'] = user
        return attrs

class LogoutSerializer(serializers.Serializer):
    """
    获取用户名和密码并尝试验证
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    
# 用户修改密码的
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "两次密码输入的不一样"})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "旧密码输入不正确"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
    
class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = dorm_models.Build
        fields = ['id', 'name', 'zone', 'xlocation', 'ylocation', 'buildingDetails', 'photo', 'type']
        extra_kwargs = {
            'id': {'read_only': True},
        }


class DormSerializer(serializers.ModelSerializer):
    zone = serializers.CharField(source='buildingPosi.zone')
    building = serializers.CharField(source='buildingPosi.name')
    buildingId = serializers.IntegerField(source='buildingPosi.id')
    selected = serializers.SerializerMethodField()
    bookmarkTeamCount = serializers.SerializerMethodField()

    def get_selected(self, obj):
        # return true if the dorm is selected by the team
        select = dorm_models.Selection.objects.filter(dormitory=obj)
        if select.count() != 0:
            return True
        return False
    
    def get_bookmarkTeamCount(self, obj):
        # return the number of teams that bookmarked this dorm
        return obj.bookMarkers.count()

    class Meta:
        model = dorm_models.Dormitory
        # fields except bookMarkers
        fields = ['id', 'type', 'zone', 'building', 'buildingId', 'floor', 'roomNumber', 'sex', 'start', 'end', 'floorPlan', 'roomLayout', 'interiorImage', 'degree', 'selected', 
                  'bookmarkTeamCount']
        extra_kwargs = {
            'id': {'read_only': True},
        }


class CommentSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    userPk = serializers.SerializerMethodField()
    replyTo = serializers.SerializerMethodField()

    replyToUserAvatar = serializers.SerializerMethodField()
    replyToUserName = serializers.SerializerMethodField()

    dormZone = serializers.CharField(source='dormitory.buildingPosi.zone')
    dormBuilding = serializers.CharField(source='dormitory.buildingPosi.name')
    dormFloor = serializers.IntegerField(source='dormitory.floor')
    dormRoomNumber = serializers.CharField(source='dormitory.roomNumber')

    def get_avatar(self, obj):
        return obj.user.profile.avatar.url
    
    def get_name(self, obj):
        return obj.user.profile.name
    
    def get_userPk(self, obj):
        return obj.user.pk
    
    def get_replyTo(self, obj):
        # return id of the the comment that this comment replies to
        # the field is parent in the model
        if obj.parent:
            return obj.parent.id
        else:
            return None
        
    def get_replyToUserAvatar(self, obj):
        # return avatar of the user that this comment replies to
        if obj.parent:
            return obj.parent.user.profile.avatar.url
        else:
            return None
        
    def get_replyToUserName(self, obj):
        # return name of the user that this comment replies to
        if obj.parent:
            return obj.parent.user.profile.name
        else:
            return None

    class Meta:
        model = dorm_models.Comment
        fields = ['id', 'userPk', 'avatar', 'name', 'comment', 'rating', 'time', 'replyTo',
                  'replyToUserAvatar', 'replyToUserName', 'dormZone', 'dormBuilding', 'dormFloor', 'dormRoomNumber']
        extra_kwargs = {
            'id': {'read_only': True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    studentId = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    habits = serializers.CharField(source='profile.habits')
    sex = serializers.CharField(source='profile.sex')
    team = serializers.SerializerMethodField()
    sleep = serializers.TimeField(source='profile.sleep')
    wake = serializers.TimeField(source='profile.wake')
    contact = serializers.CharField(source='profile.contact')
    interests = serializers.SerializerMethodField()
    degree = serializers.CharField(source='profile.degree')

    def get_studentId(self, obj):
        return obj.profile.sid

    def get_avatar(self, obj):
        return obj.profile.avatar.url
    
    def get_name(self, obj):
        return obj.profile.name
    
    def get_team(self, obj):
        if obj.profile.team:
            return obj.profile.team.id
        else:
            return None
        
    def get_interests(self, obj):
        return obj.profile.interests.names()

    class Meta:
        model = User
        fields = ['pk', 'studentId', 'avatar', 'name', 'habits', 'sex', 'sleep', 'wake', 'contact', 'interests', 'team', 'degree']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = dorm_models.Comment
        fields = ['dormitory', 'user', 'comment', 'rating', 'parent']
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        comment = dorm_models.Comment.objects.create(**validated_data)
        # if the comment's parent is not None, which means the comment is a reply
        # then send a notification to the user who is replied
        if comment.parent:
            # content is the notification content, including under which dormitory and what the comment is
            content = '你收到了一条回复\n'
            content += '\n在宿舍：' + comment.dormitory.buildingPosi.name + '栋 ' + str(comment.dormitory.floor) + str(comment.dormitory.roomNumber)
            content += '\n评论内容：' + comment.comment
            account_models.Notification.objects.create(user=comment.parent.user, content=content)
        return comment
    
    def validate(self, attrs):
        # 验证用户
        user = self.context.get('request').user
        if not user:
            # 用户验证失败，提示，vailidationerror
            msg = '用户未登录'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
    
class ChangeAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar')
    class Meta:
        model = User
        fields = ['avatar']
        extra_kwargs = {
            'avatar': {'required': True},
        }

    def update(self, instance, validated_data):
        instance.profile.avatar = validated_data['profile']['avatar']
        instance.profile.save()
        return instance
    

class ChangeProfileSerializer(TaggitSerializer,serializers.ModelSerializer):
    habits = serializers.CharField(source='profile.habits')
    contact = serializers.CharField(source='profile.contact')
    sleep = serializers.TimeField(source='profile.sleep')
    wake = serializers.TimeField(source='profile.wake')
    interests = TagListSerializerField(source='profile.interests')

    class Meta:
        model = User
        fields = ['habits', 'contact', 'sleep', 'wake', 'interests']

    def update(self, instance, validated_data):
        instance.profile.habits = validated_data['profile']['habits']
        instance.profile.contact = validated_data['profile']['contact']
        instance.profile.sleep = validated_data['profile']['sleep']
        instance.profile.wake = validated_data['profile']['wake']
        # instance.profile.interests = validated_data['profile']['interests']
        for interest in instance.profile.interests.all():
            instance.profile.interests.remove(interest)
        for interest in validated_data['profile']['interests']:
            instance.profile.interests.add(interest)
        instance.profile.save()
        return instance
    

class TeamSerializer(serializers.ModelSerializer):
    leader = UserProfileSerializer(read_only=True)
    photo = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    def get_photo(self, obj):
        # return avatar of the leader
        return obj.leader.profile.avatar.url
    
    def get_members(self, obj):
        # return a list of members' profile
        members = account_models.Profile.objects.filter(team=obj)
        users = []
        for member in members:
            users.append(member.user)
        serializer = UserProfileSerializer(users, many=True)
        return serializer.data

    class Meta:
        model = dorm_models.Team
        fields = ['id', 'name', 'leader', 'photo', 'members']
        extra_kwargs = {
            'id': {'read_only': True},
        }

class TeamCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = dorm_models.Team
        fields = ['name', 'leader']
        extra_kwargs = {
            'leader': {'read_only': True},
        }

    def create(self, validated_data):
        team = dorm_models.Team.objects.create(**validated_data)
        user = self.context.get('request').user
        user.profile.team = team
        user.profile.save()
        return team
    
    def validate(self, attrs):
        # 验证用户
        user = self.context.get('request').user
        if not user:
            # 用户验证失败，提示，vailidationerror
            msg = '用户未登录'
            raise serializers.ValidationError(msg, code='authorization')
        if user.profile.team:
            msg = '用户已经在队伍中'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['leader'] = user
        return attrs
    

class LeaveTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = dorm_models.Team
        fields = ['id']
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        team = user.profile.team
        content = '你收到了一条通知\n'
        content += '\n' + user.username + ' ' + user.profile.name + '离开了队伍'
        for member in team.member_profiles.all():
            account_models.Notification.objects.create(user=member.user, content=content)
        if team.leader == user:
            team.delete()
        else:
            user.profile.team = None
            user.profile.save()

        return instance
    

class JoinTeamSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        # 验证用户
        user = self.context.get('request').user
        if not user:
            # 用户验证失败，提示，vailidationerror
            msg = '用户未登录'
            raise serializers.ValidationError(msg, code='authorization')
        if user.profile.team:
            msg = '用户已经在队伍中'
            raise serializers.ValidationError(msg, code='authorization')
        if dorm_models.Team.objects.filter(pk=attrs['id']).count() == 0:
            msg = '队伍不存在'
            raise serializers.ValidationError(msg, code='authorization')
        team = dorm_models.Team.objects.get(pk=attrs['id'])
        if account_models.Profile.objects.filter(team=team).count() >= 4:
            msg = '队伍人数已满'
            raise serializers.ValidationError(msg, code='authorization')
        # team leader gender should be the same as user
        if team.leader.profile.sex != user.profile.sex:
            msg = '队长性别与用户性别不符'
            raise serializers.ValidationError(msg, code='authorization')
        # team leader degree should be the same as user
        if team.leader.profile.degree != user.profile.degree:
            msg = '队长学历与用户学历不符'
            raise serializers.ValidationError(msg, code='authorization')
        return attrs

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        team = dorm_models.Team.objects.get(pk=validated_data['id'])
        user.profile.team = team
        user.profile.save()
        # 队员加入队伍后，队伍里的所有人都会收到一条通知
        content = '你收到了一条通知\n'
        content += '\n' + user.username + ' ' + user.profile.name + '加入了队伍'
        for member in team.member_profiles.all():
            account_models.Notification.objects.create(user=member.user, content=content)

        return instance
    
class UpdateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = dorm_models.Team
        fields = ['name']
        extra_kwargs = {
            'name': {'required': True},
        }

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()
        return instance
    
# bookmark a dormitory in team
class AddBookMarkDormSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        # 验证用户
        user = self.context.get('request').user
        if not user:
            # 用户验证失败，提示，vailidationerror
            msg = '用户未登录'
            raise serializers.ValidationError(msg, code='authorization')
        if not user.profile.team:
            msg = '用户不在队伍中'
            raise serializers.ValidationError(msg, code='authorization')
        if dorm_models.Dormitory.objects.filter(pk=attrs['id']).count() == 0:
            msg = '宿舍不存在'
            raise serializers.ValidationError(msg, code='authorization')
        # one team can only bookmark up to 5 dormitories
        team = user.profile.team
        if team.bookmarks.count() >= 5:
            msg = '队伍已经收藏了5个宿舍'
            raise serializers.ValidationError(msg, code='authorization')
        return attrs

    def update(self):
        user = self.context.get('request').user
        team = user.profile.team
        dorm = dorm_models.Dormitory.objects.get(pk=self.validated_data['id'])
        dorm.bookMarkers.add(team)
        dorm.save()
        return 
    
# unbookmark a dormitory in team
class UnBookMarkDormSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        # 验证用户
        user = self.context.get('request').user
        if not user:
            # 用户验证失败，提示，vailidationerror
            msg = '用户未登录'
            raise serializers.ValidationError(msg, code='authorization')
        if not user.profile.team:
            msg = '用户不在队伍中'
            raise serializers.ValidationError(msg, code='authorization')
        if dorm_models.Dormitory.objects.filter(pk=attrs['id']).count() == 0:
            msg = '宿舍不存在'
            raise serializers.ValidationError(msg, code='authorization')
        return attrs

    def update(self):
        user = self.context.get('request').user
        team = user.profile.team
        dorm = dorm_models.Dormitory.objects.get(pk=self.validated_data['id'])
        dorm.bookMarkers.remove(team)
        dorm.save()
        return 
    

class MessageSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    trueName = serializers.SerializerMethodField()
    currentUser = serializers.SerializerMethodField()
        
    def get_avatar(self, obj):
        return obj.user.profile.avatar.url
    
    def get_trueName(self, obj):
        return obj.user.profile.name
    
    def get_currentUser(self, obj):
        # if the message is sent by the current user, return true
        user = self.context.get('request').user
        if user == obj.user:
            return True
        else:
            return False
    

    class Meta:
        model = dorm_models.Message
        fields = ['user', 'avatar', 'trueName', 'text', 'photo', 'time', 'currentUser']


class SendMessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    photo = serializers.ImageField(required=False)
    parent = serializers.IntegerField(required=False)

    class Meta:
        model = dorm_models.Message
        fields = ['user', 'text', 'photo', 'parent']
        extra_kwargs = {
            'user': {'read_only': True},
        }


    def create(self, validated_data):
        message = dorm_models.Message.objects.create(**validated_data)
        return message
    
    def validate(self, attrs):
        # 验证用户
        user = self.context.get('request').user
        if not user:
            # 用户验证失败，提示，vailidationerror
            msg = '用户未登录'
            raise serializers.ValidationError(msg, code='authorization')
        team = user.profile.team
        if not team:
            msg = '用户不在队伍中'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        attrs['team'] = team
        return attrs
    

class SelectDormSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        # check whther the dorm exists or selected
        if dorm_models.Dormitory.objects.filter(pk=attrs['id']).count() == 0:
            msg = '宿舍不存在'
            raise serializers.ValidationError(msg, code='authorization')
        dorm = dorm_models.Dormitory.objects.get(pk=attrs['id'])
        if dorm_models.Selection.objects.filter(dormitory=dorm).count() != 0:
            msg = '宿舍已经被选择'
            raise serializers.ValidationError(msg, code='authorization')
        # if the user is the leader of the team then the leader can select dorm
        user = self.context.get('request').user
        team = user.profile.team
        if not team:
            msg = '用户不在队伍中，请先加入队伍'
            raise serializers.ValidationError(msg, code='authorization')
        # if team.leader != user:
        #     msg = '用户不是队长，只有队长可以选择宿舍'
        #     raise serializers.ValidationError(msg, code='authorization')
        if dorm not in team.bookmarks.all():
            msg = '宿舍不在队伍收藏中'
            raise serializers.ValidationError(msg, code='authorization')
        select = dorm_models.Selection.objects.filter(team=team)
        if select.count() != 0:
            msg = '用户已经选择过宿舍'
            raise serializers.ValidationError(msg, code='authorization')
        # whether num of people match
        num_people = account_models.Profile.objects.filter(team=team).count()
        capacity = 0
        if dorm.type == 'double_room':
            capacity = 2
        elif dorm.type == 'single_room':
            capacity = 1
        elif dorm.type == 'quadruple_room':
            capacity = 4
        elif dorm.type == 'triple_room':
            capacity = 3
        if num_people != capacity:
            msg = '队伍人数与宿舍容量不符'
            raise serializers.ValidationError(msg, code='authorization')
        if user.profile.sex != dorm.sex:
            msg = '用户性别与宿舍性别不符'
            raise serializers.ValidationError(msg, code='authorization')
        # if degree doesn't match
        if user.profile.degree != dorm.degree:
            msg = '用户学历与宿舍学历不符'
            raise serializers.ValidationError(msg, code='authorization')
        # check whther the dorm is in the select time
        start = dorm.start
        end = dorm.end
        # if now is not in the select time
        timezone.activate("Asia/Shanghai")
        now = timezone.now()

        if now < start or now > end:
            msg = '现在不在选择时间内'
            raise serializers.ValidationError(msg, code='authorization')
        return attrs
            

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        team = user.profile.team
        dorm = dorm_models.Dormitory.objects.get(pk=validated_data['id'])
        dorm_models.Selection.objects.create(team=team, dormitory=dorm)
        return instance
    
    def save(self):
        self.update(self.instance, self.validated_data)
        return self.instance
    

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = account_models.Notification
        fields = ['id', 'content', 'created_at']
        extra_kwargs = {
            'id': {'read_only': True},
        }


# get avatar of a user, receive pk of the user, return avatar url
class AvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        return obj.profile.avatar.url

    class Meta:
        model = User
        fields = ['avatar']
        extra_kwargs = {
            'avatar': {'read_only': True},
        }

    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        extra_kwargs = {
            'id': {'read_only': True},
        }


class UserCommentsSerializer(serializers.Serializer):
    pk = serializers.IntegerField()