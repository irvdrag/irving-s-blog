from django import forms
from .models import Post,Comentario,ImagenPost
from django.forms import modelformset_factory
from django import forms

class ImagenPostForm(forms.ModelForm):
    class Meta:
        model = ImagenPost
        fields = ['imagen', 'descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'placeholder': 'Descripción opcional'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'tags']
        widgets = {
            'tags': forms.TextInput(attrs={
                'placeholder': 'Escribe etiquetas separadas por comas, ej: python, django, tutorial'
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].required = False  # 🔽 Esto garantiza que no sea obligatorio

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

ImagenPostFormSet = modelformset_factory(ImagenPost, fields=('imagen', 'descripcion'), extra=3, can_delete=True)