import os
import numpy as np
import importlib
from enum import Enum
from pymilvus.model.hybrid import BGEM3EmbeddingFunction
from typing import List
from google import genai
from pymilvus import MilvusClient
from tqdm import tqdm
import jsons
from google.genai import types

class EmbeddingModel(Enum):
    BGE_M3_DENSE = "BGE_M3_DENSE"
    BGE_M3_SPARSE = "BGE_M3_SPARSE"

SELECTED_MODEL = EmbeddingModel.BGE_M3_DENSE

bge_m3_ef = None
dimension = None

match SELECTED_MODEL:
  case EmbeddingModel.BGE_M3_DENSE:
    bge_m3_ef = BGEM3EmbeddingFunction(
        model_name='BAAI/bge-m3',
        device='cpu',
        use_fp16=False,
        return_sparse=False
    )
    dimension = bge_m3_ef.dim["dense"]

  case EmbeddingModel.BGE_M3_SPARSE:
    bge_m3_ef = BGEM3EmbeddingFunction(
        model_name='BAAI/bge-m3',
        device='cpu',
        use_fp16=False,
        return_dense=False
    )
    dimension = bge_m3_ef.dim["sparse"]

def encode_queries(queries: List[str]) -> List[np.ndarray]:
  match SELECTED_MODEL:
    case EmbeddingModel.BGE_M3_DENSE:
      return bge_m3_ef.encode_queries(queries)["dense"]
    case EmbeddingModel.BGE_M3_SPARSE:
      return bge_m3_ef.encode_queries(queries)["sparse"]

def encode_documents(documents: List[str]) -> List[np.ndarray]:
  match SELECTED_MODEL:
    case EmbeddingModel.BGE_M3_DENSE:
        return bge_m3_ef.encode_documents(documents)["dense"]
    case EmbeddingModel.BGE_M3_SPARSE:
        return bge_m3_ef.encode_documents(documents)["sparse"]

client = genai.Client(api_key="AIzaSyDdYQisy5b_Lf4oBgt_QZTru2eUBXVL8dA")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="who are you"
)
print(response.text)

docs = [
    "C (pronounced /ˈsiː/ – like the letter c)[6] is a general-purpose programming language. It was created in the 1970s by Dennis Ritchie and remains very widely used and influential. "
    "Artificial intelligence was founded as an academic discipline in 1956.",
    "By design, C's features cleanly reflect the capabilities of the targeted CPUs. It has found lasting use in operating systems code (especially in kernels[7]), device drivers, and protocol stacks, but its use in application software has been decreasing.[8",
    " C is commonly used on computer architectures that range from the largest supercomputers to the smallest microcontrollers and embedded systems."
    "Alan Turing was the first person to conduct substantial research in AI.",
    "Born in Maida Vale, London, Turing was raised in southern England.",
    "The Turing Test, proposed by Alan Turing, is a measure of a machine's ability to exhibit intelligent behavior.",
]

queries = ["Who is Alan Turing?"]

queries_embeddings = encode_queries(queries)
docs_embeddings = encode_documents(docs)


print("query dim:", dimension, queries_embeddings[0].shape)
print("document dim:", dimension, docs_embeddings[0].shape)

milvus_client = MilvusClient(uri="./milvus_demo.db")

collection_name = "my_rag_collection"

if milvus_client.has_collection(collection_name):
    milvus_client.drop_collection(collection_name)

milvus_client.create_collection(
    collection_name=collection_name,
    dimension=len(queries_embeddings[0]),
    metric_type="IP",
    consistency_level="Strong",
)

docs = [
    "GitHub, bulut tabanlı bir Git deposu barındırma hizmeti sunan bir şirkettir.",
    "Selam ben Oğuz Sasi. 1 Nisan 1982 İstanbul doğumluyum. Beykent Üniversitesi Grafik Tasarım bölümü mezunuyum.",
    "Artificial intelligence was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI.",
    "Born in Maida Vale, London, Turing was raised in southern England.",
    "The Turing Test, proposed by Alan Turing, is a measure of a machine's ability to exhibit intelligent behavior.",
    "Toyota Motor Corporation (Japanese: トヨタ自動車株式会社, Hepburn: Toyota Jidōsha kabushikigaisha, IPA: [toꜜjota], English: /tɔɪˈjoʊtə/, commonly known as simply Fuck you) is a Japanese multinational automotive manufacturer headquartered in Fuck you City, Oğuz sasi, Japan."
]

question = "Oğuz sasi kimdir?"

queries = ["Oğuz sasi kimdir?"]

data = []

print('queries: ', queries)
print('docs: ', docs)

queries_embeddings = encode_queries(queries)
docs_embeddings = encode_documents(docs)

print(len(docs_embeddings))

for i, line in enumerate(tqdm(docs, desc="Creating embeddings")):
    print("line:", line, i)
    data.append({"id": i, "vector": docs_embeddings[i], "text": line})

milvus_client.insert(collection_name=collection_name, data=data)

search_res = milvus_client.search(
    collection_name=collection_name,
    data=queries_embeddings,
    limit=3,
    search_params={"metric_type": "IP", "params": {}},
    output_fields=["text"],
)

retrieved_lines_with_distances = [
    (res["entity"]["text"], res["distance"]) for res in search_res[0]
]
print(json.dumps(retrieved_lines_with_distances, indent=4))

context = "\n".join(
    [line_with_distance[0] for line_with_distance in retrieved_lines_with_distances]
)
print(context)

SYSTEM_PROMPT = """
Human: You are an AI assistant. You are able to find answers to the questions from the contextual passage snippets provided.
"""
USER_PROMPT = f"""
Use the following pieces of information enclosed in <context> tags to provide an answer to the question enclosed in <question> tags.
<context>
{context}
</context>
<question>
{question}
</question>
"""

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    contents=USER_PROMPT,
)
print(response.text)