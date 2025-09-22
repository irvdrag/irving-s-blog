from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
# Create your views here.
def lista_posts(request):
    posts=Post.objects.all().order_by('-fecha_creacion')
    return render(request,'blog/lista.html',{'posts':posts})

def detalle_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    return render(request,'blog/detalle.html',{'post':post})

@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            nuevo_post = form.save(commit=False)
            nuevo_post.autor = request.user  # ✅ Asigna el autor
            nuevo_post.save()
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