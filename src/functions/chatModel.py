import os, logging, sys
from llama_index.core import (
    VectorStoreIndex,
    ServiceContext,
)
from llama_index.core.indices.query.query_transform.base import (
    StepDecomposeQueryTransform,
)
from llama_index.core.query_engine.multistep_query_engine import (
    MultiStepQueryEngine,
)
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PyMuPDFReader
from dotenv import load_dotenv

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

load_dotenv()

def init_openai():
    OpenAI.api_key = os.environ['OPENAI_API_KEY']
    gpt4 = OpenAI(temperature=0.9, model='gpt-4')
    gpt3 = OpenAI(temperature=0.9, model='gpt-3.5-turbo-0125')
    return gpt4, gpt3

def init_model(file_path: str, gpt4, gpt3):
    return file_path, gpt4, gpt3

def load_index(file_path, gpt4):
    loader = PyMuPDFReader()
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'The file \'{file_path}\' does not exist.')
    documents = loader.load(file_path=file_path)

    service_context = ServiceContext.from_defaults(chunk_size=1024, chunk_overlap=0, llm=gpt4)

    index = VectorStoreIndex.from_documents(
        documents, service_context=service_context
    )
    return index

def create_service_context(gpt4):
    return ServiceContext.from_defaults(llm=gpt4)

def create_query_engine(index, service_context, summary_of_data, gpt4):
    step_decompose_transform = StepDecomposeQueryTransform(llm=gpt4, verbose=True)
    query_engine = index.as_query_engine(service_context=service_context)
    return MultiStepQueryEngine(
        query_engine=query_engine,
        query_transform=step_decompose_transform,
        index_summary=summary_of_data,
    )

def query(index, prompt: str, summary_of_data, gpt4):
    service_context = create_service_context(gpt4)
    query_engine = create_query_engine(index, service_context, summary_of_data, gpt4)
    query_response = query_engine.query(prompt)
    return query_response.response

# Example:
# if __name__ == "__main__":
#     gpt4, gpt3 = init_openai()
#     file_path, gpt4, gpt3 = init_model('example.pdf', gpt4, gpt3)
#     index = load_index(file_path, gpt4)
#     summary_of_data = "Summary of the data"
#     prompt = "What is the meaning of life?"
#     response = query(index, prompt, summary_of_data, gpt4)
#     print(response)
