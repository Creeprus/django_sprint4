from typing import Any, Dict

from django.db.models.query import QuerySet, Q
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DetailView,
    DeleteView,
    ListView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import Category, Comment, Post, User

from blog.forms import CommentForm, PostForm


class PostMixin:
    """Класс mixin для поста."""

    model = Post
    paginate_by = 10


class CommentMixin:
    """Класс mixin для комментариев."""

    model = Comment
    form_class = CommentForm

    def get_object(self, queryset=None):
        """Получить объект CommentMixin."""
        return get_object_or_404(
            Comment, pk=self.kwargs["comment_pk"],
            post_id=self.kwargs["post_pk"]
        )

    def get_success_url(self):
        """Обработка переадресации.

        Если всё прошло успешно,
        перенести пользователя на страницу с постом.
        """
        return reverse("blog:post_detail",
                       kwargs={"pk": self.kwargs["post_pk"]})


class DispatchMixin:
    """Класс mixin для редирекции пользователя, после создания комментария."""

    def dispatch(self, request, *args, **kwargs):
        """Само действие редирекции."""
        if self.get_object().author != request.user:
            return redirect(
                reverse('blog:post_detail',
                        kwargs={'pk': self.get_object().pk}
                        )
            )
        return super().dispatch(request, *args, **kwargs)


class PostListView(PostMixin, ListView):
    """Класс представление списка постов (прошлый index)."""

    def get_queryset(self):
        """Возвращает список постов.

        А именно посты, которые:
        опубликованы, старее текущей даты,
        категория опубликована.
        """
        posts = Post.objects.prefetch_related(
            "author", "category", "location"
        ).filter(
            pub_date__lt=timezone.now(),
            is_published=True,
            category__is_published=True,
        ).annotate(
            comment_count=Count("comments")
        ).order_by("-pub_date")
        return posts


class PostCreateView(LoginRequiredMixin, CreateView):
    """Класс отвечающий за добавление постов (форма)."""

    model = Post
    form_class = PostForm

    def form_valid(self, form):
        """Проверяет валидность формы."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """Обработка переадресации.

        Если все прошло успешно,
        то пользователя обратно отправляет на его профиль.
        """
        return reverse("blog:profile", kwargs={
            "username": self.request.user.username})


class PostDetailView(DetailView):
    """Класс отвечающий за отображение полного поста (бывший post_detail)."""

    model = Post

    def get_object(self):
        """Получить объект PostDetailView."""
        return get_object_or_404(
            Post.objects.filter(
                Q(is_published=True) | Q(author__username=self.request.user)
            ),
            pk=self.kwargs['pk'],
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Получить список комментарией, связанные с постом."""
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.select_related("author")
        return context


class PostUpdateView(LoginRequiredMixin, DispatchMixin, UpdateView):
    """Класс отвечающий за обновление поста (форма)."""

    model = Post
    form_class = PostForm

    def form_valid(self, form):
        """Проверяет валидность формы."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DispatchMixin, DeleteView):
    """Класс отвечающий за удаление поста (форма)."""

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog:post_list")


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Класс отвечающий за добавление комментария (форма)."""

    post_object = None
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        """Проверяет валидность формы."""
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        """Обработка переадресации.

        Если все прошло успешно,
        то пользователя обратно отправляет на главную страницу.
        """      
        return reverse("blog:post_detail", kwargs={"pk": self.kwargs["pk"]})


class CommentUpdateView(CommentMixin,
                        DispatchMixin,
                        LoginRequiredMixin,
                        UpdateView):
    """Связка между классами.

    Необходимо, чтобы обновление на форме с переадресацией работали.
    """

    pass


class CommentDeleteView(CommentMixin,
                        DispatchMixin,
                        LoginRequiredMixin,
                        DeleteView):
    """Связка между классами.

    Необходимо, чтобы удаление на форме с переадресацией работали.
    """

    template_name = "blog/comment_form.html"


class CategoryListView(PostMixin, ListView):
    """Класс отвечающий за отображение списка категорий."""

    template_name = "blog/category.html"
    context_object_name = "page_obj"

    def get_queryset(self) -> QuerySet[Any]:
        """Возвращает список категорий.

        А именно категории, которые:
        опубликованы, старее текущей даты,
        категория опубликована.
        """
        self.category = get_object_or_404(Category,
                                          slug=self.kwargs["category_slug"],
                                          is_published=True)
        return (
            Post.objects.select_related("category")
            .filter(category=self.category,
                    pub_date__lt=timezone.now(),
                    category__is_published=True,
                    is_published=True,
                    )
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
            .all()
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Получить все прочие объекты, связанные с категорией."""
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class ProfileView(PostMixin, ListView):
    """Класс, отвечающий за отображение профиля."""

    template_name = "blog/profile.html"
    ordering = "-pub_date"

    def get_queryset(self):
        """Возвращает данные профиля."""
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return (
            Post.objects.select_related("author", "category", "location")
            .filter(
                author=self.author,
            )
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
        )

    def get_context_data(self, **kwargs):
        """Получить все прочие объекты, связанные с профилем."""
        context = super().get_context_data(**kwargs)
        context["profile"] = self.author
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Класс, отвечающий за обновление профиля (форма)."""

    model = User
    template_name = "blog/profile_update.html"
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]

    def get_success_url(self) -> str:
        """Выполняет переадресацию."""
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.object.username})

    def get_object(self, queryset=None):
        """Получает объект класса."""
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def form_valid(self, form):
        """Проверяет валидность формы."""
        user = form.save(commit=False)
        user.username = form.cleaned_data.get('username')
        self.request.user = user
        user.save()
        return redirect(self.get_success_url())
