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

OpenAI.api_key = os.environ['OPENAI_API_KEY']

class Model:

  """
  Initialize the Model class with the OpenAI instance.
  :param llm: The OpenAI instance to be used.
  """
  def __init__(self, llm: OpenAI):
    self.llm = llm

  """
  Load the index from the provided file path.
  :param file_path: The path to the file to be indexed.
  :param chunk_size: The size of each chunk to be processed.
  :param chunk_overlap: The overlap between chunks.
  :return: The VectorStoreIndex object.
  """
  def load_index(self, file_path: str, chunk_size: int = 1024, chunk_overlap: int = 0) -> VectorStoreIndex:
    try:
      loader: PyMuPDFReader = PyMuPDFReader()
      if not os.path.isfile(file_path):
        raise FileNotFoundError(f'The file \'{file_path}\' does not exist.')

      documents: list = loader.load(file_path=file_path)

      service_context: ServiceContext = ServiceContext.from_defaults(chunk_size=chunk_size, chunk_overlap=chunk_overlap, llm=self.llm)

      index: VectorStoreIndex = VectorStoreIndex.from_documents(
        documents, service_context=service_context
      )
    except Exception as e:
      print('Error indexing data: %s' % e)

    return index


  """
  Create a ServiceContext object with default settings.
  :return: The ServiceContext object.
  """
  def create_service_context(self) -> ServiceContext:
    return ServiceContext.from_defaults(llm=self.llm)

  """
  Create a MultiStepQueryEngine object.
  :param index: The VectorStoreIndex object to be used.
  :param service_context: The ServiceContext object to be used.
  :param summary_of_data: A summary of the data to be indexed.
  :return: The MultiStepQueryEngine object.
  """
  def create_query_engine(self, index: VectorStoreIndex, service_context: ServiceContext, summary_of_data: str) -> MultiStepQueryEngine:

    step_decompose_transform: StepDecomposeQueryTransform = StepDecomposeQueryTransform(llm=self.llm, verbose=True)

    query_engine: MultiStepQueryEngine = index.as_query_engine(service_context=service_context)

    return MultiStepQueryEngine(
      query_engine=query_engine,
      query_transform=step_decompose_transform,
      index_summary=summary_of_data,
    )

  """
  Query the index with the provided prompt.
  :param index: The VectorStoreIndex object to be queried.
  :param prompt: The prompt to be used for the query.
  :param summary_of_data: A summary of the data to be indexed.
  :param gpt4: The OpenAI instance to be used for the query.
  :return: The response from the query.
  """
  def query(self, index: VectorStoreIndex, prompt: str, summary_of_data: str):

    service_context: ServiceContext = self.create_service_context()

    query_engine: MultiStepQueryEngine = self.create_query_engine(index, service_context,
    summary_of_data)

    query_response: query_engine = query_engine.query(prompt)

    return query_response.response

