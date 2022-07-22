import PIL.Image
import cv2.utils
import io

import cv2
from django.shortcuts import render
from django.http import HttpResponseRedirect
import base64
from keras.models import load_model
import numpy as np
from PIL import Image

# Create your views here.

model = load_model('static/models/test_model.h5')

def index(request):
    return render(request, 'website/base.html')


def compute(request):
    if request.method == 'POST':
        img = request.POST.get('canvasData')
        img_as_bytes = base64.b64decode(img[22::])
        img_as_img = Image.open(io.BytesIO(img_as_bytes)).convert(mode='P').resize((28, 28))
        img_as_nparray = np.array(img_as_img).reshape(-1, 28, 28, 1)
        result = np.argmax(model.predict([img_as_nparray]))
        return render(request, 'website/result.html', context={'result': result})
    else:
        return HttpResponseRedirect('/')


