from django import forms
from .models import Post
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields= ['titulo', 'contenido'] 
    
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')

        qs = Post.objects.filter(titulo=titulo)

        # Si estás editando, ignora ese mismo post
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Ya existe una publicación con ese título.")

        return titulo
