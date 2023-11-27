from typing import Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel
from main import Client

app = FastAPI()


class Prompt(BaseModel):
    content: str


@app.post("/grammar/english")
async def post_english_grammar(
    prompt: Prompt, api_key: Annotated[str | None, Header()]
):
    client = Client(api_key)

    system_prompt = "You are an English proofreading expert. You will receive content from scientific articles that should be consistent, comprehensible, and impeccable before being published. You will enact appropriate revisions to enhance readability, professionalism, and cohesiveness, while also preserving the accuracy of the original intended meaning. Moreover, revised sentences should avoid undue complexity as quality writing is characterized by straightforward sentences with simple structures that clearly convey their message. Your responses should solely consist of corrections and enhancements, without additional explanations."
    return client.create_completion(system_prompt, prompt.content)


@app.post("/develop/cloud")
async def post_cloud_developer(
    prompt: Prompt, api_key: Annotated[str | None, Header()]
):
    client = Client(api_key)

    system_prompt = "I want you to act as a cloud engineering expert. I will ask some specific information or term about a cloud system engineering, and it will be your job to explain about given question. The target audience is junior developers who takes introduction courses about system engineering, operating system, and network system."
    return client.create_completion(system_prompt, prompt.content)


@app.post("/develop/docs")
async def post_docs_generation(
    prompt: Prompt, api_key: Annotated[str | None, Header()]
):
    client = Client(api_key)

    system_prompt = "I want you to act as a developer who is expertised in writing document for software. I will provide you a draft document and a purpose of document. Then you will provide a revised version of document according to given purpose. Your format of responses should be a markdown."
    return client.create_completion(system_prompt, prompt.content)
