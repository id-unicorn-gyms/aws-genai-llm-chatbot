import json
import os

from aws_lambda_powertools import Logger
from langchain_community.llms.sagemaker_endpoint import (
    LLMContentHandler,
    SagemakerEndpoint,
)

from langchain_core.prompts.prompt import PromptTemplate

from ...base import ModelAdapter
from genai_core.registry import registry

logger = Logger()

SeaLlmChatPrompt = """<|im_start|>system
You are an helpful assistant that provides accurate and concise answers to user questions with as little sentences as possible and at maximum 3 sentences. You do not repeat yourself. You avoid bulleted list or emojis.
If you're unsure about something, please say so instead of guessing.
{chat_history}
</s><|im_start|>user
{input}
</s><|im_start|>assistant
"""  # noqa:E501

SeaLlmChatQAPrompt = """<|im_start|>system
Use the following conversation history and pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. You do not repeat yourself. You avoid bulleted list or emojis.

Context: {context}

Chat history:
{chat_history}

</s><|im_start|>user
{question}
</s><|im_start|>assistant
"""  # noqa:E501

SeaLlmChatCondensedQAPrompt = """<|im_start|>system
Given the following conversation and the question at the end, rephrase the follow up input to be a standalone question, in the same language as the follow up input. You do not repeat yourself. You avoid bulleted list or emojis.

Chat history:
{chat_history}

</s><|im_start|>user
{question}
</s><|im_start|>assistant
"""  # noqa:E501


SeaLlmChatPromptTemplate = PromptTemplate.from_template(SeaLlmChatPrompt)
SeaLlmChatQAPromptTemplate = PromptTemplate.from_template(SeaLlmChatQAPrompt)
SeaLlmChatCondensedQAPromptTemplate = PromptTemplate.from_template(
    SeaLlmChatCondensedQAPrompt
)

class SeaLlmInstructContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt, model_kwargs) -> bytes:
        logger.info(f"prompt: {prompt}")
        input_str = json.dumps(
            {
                "inputs": prompt,
                "parameters": {
                    "do_sample": True,
                    "max_new_tokens": model_kwargs.get("max_new_tokens", 512),
                    "top_p": model_kwargs.get("top_p", 0.9),
                    "temperature": model_kwargs.get("temperature", 0.6),
                    "return_full_text": False,
                    "stop": ["###", "</s>"],
                },
            }
        )
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes):
        out_str = output.read().decode("utf-8")
        logger.info(f"output: {out_str}")
        response_json = json.loads(out_str)
        return response_json[0]["generated_text"]


content_handler = SeaLlmInstructContentHandler()


class SMSeaLlmChatAdapter(ModelAdapter):
    def __init__(self, model_id, **kwargs):
        self.model_id = model_id

        super().__init__(**kwargs)

    def get_llm(self, model_kwargs={}):
        params = {}
        if "temperature" in model_kwargs:
            params["temperature"] = model_kwargs["temperature"]
        if "topP" in model_kwargs:
            params["top_p"] = model_kwargs["topP"]
        if "maxTokens" in model_kwargs:
            params["max_new_tokens"] = model_kwargs["maxTokens"]

        return SagemakerEndpoint(
            endpoint_name=self.get_endpoint(self.model_id),
            region_name=os.environ["AWS_REGION"],
            content_handler=content_handler,
            model_kwargs=params,
            callbacks=[self.callback_handler],
        )

    def get_qa_prompt(self):
        return SeaLlmChatQAPromptTemplate

    def get_prompt(self):
        return SeaLlmChatPromptTemplate

    def get_condense_question_prompt(self):
        return SeaLlmChatCondensedQAPromptTemplate


# Register the adapter
registry.register(r"(?i)sagemaker\.SeaLLMs-*", SMSeaLlmChatAdapter)
registry.register(r"(?i)sagemaker\.Qwen-Qwen2-5-*", SMSeaLlmChatAdapter)
registry.register(r"(?i)sagemaker\.GoToCompany-*", SMSeaLlmChatAdapter)
