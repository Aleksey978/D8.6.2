# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import  reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView


from .filters import PostFilter
from .forms import PostForm, SubscribeForm
from .models import Post, Author, Category


class PostList(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object.category.all()
        print(context)
        return context

@login_required(login_url='/posts/')  # Убедитесь, что URL указан правильно
@permission_required('news_portal.add_post', login_url='/posts/')
def post_create(request):
    form = PostForm
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Author.objects.get(user=request.user)
            if request.path == '/posts/news/create/':
                post.choose = 'NE'
            elif request.path == '/posts/articles/create/':
                post.choose = 'AR'
            form.save()
            categories = post.category.all()
            print(categories)

            # send_post_notification(post)
            return HttpResponseRedirect('/posts/')
    return render(request, 'post_edit.html', {'form': form})


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'news_portal.update_post'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news_portal.delete_post'

@login_required
def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        print(request.POST)
        if form.is_valid():
            category = get_object_or_404(Category, id=form.cleaned_data['category_id'])
            category.subscribers.add(request.user)
            return redirect('/')
    return redirect('/')

def send_post_notification(post):
    category = post.category
    subscribers = category.subscribers.all()
    subject = post.title
    message = render_to_string('post_notification_email.html', {
        'post': post,
        'username': '{{ user.username }}'
    })
    from_email = 'aleksei.tchetvyorkin@yandex.ru'
    for subscriber in subscribers:
        send_mail(subject, '', from_email, [subscriber.email], html_message=message)