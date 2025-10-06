from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your models here.
class Post(models.Model):
    titulo=models.CharField(max_length=200)
    contenido=models.TextField()
    fecha_creacion=models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    #from taggit
    tags = TaggableManager(blank=True) 
    def __str__(self):
        return self.titulo 

class Comentario(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Nuevo: relación recursiva para permitir respuestas
    padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='respuestas')

    # Nuevo: para poder bloquear comentarios
    bloqueado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.autor.username} comentó en "{self.post.titulo}"'


class ImagenPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='posts/')
    descripcion = models.CharField(max_length=255, blank=True)  # opcional

    def __str__(self):
        return f"Imagen de {self.post.titulo}"


