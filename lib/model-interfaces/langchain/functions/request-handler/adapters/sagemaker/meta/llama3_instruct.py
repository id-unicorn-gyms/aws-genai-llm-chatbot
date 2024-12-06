import json
import os

from langchain_community.llms.sagemaker_endpoint import (
    LLMContentHandler,
    SagemakerEndpoint,
)

from ...base import ModelAdapter
from genai_core.registry import registry

from ...shared.meta.llama3_instruct import (
    Llama3PromptTemplate,
    Llama3QAPromptTemplate,
    Llama3CondensedQAPromptTemplate,
    Llama3ConversationBufferMemory
)


class Llama3InstructContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def clean_prompt(self, prompt):
        """Remove only the very last occurence of [/INST] tag if present"""
        if prompt.endswith("[/INST]"):
            prompt = prompt[: prompt.rfind("[/INST]")]
        return prompt

    def transform_input(self, prompt, model_kwargs) -> bytes:
        prompt = self.clean_prompt(prompt)
        input_str = json.dumps(
            {
                "inputs": prompt,
                "parameters": model_kwargs,
            }
        )
        print(f"input: {input_str}")
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes):
        output_str = output.read().decode("utf-8")
        print(output_str)
        response_json = json.loads(output_str)
        return response_json["generated_text"] if response_json else ""


class SMJumpstartLlama3InstructAdapter(ModelAdapter):

    def __init__(self, model_id, **kwargs):
        self.model_id = model_id
        self.endpoint_name = f"jumpstart-{model_id}"
        self.content_handler = Llama3InstructContentHandler()
        super().__init__(**kwargs)

    def get_memory(self, output_key=None, return_messages=False):
        return Llama3ConversationBufferMemory(
            memory_key="chat_history",
            chat_memory=self.chat_history,
            return_messages=return_messages,
            output_key=output_key,
        )

    def get_llm(self, model_kwargs={}):
        params = {}
        if "temperature" in model_kwargs:
            params["temperature"] = model_kwargs["temperature"]
        if "topP" in model_kwargs:
            params["top_p"] = model_kwargs["topP"]
        if "maxTokens" in model_kwargs:
            params["max_new_tokens"] = model_kwargs["maxTokens"]

        return SagemakerEndpoint(
            endpoint_name=self.endpoint_name,
            region_name=os.environ.get("AWS_REGION"),
            model_kwargs=params,
            endpoint_kwargs={"CustomAttributes": "accept_eula=true"},
            content_handler=self.content_handler,
            callbacks=[self.callback_handler],
        )

    def get_prompt(self):
        return self._prompt_template_with_default(Llama3PromptTemplate)

    def get_qa_prompt(self):
        return self._prompt_qna_template_with_default(Llama3QAPromptTemplate)

    def get_condense_question_prompt(self):
        return self._prompt_condensed_qna_template_with_default(Llama3CondensedQAPromptTemplate)


# Register the adapter
registry.register(r"(?i)sagemaker\.meta-LLama3-1.*\d+b.*instruct.*", SMJumpstartLlama3InstructAdapter)
