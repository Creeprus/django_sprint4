from django.shortcuts import render


def page_not_found(request, exception):
    """Обработка 404."""
    return render(request, 'pages/404.html', status=404)


def internal_server_error(request):
    """Обработка 500."""
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    """Обработка 403."""
    return render(request, 'pages/403csrf.html', status=403)
