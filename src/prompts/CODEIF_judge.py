ZH_JUDGE_PROMPT='''
作为编程助理，你的任务是根据下面给出的用户问题和指示，判断模型生成的代码是否严格遵循了这些指示。你需要返回一个与指示长度相同的列表，列表中只包含'Yes'和'No'，表示模型是否遵循了对应的指示。

## 请在判断时考虑以下几点：

- 你必须严格按照用户的指示进行判断。如果指示中要求使用特定的语言或方法，那么你就要确切地检查代码是否使用了它。

- 你的输出应该是一个与指示长度相同的列表，列表中只包含'Yes'和'No'。

- 要密切注意你正在使用的编程语言的语法和格式规则。代码应该排版整洁，易于阅读。

- 你生成的列表应该是有效和不过于复杂的。

## 任务信息

用户提问：
{question}

指示：
{instructions_str}

模型生成的回答：
{generated_code}

请根据上述信息判断模型是否遵循了指示，并返回一个与指示长度相同的列表，列表中只包含'Yes'和'No'
请注意!!! 你的输出应该只有列表,没有其他任何的内容。列表中的内容只包含'Yes'和'No',不要包含其他的单词
'''

EN_JUDGE_PROMPT='''
As a programming assistant, your task is to evaluate if the model-generated code adheres to the user instructions and question stated below. You need to return a list whose length is that of the instructions, containing only the terms 'Yes' or 'No', indicating if the model has followed each instruction respectively.

## Please consider the following points while evaluating:

- You must judge strictly based on the user's instruction. If a specific language or method is asked for in the instructions, you must specifically check if it has been used in the code.

- Your output should be a list the same length as the instructions, containing only 'Yes' or 'No'.

- Be mindful of the syntax and formatting rules of the programming language you are using. The codes should be neatly formatted and easy to read.

- The list you generate should be valid and not overly complex.

## Task information

User question:
{question}

Instructions:
{instructions_str}

Model-generated code:
{generated_code}

Please, based on the above information, judge if the model has followed the instructions, and return a list of the same length as the instructions, containing only 'Yes' or 'No'. such ['No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No']
Please note!!! Your output should only be a list, without any other content. The list should only contain 'Yes' and 'No', do not include any other words.
Please note!!! Your output should be a list the same length as the instructions, containing only 'Yes' or 'No'.
'''