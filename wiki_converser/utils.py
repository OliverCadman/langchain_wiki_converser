from dataclasses import dataclass


@dataclass
class PineconeCredentials:
    api_key: str
    index_name: str
    environment_region: str


def init_pinecone():
    api_key = "2d0e4803-f671-4169-a952-0d8e3dfd0f15"
    index_name = "langchain-example-db"
    environment = "us-east4-gcp"

    if api_key is None:
        msg = "PINECONE_API_KEY environment variable is not set."
        raise ValueError(msg)
    
    if index_name is None:
        msg = "PINECONE_INDEX_NAME environment variable is not set."
        raise ValueError(msg)
    
    if environment is None:
        msg = "PINECONE_ENVIRONMENT_REGION environment variable is not set."
        raise ValueError(msg)
    
    return PineconeCredentials(
        api_key=api_key,
        index_name=index_name,
        environment_region=environment
    )
