# pip install -r requirements.txt 
import numpy as np
import os
from dotenv import load_dotenv
import torch
import json

import time
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from typing import List
from langchain.vectorstores import Chroma

# pip install numpy sentence_transformers
# pip install transformers==4.47.0
# pip install langchain==0.3.13
# pip install langchain-community==0.3.13
# pip install --upgrade pymilvus
# pip install "pymilvus[model]"
from pymilvus.model.dense import JinaEmbeddingFunction

# pip install chromadb
import chromadb

# pip install langchain_google_genai          

# gpu 사용 여부 확인
torch.cuda.is_available()
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
print(f"Using device: {device}")

load_dotenv()

# 통합 JSON file 가져오기
with open('C:/Users/Admin/Desktop/Json_test_for_RAG/full_data.json','r', encoding='utf-8') as json_file:
  json_data = json.load(json_file)

  jina_ef = JinaEmbeddingFunction(
    model_name="jina-embeddings-v3", # Defaults to `jina-embeddings-v3`
    api_key=os.environ.get('JINAAI_API_KEY'), # Provide your Jina AI API key
    task="retrieval.passage", # Specify the task
    dimensions=1024, # Defaults to 1024
)

### TEXT SPLIT
# Markdown split -> Text split -> Document Class
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3")
]
md_splitter = MarkdownHeaderTextSplitter(
      headers_to_split_on=headers_to_split_on, strip_headers=False
  )

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=200,
    # length_function=lambda text: len(jina_ef.tokenizer.encode(text)),

)

docs_preprocessed = []
for pdf_text in json_data:
  md_doc_split = md_splitter.split_text(pdf_text['content'])
  doc_split = splitter.split_documents(md_doc_split)
  doc_split_dicts = [
    {"text": doc.page_content, "metadata": doc.metadata} for doc in doc_split
  ]
  docs_preprocessed.append(doc_split_dicts) # Serializable 하게 변환

### EMBED TEXT TO VECTOR
# embedding with jina_ai_embedding_v3 : 20-30개씩 끊어서 해야함
docs_embeddings = []
for doc in docs_preprocessed:
  embed_vec = jina_ef.encode_documents(doc)
  docs_embeddings.append(embed_vec)


# embedded vectors of chunks in markdown (saved locally)
embedded = np.load('./embeddings_test.npy')

### ADD TO CHROMADB

### QUERY EMBED
# ChromaDB에 저장했으므로 불러온다
client = chromadb.Client()
collection = client.get_collection(name="chroma_db_test")

query_embedding =  jina_ef.encode_queries([
    "전곡역 제일풍경채 리버파크의 공급 위치는 어딘가요?",
    "금정 메종카운티의 특별공급 당첨자 발표일은 언제인가요?",
    "무주택세대원의 기준은 무엇인가요?"
])

### RETRIEVER
# Chroma DB에서 검색
search_results = collection.query(
    query_embeddings=query_embedding,
    n_results=3  # 상위 3개 결과 반환
)

print("검색 결과:")
for doc in search_results['documents']:
    print(doc, sep = "\n")

### CONNECT LLM -----