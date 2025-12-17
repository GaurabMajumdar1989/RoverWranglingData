# main.py
import os
from ingest import load_document, chunk_text, ingest_with_faiss
from embed import generate_embeddings
from retrieve import top_k_similar, retrieve_with_faiss
from config import get_active_provider, USE_FAISS_INGESTION, USE_FAISS_RETRIEVAL
from generate import generate_answer

print("Starting RAG Core Application")
print(os.getcwd())



if __name__ == "__main__":
    print(f"Active LLM Provider: {get_active_provider()}")
    text = load_document("fantasy_doc.txt")
    doc_chunks = chunk_text(text)
    query = "What is happening in Aethelgard?"
    
    if USE_FAISS_INGESTION: # Ingestion phase
      ingest_with_faiss("fantasy_doc.txt", doc_chunks)
    else:  
      doc_vectors = generate_embeddings(doc_chunks)

    if USE_FAISS_RETRIEVAL:
      chunks = retrieve_with_faiss(query)
      print("\n--- Retrieved Chunks ---\n")
      for chunk in chunks:
          print(chunk)          
    else:  
      # Retrieval
      query_vector = generate_embeddings([query])[0]
      top_matches = top_k_similar(query_vector, doc_vectors, k=2)

      retrieved_chunks = [doc_chunks[idx] for idx, _ in top_matches]

      # -------- Generation --------
      answer = generate_answer(retrieved_chunks, query)

      print("\n--- Answer ---\n")
      print(answer)
