import re
import json # To save our chunks in a structured format

def chunk_text(text, max_chunk_size=500, overlap_size=50):
    """
    Chunks a given text into smaller, overlapping segments suitable for embedding.
    Attempts to chunk by paragraph first, then by sentence if paragraphs are too large.
    """
    chunks = []

    # 1. Split by Paragraphs first
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    for para in paragraphs:
        if len(para) <= max_chunk_size:
            # If paragraph is small enough, use it as a chunk
            chunks.append(para)
        else:
            # If paragraph is too large, split by sentences (or fixed size if sentences are also huge)
            sentences = re.split(r'(?<=[.!?])\s+', para) # Split by ., !, ? followed by space

            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 <= max_chunk_size: # +1 for a space
                    current_chunk += (sentence + " ").strip()
                else:
                    if current_chunk: # Add the current_chunk if not empty
                        chunks.append(current_chunk)

                        # Apply overlap
                        overlap_start_index = max(0, len(current_chunk) - overlap_size)
                        current_chunk = current_chunk[overlap_start_index:].strip() + " " + sentence + " "
                        current_chunk = current_chunk.strip() # Start new chunk with overlap
                    else: # If a single sentence is larger than max_chunk_size
                        chunks.append(sentence[:max_chunk_size])
                        current_chunk = sentence[max_chunk_size:].strip() + " " # Continue with rest

            if current_chunk: # Add any remaining text
                chunks.append(current_chunk)

    # Final pass to ensure no empty chunks
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def process_cleaned_file_for_chunking(input_filepath, output_json_filepath, book_title):
    """
    Reads a cleaned text file, chunks it, and saves the chunks with metadata.
    """
    print(f"Loading cleaned text from '{input_filepath}'...")
    with open(input_filepath, 'r', encoding='utf-8') as f:
        cleaned_text = f.read()

    print(f"Chunking text with max_chunk_size={MAX_CHUNK_SIZE}, overlap_size={OVERLAP_SIZE}...")
    text_chunks = chunk_text(cleaned_text, max_chunk_size=MAX_CHUNK_SIZE, overlap_size=OVERLAP_SIZE)

    # Add metadata to each chunk
    structured_chunks = []
    for i, chunk in enumerate(text_chunks):
        structured_chunks.append({
            "id": f"{book_title.replace(' ', '_')}_{i:04d}", # Unique ID for the chunk
            "text": chunk,
            "source": book_title,
            "chunk_number": i + 1,
            "length": len(chunk)
        })

    print(f"Generated {len(structured_chunks)} chunks.")
    print(f"Saving structured chunks to '{output_json_filepath}'...")
    with open(output_json_filepath, 'w', encoding='utf-8') as f:
        json.dump(structured_chunks, f, indent=2, ensure_ascii=False)

    print("Chunking complete and saved.")


# --- Configuration ---
MAX_CHUNK_SIZE = 500
OVERLAP_SIZE = 50

input_cleaned_file = "cleaned_book_2.txt"      # <-- Use Book 2's clean file
output_chunks_json = "osho_chunks_book_2.json" # <-- New output file for Book 2
book_title_for_metadata = "Vigyan Bhairav Tantra" # <-- New book title for metadata

# --- Run Chunking ---
if __name__ == "__main__":
    print("Starting Osho text chunking process for Book 2...")
    process_cleaned_file_for_chunking(input_cleaned_file, output_chunks_json, book_title_for_metadata)
    print("Osho text chunking process finished.")