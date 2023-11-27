from openai import OpenAI
from abc import ABCMeta, abstractmethod
import json
import os.path
import requests

KEY_FILE = "key.json"


class Client(metaclass=ABCMeta):
    def __init__(self, api_key):
        if os.path.isfile(KEY_FILE):
            self.client = LLMServiceClient()
        else:
            self.client = OpenAIClient(api_key)

    def create_completion(self, system_prompt, user_prompt):
        return self.client.create_completion(system_prompt, user_prompt)


class OpenAIClient(Client):
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def create_completion(self, system_prompt, user_prompt):
        completion = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return completion.choices[0].message.content


class LLMServiceClient(Client):
    def __init__(self):
        with open(KEY_FILE, "r") as key_file:
            svc_key = json.load(key_file)

        # Get Token
        self.svc_url = svc_key["url"]
        client_id = svc_key["uaa"]["clientid"]
        client_secret = svc_key["uaa"]["clientsecret"]
        uaa_url = svc_key["uaa"]["url"]

        params = {"grant_type": "client_credentials"}
        resp = requests.post(
            f"{uaa_url}/oauth/token", auth=(client_id, client_secret), params=params
        )

        self.token = resp.json()["access_token"]

    def create_completion(self, system_prompt, user_prompt):
        data = {
            "deployment_id": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": 800,
            "temperature": 0.7,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "top_p": 0.95,
            "stop": "null",
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"{self.svc_url}/api/v1/completions", headers=headers, json=data
        )
        completion = response.json()
        return completion["choices"][0]["message"]["content"]
