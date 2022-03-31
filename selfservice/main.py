import os
import sys

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from selfservice.forms import EduroamUserForm
from selfservice.nac import NacConnection

try:
    NAC_TOKEN = os.environ["NAC_TOKEN"]
except KeyError:
    print("Enironment variable NAC_TOKEN must be set.")
    sys.exit(-2)

try:
    NAC_URL = os.environ["NAC_URL"]
except KeyError:
    print("Enironment variable NAC_URL must be set.")
    sys.exit(-2)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

nac = NacConnection(NAC_URL, NAC_TOKEN)


@app.get("/")
def index_get(request: Request):
    eppn = request.headers.get("REMOTE_USER")

    if eppn == None:
        context = {
            "request": request,
            "username": eppn,
            "errors": ["Failed to read username (EPPN)"]
        }
        return templates.TemplateResponse("fail.html", context=context)

    context = {
        "request": request,
        "username": eppn,
    }
    return templates.TemplateResponse("index.html", context=context)


@app.post("/")
async def index_post(request: Request):
    form = EduroamUserForm(request)
    await form.load_data()
    errors = form.is_valid()

    if errors != []:
        context = {
            "request": request,
            "username": form.username,
            "errors": form.errors
        }
        return templates.TemplateResponse("fail.html", context=context)
    else:
        errors = nac.handle_user(form.username, form.password)
        context = {
            "request": request,
            "username": form.username,
            "errors": errors
        }

        if errors != []:
            return templates.TemplateResponse("fail.html", context=context)
    return templates.TemplateResponse("success.html", context=context)
