from django.shortcuts import render
from rest_framework import permissions, views, status, generics, viewsets
from .serializers import LoginSerializer
from . import serializers
from django.contrib.auth import login, logout
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from dorm import models as dorm_models
from account import models as account_models
from django.http import Http404
from django.contrib.sessions.models import Session
from django.utils import timezone
from taggit.models import Tag
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# Create your views here.

class LoginView(views.APIView):
    # 如果用户没登录也可以访问这一个，所以要设置一下谁可以访问
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Close or delete existing sessions for the user
        # 有可能是用户在别的地方登录了，所以要把之前的session都删掉
        # 这样就不会出现一个用户在两个地方登录的情况了
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in sessions:
            if str(user.pk) == session.get_decoded().get('_auth_user_id'):
                session.delete()

        login(request, user)
        self.request.session.set_expiry(0)

        if not request.session.exists(request.session.session_key):
            request.session.create()

        # return pk and session id
        loginResponse = {
            'pk': user.pk,
            'sessionid': request.session.session_key,
        }
        return Response(data=loginResponse, status=status.HTTP_200_OK)

# 用户登出
class LogoutAPI(views.APIView):

    serializer_class = serializers.LogoutSerializer

    def get(self, request, format=None):
        # using Django logout
        # 因为咱们是存在session里的嘛，所以得用django的
        logout(request)
        return Response(status=status.HTTP_200_OK)

class ChangePasswordView(generics.UpdateAPIView):
    # 注意，默认是登录了之后才能调用这些api，所以不用担心安全问题
    # 这是我们在settings里的设置

    queryset = User.objects.all()
    serializer_class = serializers.ChangePasswordSerializer

# list all buildings
# api with get method
# /api/buildings/
class BuildViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = dorm_models.Build.objects.all()
    serializer_class = serializers.BuildSerializer
    

# dorm view read only
class DormViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = dorm_models.Dormitory.objects.all()
    serializer_class = serializers.DormSerializer

# get comments according to dorm id
class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = dorm_models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        queryset = dorm_models.Comment.objects.all()
        dorm_id = self.request.query_params.get('dorm_id', None)
        # query params is like ?dorm_id=1
        if dorm_id is not None:
            queryset = queryset.filter(dormitory__id=dorm_id)
        return queryset
    

