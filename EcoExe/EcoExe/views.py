# Authored by Jack Hales,  James Sadler

from django.shortcuts import render

# Create view for index page
def index(request):
    return render(request, "index.html")

# Create view for privacy policy page
def privacy(request):
    return render(request, "privacy.html")

# Create view for terms and conditions page
def terms(request):
    return render(request, "terms.html")

# Create view for custom 404 error page
def custom_404(request, exception):
    return render(request, 'error/404.html', status=404)

# Create view for custom 500 error page
def custom_500(request):
    return render(request, 'error/500.html', status=500)