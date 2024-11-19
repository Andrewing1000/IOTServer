from django.shortcuts import render

def index(request):
    return render(request, 'airdrum/index.html')

def drum_interface(request):
    url = f'{request.get_host()}'
    return render(request, 'airdrum/animacion.html', {'base_url': url})