# user information
# get /api/user-information/
# with params: pk
class UserInformationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        pk = self.request.query_params.get('pk', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
            if queryset is None:
                raise Http404("No user matches the given query.")
        return queryset
    

# create a comment
# api with post method
# /api/create-comment/
class CommentCreateView(views.APIView):
    serializer_class = serializers.CommentCreateSerializer

    def post(self, request, format=None):
        serializer = serializers.CommentCreateSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

# change user habits in profile
# api with post method
# /api/change-habits/
class ChangeAvatarView(views.APIView):
    serializer_class = serializers.ChangeAvatarSerializer

    def post(self, request, format=None):
        serializer = serializers.ChangeAvatarSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.update(self.request.user, serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

# change user avatar in profile
# api with post method
# /api/change-avatar/
class ChangeProfileView(views.APIView):
    serializer_class = serializers.ChangeProfileSerializer

    def post(self, request, format=None):
        serializer = serializers.ChangeProfileSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.update(self.request.user, serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
# all teams information view
# api with get method
# /api/teams/
class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = dorm_models.Team.objects.all()
    serializer_class = serializers.TeamSerializer


# create a team
# api with post method
# /api/create-team/
class TeamCreateView(views.APIView):
    serializer_class = serializers.TeamCreateSerializer

    def post(self, request, format=None):
        serializer = serializers.TeamCreateSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

# leave team
# api with post method
# /api/leave-team/
class LeaveTeamView(views.APIView):
    serializer_class = serializers.LeaveTeamSerializer

    def post(self, request, format=None):
        serializer = serializers.LeaveTeamSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.update(self.request.user, serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

# join team if the team number is less than 4
# api with post method
# /api/join-team/
class JoinTeamView(views.APIView):
    serializer_class = serializers.JoinTeamSerializer

    def post(self, request, format=None):
        serializer = serializers.JoinTeamSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.update(self.request.user, serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class UpdateTeamView(views.APIView):
    serializer_class = serializers.UpdateTeamSerializer

    def post(self, request, format=None):
        serializer = serializers.UpdateTeamSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        team = user.profile.team
        serializer.update(team, serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

class BookMarkDormView(views.APIView):
    serializer_class = serializers.AddBookMarkDormSerializer

    def post(self, request, format=None):
        serializer = serializers.AddBookMarkDormSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.update()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class UnBookMarkDormView(views.APIView):
    serializer_class = serializers.UnBookMarkDormSerializer

    def post(self, request, format=None):
        serializer = serializers.UnBookMarkDormSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.update()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

class AllBookMarkDormView(views.APIView):

    def get_dorms(self, request):
        user = request.user
        team = user.profile.team
        if not team:
            # if user has no team, return empty
            return []
        return dorm_models.Dormitory.objects.filter(bookMarkers__in=[team])

    def get(self, request, format=None):
        serializer = serializers.DormSerializer(self.get_dorms(request), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

# get all chat history in one team
# api with get method
# /api/chat-history/
class ChatHistoryView(views.APIView):

    def get_history(self, request):
        # get all messages in one team
        user = request.user
        team = user.profile.team
        if not team:
            # if user has no team, return empty
            return []
        return dorm_models.Message.objects.filter(team=team)

    def get(self, request, format=None):
        data = serializers.MessageSerializer(
            self.get_history(request), 
            context={'request': self.request},
            many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    

# send message
# api with post method
# /api/send-message/
class SendMessageView(views.APIView):
    serializer_class = serializers.SendMessageSerializer

    def post(self, request, format=None):
        serializer = serializers.SendMessageSerializer(data=self.request.data,
                                        context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

# select a dorm
# api with post method
# /api/select-dorm/
class SelectDormView(views.APIView):
    serializer_class = serializers.SelectDormSerializer

    def post(self, request, format=None):
        serializer = serializers.SelectDormSerializer(data=self.request.data,
                                        context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

# get all notifications of one user
# api with get method
# /api/notifications/
class NotificationView(views.APIView):

    def get_notifications(self, request):
        user = request.user
        return account_models.Notification.objects.filter(user=user)

    @method_decorator(cache_page(60 * 2), 'dispatch')
    def get(self, request, format=None):
        data = serializers.NotificationSerializer(self.get_notifications(request), many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    

# return avatar of one user
# api with get method
# /api/avatar/
class AvatarView(views.APIView):

    def get(self, request, format=None):
        data = serializers.AvatarSerializer(self.request.user).data
        return Response(data=data, status=status.HTTP_200_OK)
    

# get all interests tags from taggit
# api with get method
# /api/interests/
class InterestView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    @method_decorator(cache_page(60 * 2), 'dispatch')
    def get(self, request, format=None):
        data = serializers.TagSerializer(Tag.objects.all(), many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    

# get all users‘ profiles
# api with get method
# /api/profiles/
class ProfilesView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    @method_decorator(cache_page(60 * 2), 'dispatch')
    def get(self, request, format=None):
        users = []
        group = Group.objects.get(name='老师')
        for u in User.objects.all():
            # if user is not a teacher
            if not u.groups.filter(name=group).exists():
                users.append(u)
        data = serializers.UserProfileSerializer(users, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    

class GetIfLogin(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        if request.user.is_authenticated:
            return Response(data={'isLogin': True}, status=status.HTTP_200_OK)
        else:
            return Response(data={'isLogin': False}, status=status.HTTP_200_OK)
        

# get other users' comments from user pk
# api with get method
# /api/user-comments/
class UserCommentsView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserCommentsSerializer

    @method_decorator(cache_page(60 * 2), 'dispatch')
    def post(self, request, format=None):
        user_pk = request.data.get('pk', None)
        if user_pk is None:
            return Response(data={'error': 'user_pk is None'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(pk=user_pk)
        data = serializers.CommentSerializer(user.comments.all(), many=True).data
        return Response(data=data, status=status.HTTP_200_OK)