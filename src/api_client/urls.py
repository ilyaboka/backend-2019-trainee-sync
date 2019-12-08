from django.urls import path

from api_client import views

urlpatterns: list = [
    path('account', views.AccountView.as_view(), name='account'),
    path('email', views.EmailView.as_view(), name='email'),
    path(
        'emailNotificationsEnabled', views.EmailNotificationsEnabledView.as_view(), name='email_notifications_enabled'
    ),
    path('following', views.FollowingView.as_view(), name='following'),
    path('message', views.MessageView.as_view(), name='message'),
    path('recognize', views.RecognizeView.as_view(), name='recognize'),
    path('signIn', views.SignInView.as_view(), name='sign_in'),
    path('signUp', views.SignUpView.as_view(), name='sign_up'),
    path('ticket', views.TicketMobileView.as_view(), name='ticket'),
    path('userList', views.UserListView.as_view(), name='user_list'),
]
