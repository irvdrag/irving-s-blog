from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_posts, name='lista_posts'),
    path('post/<int:post_id>/', views.detalle_post, name='detalle_post'),
    path('crear/', views.crear_post, name='crear_post'), 
    path('post/<int:post_id>/editar/', views.editar_post, name='editar_post'),
]