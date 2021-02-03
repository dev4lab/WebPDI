from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import cv2 as cv
import numpy as np

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@app.post("/uploadimage/")
async def create_upload_file(image: UploadFile = File(...)):
    image.filename = 'actual.png'
    file_location = f"static/images/{image.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(image.file.read())
    response = RedirectResponse(url='/edit/')
    return response

@app.post('/edit/')
async def edit_image(request: Request):
    return templates.TemplateResponse('item.html', {'request': request})

@app.get('/change/')
async def change_image(request: Request, contraste: int, brilho: int):

    image = cv.imread('static/images/actual.png', 0)
    
    im = np.double(image.copy())
    im = im * contraste + brilho #O valor de todos os pixels está sendo multiplicado por l

    #Garantindo que os valores de pixel não vão passar de 255 e nem estar abaixo de 0
    im[im > 255] = 255
    im[im < 0] = 0

    im = np.uint8(im)

    cv.imwrite('static/images/changed.png', im)
    return templates.TemplateResponse('item.html', {'request': request})