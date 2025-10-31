import streamlit as st
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import google.generativeai as genai # New import for Gemini
import time # Just for a simple "typing" effect

# --- Configuration ---
EMBEDDINGS_FILE = "osho_master_embeddings.json" # Use your latest v4 file
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3  # Number of best matching results to retrieve

# --- AI Core Loading (with Caching) ---

# This function loads your retrieval (search) model
@st.cache_resource
def load_retrieval_core(embeddings_file, model_name):
    """Loads data, builds the FAISS index, and loads the sentence model."""
    print("--- (AI CORE) Loading Retrieval (Search) Core... ---")
    
    with open(embeddings_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    embeddings = [item['embedding'] for item in data]
    texts = [item['text'] for item in data]
    embedding_array = np.array(embeddings).astype('float32')
    
    d = embedding_array.shape[1] 
    index = faiss.IndexFlatL2(d)
    index.add(embedding_array)
    
    model = SentenceTransformer(model_name)
    
    print("--- (AI CORE) Retrieval Core Loaded. ---")
    return index, model, texts, data

# This NEW function loads your generative (answer) model
@st.cache_resource
def load_generative_model():
    """Loads the Google Gemini model using the API key from secrets."""
    print("--- (AI CORE) Loading Generative (Answer) Core... ---")
    try:
        # Load API key from Streamlit's secrets
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Using Gemini 1.5 Flash - it's fast and powerful
        model = genai.GenerativeModel('models/gemini-pro-latest')
        print("--- (AI CORE) Generative Core Loaded. ---")
        return model
    except FileNotFoundError:
        st.error("Error: .streamlit/secrets.toml file not found. Please create it.")
        return None
    except KeyError:
        st.error("Error: GEMINI_API_KEY not found in .streamlit/secrets.toml. Please add it.")
        return None
    except Exception as e:
        st.error(f"An error occurred loading the generative model: {e}")
        return None

# --- Semantic Search Function (Retrieval) ---

def semantic_search(query, index, model, texts, data, top_k):
    """Runs the query, finds the top K matches, and returns the results as a list."""
    query_embedding = model.encode([query], convert_to_numpy=True).astype('float32')
    D, I = index.search(query_embedding, top_k)
    
    results = []
    for i in range(top_k):
        chunk_index = I[0][i]
        if chunk_index < len(texts):
            results.append({
                "score": 1 / (1 + D[0][i]),
                "text": texts[chunk_index],
                "source_id": data[chunk_index]['id'],
                "book": data[chunk_index]['source']
            })
    return results

# --- RAG Response Generation Function ---

def generate_response(model, query, context_chunks):
    """Builds a prompt and asks the LLM to generate an answer."""
    
    # Combine the text from all context chunks
    context = "\n\n".join([chunk['text'] for chunk in context_chunks])
    
    # Build the prompt
    prompt = f"""
    You are an AI assistant who answers questions by drawing insights from Osho's teachings.
    Based *only* on the context provided below, answer the user's question.
    If the context is not sufficient to answer the question, clearly state that.

    **Context from Osho's Discourses:**
    {context}

    **User's Question:**
    {query}

    **Your Answer:**
    """
    
    try:
        # Generate the response
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during generation: {e}"

# --- Streamlit App UI ---

# Set page title
st.set_page_config(page_title="Osho AI (RAG)", layout="wide")

# Add a title in the app
st.title("🧠 Osho AI (RAG Edition)")
st.write("Ask a question, and the AI will answer based on Osho's passages.")

# Load both AI models
try:
    retrieval_index, retrieval_model, ai_texts, ai_data = load_retrieval_core(EMBEDDINGS_FILE, MODEL_NAME)
    generative_model = load_generative_model()

    # Only show the app if both models loaded successfully
    if retrieval_index is not None and generative_model is not None:
        
        user_query = st.text_input("Your Question:", placeholder="e.g., What is the problem with suppressed sex?")

        if st.button("Ask Osho AI"):
            if user_query.strip():
                
                # --- Step 1: RETRIEVE (R) ---
                search_results = semantic_search(user_query, retrieval_index, retrieval_model, ai_texts, ai_data, TOP_K)
                
                if not search_results:
                    st.warning("I could not find any relevant passages to answer this question.")
                else:
                    
                    # --- Step 2 & 3: AUGMENT (A) & GENERATE (G) ---
                    st.subheader("Osho's Answer (Generated):")
                    
                    # Use a spinner to show "thinking"
                    with st.spinner("Thinking..."):
                        generated_answer = generate_response(generative_model, user_query, search_results)
                        
                        # Simple "typing" effect
                        answer_placeholder = st.empty()
                        full_response = ""
                        for chunk in generated_answer.split():
                            full_response += chunk + " "
                            time.sleep(0.05)
                            answer_placeholder.markdown(full_response + "▌")
                        answer_placeholder.markdown(full_response)

                    st.divider()
                    
                    # --- Step 4: Display the Sources Used ---
                    st.subheader("Passages Used as Context:")
                    for i, result in enumerate(search_results):
                        with st.expander(f"Source {i+1} (Score: {result['score']:.4f}) | {result['book']}"):
                            st.markdown(f"> {result['text']}")
                            st.caption(f"ID: {result['source_id']}")

            else:
                st.warning("Please enter a question.")

except FileNotFoundError:
    st.error(f"Error: The data file '{EMBEDDINGS_FILE}' was not found. Please run the full data pipeline first.")
except Exception as e:
    st.error(f"An unexpected error occurred during setup: {e}")