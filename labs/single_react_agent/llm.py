import os
from typing import List
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
api_key = os.getenv("AZURE_OPENAI_API_KEY")

def prepare_azure_openai_completion_model(callbacks: List[callable] = []) -> AzureChatOpenAI:
    token_provider = None
    if not api_key:
        token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    return AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_ad_token_provider=token_provider,
        temperature=0,
        streaming=True,
        model_kwargs={"stream_options":{"include_usage": True}},
        callbacks=callbacks,
        api_key=api_key,
    )

def prepare_azure_openai_embeddings_model() -> AzureOpenAIEmbeddings:
    token_provider = None
    if not api_key:
        token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    return AzureOpenAIEmbeddings(
        azure_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"),
        openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
        model= os.getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
        azure_ad_token_provider = token_provider,
        api_key=api_key,
    )