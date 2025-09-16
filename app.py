'''
     this file contains real time job
     a rest api that accepts question from postman
     note : question should be in json format

     step 1 : read question
     step 2 : covert question to vector using embedding model
     step 3 : load faiss db => tcs_doc_index
     step 4 : ask question to faiss db, get relevant chunk
     step 5 : make prompt with question, and context
     step 6 : pass prompt to any free LLMs (openai,gemini,huggingface)
     step 7 : once we get the answer from LLM, return answer to POSTMAN

'''

from flask import Flask
from flask import request
from flask import jsonify
from langchain_huggingface import HuggingFaceEmbeddings
import faiss
from langchain_community.vectorstores import FAISS
import os
from openai import OpenAI

app=Flask(__name__)

@app.route("/tcs",methods=["POST"])
def tcs_chatbot_api():
    #step 1 : read question from postman
    data=request.get_json()
    question= data.get("tcs_question")
    # step 2 : covert question to vector using embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
     #step 3 : load faiss db => tcs_doc_index
    new_vector_store = FAISS.load_local(
          "tcs_doc_index", embeddings, allow_dangerous_deserialization=True
     )
     # step 4 : ask question to faiss db, get relevant chunk
    context = new_vector_store.similarity_search("what is the revenue of tcs",k=1)

    #step 5 : make proper prompt
    prompt = f'''
           i am going ask a question ,please answer based on the given context.
          if you don't get answer from the context,then dont answer
          
          question : {question}
           context : {context}
     '''
    
    #step 6 : pass prompt to any free LLMs (openai,gemini,huggingface)
   
    os.environ["OPENAI_API_KEY"] = ""

    client = OpenAI()

    response = client.responses.create(
         model="gpt-4o-mini",
         input= prompt
     )

    return jsonify ( {"gpt response_con":str(response.output_text)})

app.run()
    

           
            
         
    
   


