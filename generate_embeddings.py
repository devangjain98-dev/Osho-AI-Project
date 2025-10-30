import json
from sentence_transformers import SentenceTransformer
import torch # To check for GPU availability

def generate_embeddings_for_chunks(input_json_filepath, output_json_filepath, model_name="all-MiniLM-L6-v2"):
    """
    Loads chunks from a JSON file, generates embeddings for each chunk,
    and saves the chunks with their embeddings to a new JSON file.
    """
    print(f"Loading chunks from '{input_json_filepath}'...")
    with open(input_json_filepath, 'r', encoding='utf-8') as f:
        chunks_data = json.load(f)

    # Check for GPU (CUDA) availability for faster processing
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device} (GPU detected: {torch.cuda.is_available()})")

    print(f"Loading Sentence Transformer model: '{model_name}'...")
    # This will download the model the first time it's run
    model = SentenceTransformer(model_name, device=device)
    print("Model loaded successfully.")

    texts_to_embed = [chunk['text'] for chunk in chunks_data]

    print(f"Generating embeddings for {len(texts_to_embed)} chunks...")
    # The encode method takes a list of strings and returns a list of embeddings
    embeddings = model.encode(texts_to_embed, show_progress_bar=True)
    print("Embeddings generated.")

    # Add embeddings back to the chunks data
    for i, chunk in enumerate(chunks_data):
        chunk['embedding'] = embeddings[i].tolist() # Convert numpy array to list for JSON serialization

    print(f"Saving chunks with embeddings to '{output_json_filepath}'...")
    with open(output_json_filepath, 'w', encoding='utf-8') as f:
        json.dump(chunks_data, f, indent=2, ensure_ascii=False)
    
    print("Embeddings generation complete and saved.")

# --- Configuration ---
input_chunks_json = "osho_chunks_v4.json" # Output from our chunking step
output_embeddings_json = "osho_embeddings_v4.json" # Where to save chunks with embeddings
embedding_model_name = "all-MiniLM-L6-v2" # A good balance of speed and accuracy

# --- Run Embedding Generation ---
if __name__ == "__main__":
    print("Starting Osho text embeddings generation process...")
    generate_embeddings_for_chunks(input_chunks_json, output_embeddings_json, embedding_model_name)
    print("Osho text embeddings generation process finished.")