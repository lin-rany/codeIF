import os
import time
import openai
import anthropic
import google.generativeai as genai
import cohere
from together import Together

# API setting constants
API_MAX_RETRY = 3
API_RETRY_SLEEP = 3
API_ERROR_OUTPUT = "$ERROR$"


def chat_completion_openai(model, message, temperature=0.0, max_tokens=4096, api_dict=None):
    if api_dict is not None and "api_key" in api_dict:
        api_key = api_dict["api_key"]
    else:
        api_key = os.environ["API_KEY"]
        
    if api_dict is not None and "api_base" in api_dict:
        api_base = api_dict["api_base"]
    else:
        api_base = os.environ["API_BASE"]
    output = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url=api_base)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}],
                temperature=temperature,
                max_tokens=max_tokens,
                n=1,
                stream=False,
                timeout=120,
            )
            output = response.choices[0].message.content
            break
        except Exception as e:
            print(type(e), e)
            print('sleeping for 3 sec')
            time.sleep(API_RETRY_SLEEP)

    return output


def chat_completion_anthropic(model, message, temperature=0.0, max_tokens=4096, api_dict=None):
    """
    Call Anthropic Claude models using the Anthropic API.
    """
    if api_dict is not None and "api_key" in api_dict:
        api_key = api_dict["api_key"]
    else:
        api_key = os.environ["ANTHROPIC_API_KEY"]

    output = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        try:
            c = anthropic.Anthropic(api_key=api_key)
            response = c.completions.create(
                model=model,
                max_tokens_to_sample=max_tokens,
                temperature=temperature,
                prompt=f"{anthropic.HUMAN_PROMPT} {message}{anthropic.AI_PROMPT}",
            )
            output = response.completion
            break
        except anthropic.APIError as e:
            print(type(e), e)
            time.sleep(API_RETRY_SLEEP)
    return output.strip()


def chat_completion_google_generativeai(model, message, temperature=0.0, max_tokens=4096, api_dict=None):
    """
    Call Google PaLM models using the Google Generative AI API.
    """
    if api_dict is not None and "api_key" in api_dict:
        api_key = api_dict["api_key"]
    else:
        api_key = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    generation_config = {
        "temperature": temperature,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": max_tokens,
    }

    output = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        try:
            gemini = genai.GenerativeModel(
                model_name=model,
                generation_config=generation_config,
                safety_settings=safety_settings,
            )
            convo = gemini.start_chat(history=[])
            convo.send_message(message)
            output = convo.last.text
            break
        except genai.types.generation_types.StopCandidateException as e:
            print(type(e), e)
            break
        except Exception as e:
            print(type(e), e)
            time.sleep(API_RETRY_SLEEP)

    return output


def chat_completion_cohere(model, message, temperature=0.0, max_tokens=4096, api_dict=None):
    """
    Call Cohere models using the Cohere API.
    """
    if api_dict is not None and "api_key" in api_dict:
        api_key = api_dict["api_key"]
    else:
        api_key = os.environ["CO_API_KEY"]

    output = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        try:
            co = cohere.Client(api_key=api_key)
            response = co.chat(
                model=model,
                max_tokens=min(max_tokens, 4000),
                temperature=temperature,
                message=message,
            )
            output = response.text
            break
        except Exception as e:
            print(type(e), e)
            time.sleep(API_RETRY_SLEEP)
    return output.strip()


def chat_completion_together(model, message, temperature=0.0, max_tokens=4096, api_dict=None):
    """
    Call Together models using the Together API.
    """
    if api_dict is not None and "api_key" in api_dict:
        api_key = api_dict["api_key"]
    else:
        api_key = os.environ["TOGETHER_API_KEY"]
    client = Together(api_key=api_key)

    output = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}],
                stream=True,
            )
            output = ""
            for chunk in stream:
                output += chunk.choices[0].delta.content or ""
            break
        except Exception as e:
            print(type(e), e)
            time.sleep(API_RETRY_SLEEP)

    return output

def chat_completion_deepseek(model, message, temperature, max_tokens, api_dict=None):
    if api_dict is not None and "api_key" in api_dict:
        api_key = api_dict["api_key"]
    else:
        api_key = os.environ["DEEPSEEK_API_KEY"]
    output = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}],
                temperature=temperature,
                max_tokens=max_tokens,
                n=1,
                stream=False
            )
            output = response.choices[0].message.content
            break
        except Exception as e:
            print(type(e), e)
            print('sleeping for 3 sec')
            time.sleep(API_RETRY_SLEEP)

    return output
