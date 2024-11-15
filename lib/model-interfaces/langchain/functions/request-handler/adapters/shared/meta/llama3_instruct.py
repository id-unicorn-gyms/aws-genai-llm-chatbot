from langchain.schema import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import genai_config.config as config 

BEGIN_OF_TEXT = "<|begin_of_text|>"
SYSTEM_HEADER = "<|start_header_id|>system<|end_header_id|>"
USER_HEADER = "<|start_header_id|>user<|end_header_id|>"
ASSISTANT_HEADER = "<|start_header_id|>assistant<|end_header_id|>"
EOD = "<|eot_id|>"

#externalize config from DynamoDB
table_name = "test-table-ddb"
key_name = "model_id"
key_value = "llama3"

reader = config.DynamoDBReader(table_name, key_name)
prompt_default = reader.read_value(key_value)["prompt_default"]['S']
prompt_qna = reader.read_value(key_value)["prompt_qna"]['S']
prompt_condensed_qna = reader.read_value(key_value)["prompt_condensed_qna"]['S']

Llama3Prompt = f"""{BEGIN_OF_TEXT}{SYSTEM_HEADER}

You are an helpful assistant that provides concise answers to user questions with as little sentences as possible and at maximum 3 sentences. You do not repeat yourself. You avoid bulleted list or emojis.{EOD}{{chat_history}}{USER_HEADER}

Context: {{input}}{EOD}{ASSISTANT_HEADER}"""  # noqa:E501

Llama3Prompt_new = prompt_default

Llama3QAPrompt = f"""{BEGIN_OF_TEXT}{SYSTEM_HEADER}

Use the following conversation history and pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. You do not repeat yourself. You avoid bulleted list or emojis.{EOD}{{chat_history}}{USER_HEADER}

Context: {{context}}

{{question}}{EOD}{ASSISTANT_HEADER}"""  # noqa:E501

Llama3QAPrompt_new = prompt_qna

Llama3CondensedQAPrompt = f"""{BEGIN_OF_TEXT}{SYSTEM_HEADER}

Given the following conversation and the question at the end, rephrase the follow up input to be a standalone question, in the same language as the follow up input. You do not repeat yourself. You avoid bulleted list or emojis.{EOD}{{chat_history}}{USER_HEADER}

{{question}}{EOD}{ASSISTANT_HEADER}"""  # noqa:E501

Llama3CondensedQAPrompt_new = prompt_condensed_qna


Llama3PromptTemplate = PromptTemplate.from_template(Llama3Prompt)
Llama3PromptTemplate_new = PromptTemplate.from_template(Llama3Prompt_new)
Llama3QAPromptTemplate = PromptTemplate.from_template(Llama3QAPrompt)
Llama3QAPromptTemplate_new = PromptTemplate.from_template(Llama3QAPrompt_new)
Llama3CondensedQAPromptTemplate = PromptTemplate.from_template(Llama3CondensedQAPrompt)
Llama3CondensedQAPromptTemplate_new = PromptTemplate.from_template(Llama3CondensedQAPrompt_new)

print("========== new prompt template reload from dynamodb")
print(Llama3PromptTemplate_new)
print(Llama3QAPromptTemplate_new)
print(Llama3CondensedQAPromptTemplate_new)


print("========== old prompt template from code")
print(Llama3PromptTemplate)
print(Llama3QAPromptTemplate)
print(Llama3CondensedQAPromptTemplate)

class Llama3ConversationBufferMemory(ConversationBufferMemory):
    @property
    def buffer_as_str(self) -> str:
        return self.get_buffer_string()

    def get_buffer_string(self) -> str:
        # See https://llama.meta.com/docs/model-cards-and-prompt-formats/meta-llama-3/
        string_messages = []
        for m in self.chat_memory.messages:
            if isinstance(m, HumanMessage):
                message = f"""{USER_HEADER}

{m.content}{EOD}"""

            elif isinstance(m, AIMessage):
                message = f"""{ASSISTANT_HEADER}

{m.content}{EOD}"""
            else:
                raise ValueError(f"Got unsupported message type: {m}")
            string_messages.append(message)

        return "".join(string_messages)
