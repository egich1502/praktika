import io
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
        img_as_img = Image.open(io.BytesIO(img_as_bytes)).convert(mode='P')
        img_as_nparray = np.array(img_as_img)

        r = img_as_nparray.strides[0]
        c = img_as_nparray.strides[1]

        a = np.lib.stride_tricks.as_strided(img_as_nparray, shape=(28, 28, 10, 10), strides=(r * 10, c * 10, r, c))
        b = np.arange(28 * 28).reshape(28, 28)

        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                b[i][j] = a[i][j].max()

        b[b > 0] = 255
        c = b.reshape(-1, 28, 28, 1)

        result = np.argmax(model.predict([c]))
        return render(request, 'website/result.html', context={'result': result})
    else:
        return HttpResponseRedirect('/')
