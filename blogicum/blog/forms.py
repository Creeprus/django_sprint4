from django import forms

from blog.models import Comment, Post


class PostForm(forms.ModelForm):
    """Класс формы для постов."""

    class Meta:
        """Класс метаданных."""

        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={'type': 'datetime-local'}
            )
        }


class CommentForm(forms.ModelForm):
    """Класс комментариев для постов."""

    class Meta:
        """Класс метаданных."""

        model = Comment
        fields = ('text',)
