from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()

            new_category_name = request.POST.get('new_category', '').strip()
            if new_category_name:
                category, _ = Category.objects.get_or_create(name=new_category_name)
                post.categories.add(category)

            messages.success(request, "Пост успешно создан.")
            return redirect('post_list')
    else:
        form = PostForm()

    all_categories = Category.objects.all()
    return render(request, 'blog/post_form.html', {
        'form': form,
        'all_categories': all_categories,
        'post': None
    })

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()

            new_category_name = request.POST.get('new_category', '').strip()
            if new_category_name:
                category, _ = Category.objects.get_or_create(name=new_category_name)
                post.categories.add(category)

            selected_categories = request.POST.getlist('categories')
            post.categories.set(selected_categories)

            messages.success(request, "Пост успешно обновлён.")
            return redirect('post_update', pk=post.pk)  
    else:
        form = PostForm(instance=post, include_categories=False)

    all_categories = Category.objects.all()
    return render(request, 'blog/post_form.html', {
        'form': form,
        'all_categories': all_categories,
        'post': post
    })

@login_required
def remove_category_from_post(request, post_pk, category_id):
    post = get_object_or_404(Post, pk=post_pk)
    category = get_object_or_404(Category, id=category_id)
    post.categories.remove(category)
    messages.info(request, f'Категория "{category.name}" удалена из поста.')
    return redirect('post_update', pk=post_pk)

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    name = category.name
    category.delete()
    messages.info(request, f'Категория "{name}" полностью удалена из базы.')
    return redirect(request.META.get('HTTP_REFERER', 'post_list'))

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        new_name = request.POST.get('name', '').strip()
        if new_name:
            old_name = category.name
            category.name = new_name
            category.save()
            messages.success(request, f'Категория "{old_name}" переименована в "{new_name}".')
        else:
            messages.error(request, "Название категории не может быть пустым.")
    return redirect(request.META.get('HTTP_REFERER', 'post_list'))

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
