import re

def clean_osho_text(input_filepath, output_filepath):
    """
    Reads raw text extracted from Osho PDFs, cleans it, and saves the cleaned text.
    This version is simplified for 'Vigyan Bhairav Tantra'.
    """
    with open(input_filepath, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # --- Cleaning Steps ---
    cleaned_text = raw_text

    # 1. De-hyphenation (join words split by a hyphen at a line break)
    cleaned_text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', cleaned_text)

    # 2. Merge short lines and re-flow paragraphs
    # This is the most important step for this book
    cleaned_text = re.sub(r'\n{2,}', '---PARAGRAPH_BREAK---', cleaned_text)
    cleaned_text = cleaned_text.replace('\n', ' ')
    cleaned_text = cleaned_text.replace('---PARAGRAPH_BREAK---', '\n\n')

    # 3. Remove excessive whitespace
    cleaned_text = re.sub(r' {2,}', ' ', cleaned_text)

    # 4. Fix "word.Word" -> "word. Word"
    cleaned_text = re.sub(r'([.,;!?"])([a-zA-Z])', r'\1 \2', cleaned_text)
    # Fix "wordWord" -> "word Word"
    cleaned_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', cleaned_text)
    # Fix "word.word" -> "word. word"
    cleaned_text = re.sub(r'([.,;!?"])([a-z])', r'\1 \2', cleaned_text)

    # 5. Final cleanup
    cleaned_text = cleaned_text.strip()
    cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text) 

    # --- Save Cleaned Text ---
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
    print(f"Text cleaned and saved to '{output_filepath}'.")

# --- Configuration ---
input_file = "extracted_book_2.txt"  
output_file = "cleaned_book_2.txt"  # New output file

# --- Run Cleaning ---
if __name__ == "__main__":
    print(f"Starting cleaning process for '{input_file}'...")
    clean_osho_text(input_file, output_file)
    print("Cleaning complete.")