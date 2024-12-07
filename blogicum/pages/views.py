from django.shortcuts import render
from django.views.generic.base import TemplateView


class AboutPageView(TemplateView):
    """Класс для адрессации на страницу about."""

    template_name = 'pages/about.html'


class RulesPageView(TemplateView):
    """Класс для адрессации на страницу rules."""

    template_name = 'pages/rules.html'


def permission_denied(request, exception):
    """Обработка 403."""
    return render(request, "pages/403.html", status=403)


def csrf_failure(request, reason=""):
    """Обработка 403 (csrf)."""
    return render(request, "pages/403csrf.html", status=403)


def page_not_found(request, exception):
    """Обработка 404."""
    return render(request, "pages/404.html", status=404)


def server_error(request):
    """Обработка 500."""
    return render(request, "pages/500.html", status=500)
