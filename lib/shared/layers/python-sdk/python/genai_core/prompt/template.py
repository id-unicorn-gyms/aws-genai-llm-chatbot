from langchain_core.prompts import PromptTemplate
from genai_core.utils.dynamodb_reader import DynamoDBReader


class PromptTemplateRetriever:
    def __init__(self, table_name):
        self.ddb_reader = DynamoDBReader(table_name=table_name, key_name="model_key")

    def get_templates(self, provider, model_id):
        item = self.ddb_reader.read_value(f"{provider}.{model_id}")
        prompt = item["prompt"]["S"] if item and item.get("prompt") else None
        prompt_tmpl = PromptTemplate.from_template(item["prompt"]["S"]) if item and item.get("prompt") else None
        prompt_qna = item["prompt_qna"]["S"] if item and item.get("prompt_qna") else None
        prompt_qna_tmpl = PromptTemplate.from_template(item["prompt_qna"]["S"]) \
            if item and item.get("prompt_qna") else None
        prompt_condensed_qna = item["prompt_condensed_qna"]["S"] if item and item.get("prompt_condensed_qna") else None
        prompt_condensed_qna_tmpl = PromptTemplate.from_template(item["prompt_condensed_qna"]["S"]) \
            if item and item.get("prompt_condensed_qna") else None
        return {
            "prompt": prompt,
            "prompt_qna": prompt_qna,
            "prompt_condensed_qna": prompt_condensed_qna,
            "prompt_tmpl": prompt_tmpl,
            "prompt_qna_tmpl": prompt_qna_tmpl,
            "prompt_condensed_qna_tmpl": prompt_condensed_qna_tmpl
        }