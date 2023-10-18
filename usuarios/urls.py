from django.urls import path
from django.contrib.auth import views as auth_views
from usuarios.views import CustomLoginView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='usuarios/login.html'
    ), name='logout'),
]