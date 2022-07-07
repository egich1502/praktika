from django.shortcuts import render
from django.http import HttpResponseRedirect
import base64
from static.scripts.black_box import send_list


# Create your views here.

def index(request):
    return render(request, 'website/base.html')


def compute(request):
    if request.method == 'POST':
        img = request.POST.get('canvasData')
        img_as_bytes = base64.b64decode(img[22::])
        result = send_list(img_as_bytes)
        return render(request, 'website/result.html', context={'result': result})
    else:
        return HttpResponseRedirect('/')
