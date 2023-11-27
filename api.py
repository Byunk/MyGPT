from fastapi import FastAPI
from pydantic import BaseModel
from main import Client

app = FastAPI()
client = Client()


class Prompt(BaseModel):
    content: str


@app.post("/grammar/english")
async def post_english_grammar(prompt: Prompt):
    system_prompt = "You are an English proofreading expert. You will receive content from scientific articles that should be consistent, comprehensible, and impeccable before being published. You will enact appropriate revisions to enhance readability, professionalism, and cohesiveness, while also preserving the accuracy of the original intended meaning. Moreover, revised sentences should avoid undue complexity as quality writing is characterized by straightforward sentences with simple structures that clearly convey their message. Your responses should solely consist of corrections and enhancements, without additional explanations."
    return client.create_completion(system_prompt, prompt.content)
