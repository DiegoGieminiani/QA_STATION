from django.shortcuts import render

def documentation(request):
    return render(request, 'user_documentation/documentation.html')
