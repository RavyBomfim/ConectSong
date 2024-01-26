from django.urls import path
from .views import IndexView, excluir_post

urlpatterns = [
    path('inicio', IndexView.as_view(), name='inicio'), 
    path('excluir/post', excluir_post, name='excluir-post'),
]