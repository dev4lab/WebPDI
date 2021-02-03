from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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