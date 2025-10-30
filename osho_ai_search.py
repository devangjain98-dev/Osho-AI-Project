import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# --- Configuration ---
EMBEDDINGS_FILE = "osho_from_sex_to_superconsciousness_embeddings.json"
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3  # Number of best matching results to retrieve

def setup_osho_ai(embeddings_file, model_name):
    """Loads data, builds the FAISS index, and loads the model."""
    print("--- Setting Up Osho AI Core ---")
    
    # Load the chunks data
    with open(embeddings_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Prepare Embeddings and Text
    embeddings = [item['embedding'] for item in data]
    texts = [item['text'] for item in data]
    
    # Convert list of embeddings to a NumPy array (required by FAISS)
    embedding_array = np.array(embeddings).astype('float32')
    
    # Check dimensions
    d = embedding_array.shape[1] # Dimension of the vectors (should be 384 for our model)
    print(f"Loaded {len(data)} chunks with {d}-dimensional vectors.")

    # 2. Build the FAISS Index
    # We use IndexFlatL2 for simple Euclidean distance (similarity search)
    index = faiss.IndexFlatL2(d)
    index.add(embedding_array)
    print(f"FAISS index built and loaded with {index.ntotal} vectors.")

    # 3. Load the Sentence Transformer model for queries
    model = SentenceTransformer(model_name)
    print(f"Sentence Transformer model '{model_name}' loaded for query generation.")
    
    print("--- Setup Complete ---")
    return index, model, texts, data

# FIX 1: Added 'data' to the function's parameters
def semantic_search(query, index, model, texts, data, top_k):
    """Runs the query, finds the top K matches, and returns the source text."""
    
    # 1. Convert the user query into an embedding vector
    query_embedding = model.encode([query], convert_to_numpy=True).astype('float32')
    
    # 2. Search the FAISS index
    # D: Distances, I: Indices of the closest vectors
    D, I = index.search(query_embedding, top_k)
    
    print(f"\nSearching for: '{query}'")
    print("-" * 50)
    
    # 3. Retrieve and format the results
    results = []
    for i in range(top_k):
        chunk_index = I[0][i]
        
        # Guard against index out of bounds if search fails
        if chunk_index < len(texts):
            result = {
                "score": 1 / (1 + D[0][i]), # Convert L2 distance to a "similarity score" (higher is better)
                "text": texts[chunk_index],
                "source_id": data[chunk_index]['id'], # This line will now work
                "book": data[chunk_index]['source']  # This line will now work
            }
            results.append(result)
            
            # Print result directly to console
            print(f"Match {i+1} (Score: {result['score']:.4f})")
            print(f"Source: {result['book']} (ID: {result['source_id']})")
            print(f"Text: {result['text']}")
            print("-" * 50)

    return results

# --- Main Application Loop ---
if __name__ == "__main__":
    # Initialize the AI
    ai_index, ai_model, ai_texts, ai_data = setup_osho_ai(EMBEDDINGS_FILE, MODEL_NAME)

    print("\nOsho AI Ready. Ask a question about 'From Sex to Superconsciousness'.")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYour Question: ")
        
        if user_input.lower() == 'exit':
            print("Thank you for exploring the Osho AI. Farewell!")
            break
            
        if user_input.strip() == "":
            continue

        # FIX 2: Added 'ai_data' to the function call
        semantic_search(user_input, ai_index, ai_model, ai_texts, ai_data, TOP_K)