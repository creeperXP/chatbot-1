from openai import OpenAI

# form is helper function to define params
# retrieve data from html files
from fastapi import FastAPI, Form, Request

# from python typing module
# attach additional metadata
from typing import Annotated

# import templates
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class = HTMLResponse) # HTML response class
async def chatpage(request: Request):
    return templates.TemplateResponse("home.html", {"request":request})

# instead of export openai api key, do this
openai = OpenAI(
    api_key = 'key'
)

chatlog = [{'role': 'system', 'content': 'You are a Minecraft player that likes 2 player parkour and bedwars'}]

chatresponses = []



# post request (input)
@app.post("/")
async def chat(request: Request, userinput: Annotated[str, Form()]): # expect input in a form version? and type string

    chatlog.append({'role': 'user', 'content': userinput})

    # add to responses (user)
    chatresponses.append(userinput)

    # response = openai.ChatCompletions.create() is incorrect
    response = openai.chat.completions.create(
        model = 'gpt-3.5-turbo',

        # messages = conversation history: array of dictionaries
        messages = chatlog,
        temperature = 0.5
    )

    # content of the response
    botresponse = response.choices[0].message.content
    chatlog.append({'role': 'assistant', 'content': botresponse})

    # append to chat responses for bot
    chatresponses.append(botresponse)

    return templates.TemplateResponse("home.html", {"request": request, "chat responses": chatresponses})
