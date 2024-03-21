from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutAPI.as_view()),
    path('change-password/<int:pk>/', views.ChangePasswordView.as_view()),
    path('dorm-room/', views.DormViewSet.as_view({'get': 'list'})),
    path('comment/', views.CommentViewSet.as_view({'get': 'list'})),
    path('user-information/', views.UserInformationViewSet.as_view({'get': 'list'})),
    path('create-comment/', views.CommentCreateView.as_view()),
    path('change-avatar/', views.ChangeAvatarView.as_view()),
    path('change-profile/', views.ChangeProfileView.as_view()),
    path('teams/', views.TeamViewSet.as_view({'get': 'list'})),
    path('create-team/', views.TeamCreateView.as_view()),
    path('leave-team/', views.LeaveTeamView.as_view()),
    path('join-team/', views.JoinTeamView.as_view()),
    path('update-team/', views.UpdateTeamView.as_view()),
    path('builds/', views.BuildViewSet.as_view({'get': 'list'})),
    path('book-dorm/', views.BookMarkDormView.as_view()),
    path('unbook-dorm/', views.UnBookMarkDormView.as_view()),
    path('bookmark-dorms/', views.AllBookMarkDormView.as_view()),
    path('messages/', views.ChatHistoryView.as_view()),
    path('send-message/', views.SendMessageView.as_view()),
    path('select-dorm/', views.SelectDormView.as_view()),
    path('notifications/', views.NotificationView.as_view()),
    path('get-avatar/', views.AvatarView.as_view()),
    path('all-interests/', views.InterestView.as_view()),
    path('all-profiles/', views.ProfilesView.as_view()),
    path('get-if-login/', views.GetIfLogin.as_view()),
    path('user-comments/', views.UserCommentsView.as_view()),
]