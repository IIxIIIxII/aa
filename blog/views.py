from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import Post, Category
from .forms import PostForm

def post_list(request):
    category_id = request.GET.get('category')
    search_author = request.GET.get('author', '').strip()
    categories = Category.objects.all()

    posts = Post.objects.all()

    if category_id:
        posts = posts.filter(categories__id=category_id).distinct()

    if search_author:
        posts = posts.filter(author__username__icontains=search_author)

    context = {
        'posts': posts,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'search_author': search_author,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_list')
    else:
        form = PostForm()
        return render(request, 'blog/post_form.html', {'form': form})


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_form.html', {'form': form})
    
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')