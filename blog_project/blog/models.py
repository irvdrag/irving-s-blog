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
    tags = TaggableManager()
    def __str__(self):
        return self.titulo 

class Comentario(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.autor.username} comentó en "{self.post.titulo}"' 

