EN_PROMPT_TEMPLATE = """
As a programming assistant, your task is to generate code snippets based on the user question and instructions given below:

## Please consider the following points while generating the code snippet:

- Make sure you follow the user instructions word to word. If the instruction says to use a specific language or a specific method, use exactly that.

- Your output should be a valid code snippet in the programming language indicated in the question or the instructions.

- Pay close attention to the syntax and formatting rules of the programming language that you are using. The code should be well-formatted and easy to read. 

- Make sure that the code snippet you are generating is efficient and is not overly complicated.

## Output Format:
The output should be a valid, well-formatted, and efficient code snippet that adheres to the above question and instructions.

## Task information

User Question:
{question}

Instructions:
{instructions_str}

Please generate the code snippet based on the above information:
"""

ZH_PROMPT_TEMPLATE = """
作为编程助理，你的任务是根据下面给出的用户问题和指示生成代码片段：
## 请在生成代码片段时考虑以下几点：

- 你必须严格按照用户的指示执行。如果指示中要求使用特定的语言或方法，那么你就要确切的使用它。

- 你的输出应该是问答或指示中所指定的编程语言的有效代码片段。

- 要密切注意你正在使用的编程语言的语法和格式规则。代码应该排版正整，易于阅读。

- 你生成的代码片段应该是有效和不过于复杂的。

## 输出格式：
输出应该是一个有效的、排版整洁的、效率高的代码片段，且符合上述的问题和指示。
请注意!!!你的输出应该只有代码片段,没有其他任何的内容。
## 任务信息

用户提问：
{question}

指示：
{instructions_str}

请根据上述信息生成代码片段：
"""