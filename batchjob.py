from langchain_community.document_loaders import PyPDFLoader
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS



file_path = os.path.join("documents","tcsreport.pdf")
loader = PyPDFLoader(file_path)
documents = loader.load()

print(len(documents))

#step 2 : covert document to smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=2000,
    chunk_overlap=500,
)
#let us load chunks
mychunks = text_splitter.split_documents(documents)
print('total chunks :' ,len(mychunks))

#step 3 : create embeddings model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# step 4 : create faiss db

index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

# step 5 : store our chunks to vector db
vector_store.add_documents(mychunks)
print('successfully created vector db')

# step 6 : store vector store [db] permanantly
vector_store.save_local("tcs_doc_index")
print('successfully loaded vector db')

