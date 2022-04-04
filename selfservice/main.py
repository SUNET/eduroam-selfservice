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


def response_return(context):
    if "errors" in context and context["errors"] != []:
        return templates.TemplateResponse("fail.html", context=context)
    if "applied" in context and context["applied"]:
        return templates.TemplateResponse("success.html", context=context)
    return templates.TemplateResponse("index.html", context=context)


@app.get("/")
def index_get(request: Request):
    if "REMOTE_USER" in request.headers:
        eppn = request.headers.get("REMOTE_USER")
    elif "REMOTE_USER" in os.environ:
        eppn = os.environ["REMOTE_USER"]
    else:
        eppn = None

    context = {
        "request": request,
        "username": eppn,
    }

    if eppn is None:
        context["errors"] = ["Failed to read username (EPPN)"]

    return response_return(context)


@app.post("/")
async def index_post(request: Request):
    form = EduroamUserForm(request)
    await form.load_data()
    errors = form.is_valid()
    context = {
        "request": request,
        "username": form.username,
    }

    if errors != []:
        context["errors"] = form.errors
    else:
        context["applied"] = True
        errors = nac.handle_user(form.username, form.password)
        if errors != []:
            context["errors"] = errors

    return response_return(context)
