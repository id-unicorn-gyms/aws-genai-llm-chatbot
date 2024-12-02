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
table_name = "model-config"
key_name = "model_id"
key_value = "llama3"

reader = config.DynamoDBReader(table_name, key_name)
prompt_default = reader.read_value(key_value)["prompt_default"]['S']
prompt_qna = reader.read_value(key_value)["prompt_qna"]['S']
prompt_condensed_qna = reader.read_value(key_value)["prompt_condensed_qna"]['S']

Llama3Prompt_new = prompt_default
Llama3QAPrompt_new = prompt_qna
Llama3CondensedQAPrompt_new = prompt_condensed_qna

Llama3PromptTemplate = PromptTemplate.from_template(Llama3Prompt_new)
Llama3QAPromptTemplate = PromptTemplate.from_template(Llama3QAPrompt_new)
Llama3CondensedQAPromptTemplate = PromptTemplate.from_template(Llama3CondensedQAPrompt_new)



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
