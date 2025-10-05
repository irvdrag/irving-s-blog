from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
#de libreria taggit
from taggit.models import Tag
from .models import Post,Comentario
from .forms import PostForm,ComentarioForm
from django.contrib.auth import login
# Create your views here.
def lista_posts(request):
    query = request.GET.get('q')  # capturamos la búsqueda
    if query:
        posts = Post.objects.filter(
            Q(titulo__icontains=query) |
            Q(contenido__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-fecha_creacion')
    else:
        posts = Post.objects.all().order_by('-fecha_creacion')

    return render(request, 'blog/lista.html', {
        'posts': posts,
        'query': query  # para mostrar lo que se buscó en el HTML
    })



def detalle_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = post.comentarios.filter(padre__isnull=True).order_by('-fecha_creacion')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.autor = request.user
                comentario.post = post

                # 🔽 ESTA PARTE ES FUNDAMENTAL
                padre_id = request.POST.get('padre_id')
                if padre_id:
                    try:
                        padre = Comentario.objects.get(id=padre_id)
                        comentario.padre = padre
                    except Comentario.DoesNotExist:
                        pass

                comentario.save()
                return redirect('detalle_post', post_id=post.id)
        else:
            return redirect('login')
    else:
        form = ComentarioForm()

    return render(request, 'blog/detalle.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form
    })

@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            nuevo_post = form.save(commit=False)
            nuevo_post.autor = request.user  # ✅ Asigna el autor
            nuevo_post.save()
            form.save_m2m() 
            return redirect('lista_posts')
    else:
        form = PostForm()
    
    return render(request, 'blog/crear_post.html', {'form': form})

@login_required
def editar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('lista_posts')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/editar_post.html', {'form': form, 'post': post})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # inicia sesión automáticamente después del registro
            return redirect('lista_posts')  # cambia 'home' por la vista a la que quieras redirigir
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

#para taggit
def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag])
    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts})

@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    # 🔒 Solo el autor o staff puede editar
    if request.user != comentario.autor and not request.user.is_staff:
        messages.error(request, "No tenés permiso para editar este comentario.")
        return redirect('detalle_post', post_id=comentario.post.id)

    # 🔒 No permitir editar si el comentario está bloqueado
    if comentario.bloqueado:
        messages.warning(request, "Este comentario está bloqueado y no puede ser editado.")
        return redirect('detalle_post', post_id=comentario.post.id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, "Comentario actualizado correctamente.")
            return redirect('detalle_post', post_id=comentario.post.id)
    else:
        form = ComentarioForm(instance=comentario)

    return render(request, 'blog/editar_comentario.html', {
        'form': form,
        'comentario': comentario
    })

@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    if request.user != comentario.autor and not request.user.is_staff:
        return HttpResponseForbidden("No tenés permiso para eliminar este comentario.")

    if request.method == 'POST':
        post_id = comentario.post.id
        comentario.delete()
        return redirect('detalle_post', post_id=post_id)

    return render(request, 'blog/confirmar_eliminacion.html', {'comentario': comentario})


