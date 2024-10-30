from django.shortcuts import render 

def documentation_view(request):
    return render(request, 'user_documentation/documentation.html')

