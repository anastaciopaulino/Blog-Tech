from django.conf.urls import url
from accounts import views
from django.contrib.auth import views as auth_views

# Nome da aplicação
app_name = 'accounts'

urlpatterns = [
    url(r'login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'(?P<token>[-\w]+)/(?P<username>[-\w]+)/others-info/$', views.UserOthersInfo.as_view(), name='others-info'),
    url(r'(?P<username>[-\w]+)/(?P<pk>\d+)/in/detail/$', views.UserDetail.as_view(), name='detail-user'),
    url(r'(?P<username>[-\w]+)/(?P<pk>\d+)/detail/in/user-update/$', views.UserUpdateProfile.as_view(), name='image-update'),
    url(r'(?P<username>[-\w]+)/(?P<pk>\d+)/detail/in/update-image/$', views.UserUpdate.as_view(), name='user-update'),
    url(r'accounts/check-info/$', views.RedirectInfo.as_view(), name='check-info'),
]