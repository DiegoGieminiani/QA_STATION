from django.shortcuts import render

# Vista para la página "Nosotros"
def about_view(request):
    return render(request, 'about_us/about_us.html')

