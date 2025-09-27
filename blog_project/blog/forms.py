from django import forms
from .models import Post,Comentario

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'tags']
        widgets = {
            'tags': forms.TextInput(attrs={
                'placeholder': 'Escribe etiquetas separadas por comas, ej: python, django, tutorial'
            }),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        qs = Post.objects.filter(titulo=titulo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe una publicación con ese título.")
        return titulo

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu comentario'}),
        }
        labels = {
            'contenido': '',
        }