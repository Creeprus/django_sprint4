from django.contrib import admin

from blog.models import Category, Comment, Location, Post


class PostInline(admin.StackedInline):
    """Сущность Post в админке (многие ко многим)."""

    model = Post
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Сущность Post в админке."""

    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'category',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Сущность Category в админке."""

    inlines = (
        PostInline,
    )
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Сущность Location в админке."""

    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Сущность Comment в админке."""

    list_display = (
        'text',
        'author',
        'post'
    )
