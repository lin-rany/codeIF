import pytest
import os
from utils.api_util import chat_completion_deepseek

# 测试正常情况
def test_chat_completion_deepseek_success():
    model = "deepseek-chat"
    message = "你好,你是谁?"
    temperature = 0.5
    max_tokens = 100
    api_dict = {"api_key": "sk-2940b2244b6942bb906c9b7c4dedd057"}

    result = chat_completion_deepseek(model, message, temperature, max_tokens, api_dict)
    print(f"message:{message},result: {result}")
    assert result!= "API_ERROR_OUTPUT"

