import openai as ai
import streamlit as st
import io
from collections import namedtuple

AI_SECRET_KEY = st.secrets["AI_SECRET_KEY"]
AI_ORG_ID = st.secrets["AI_ORG_ID"]
AUDIO_MODEL = "whisper-1"
CHAT_MODEL = "gpt-3.5-turbo"

ai.organization = AI_ORG_ID
ai.api_key = AI_SECRET_KEY

ChatResponse = namedtuple("ChatResponse", ("message_dict", "tokens"))


def chatgpt_response(messages) -> ChatResponse:
    response = ai.ChatCompletion.create(
        model=CHAT_MODEL,
        messages=messages,
    )
    return ChatResponse(
        response["choices"][0]["message"],
        (
            response["usage"]["prompt_tokens"],
            response["usage"]["completion_tokens"],
            response["usage"]["total_tokens"],
        ),
    )


def transcribe_audio(a_file: io.FileIO, prompt=None, translate=False) -> dict:
    if not prompt:
        prompt = ""
    return ai.Audio.transcribe(AUDIO_MODEL, a_file, prompt=prompt)
