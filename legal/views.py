from django.shortcuts import render

# Create your views here.
def termsofservice(request):
    return render(request, 'legal/tos.html')

def privacypolicy(request):
    return render(request, 'legal/privacy.html')