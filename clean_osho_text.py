import re

def clean_osho_text(input_filepath, output_filepath):
    """
    Reads raw text extracted from Osho PDFs, cleans it, and saves the cleaned text.
    """
    with open(input_filepath, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # --- Cleaning Steps ---
    cleaned_text = raw_text

    # 1. Remove Headers/Footers
    cleaned_text = re.sub(r'^\s*\d+\s+OSHO\b', '', cleaned_text, flags=re.MULTILINE)
    book_title_pattern = r'^\s*' + re.escape("From Sex to Superconsciousness") + r'\s*$'
    cleaned_text = re.sub(book_title_pattern, '', cleaned_text, flags=re.MULTILINE | re.IGNORECASE)

    # 2. De-hyphenation
    cleaned_text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', cleaned_text)

    # 3. Merge lines
    cleaned_text = re.sub(r'\n{2,}', '---PARAGRAPH_BREAK---', cleaned_text)
    cleaned_text = cleaned_text.replace('\n', ' ')
    cleaned_text = cleaned_text.replace('---PARAGRAPH_BREAK---', '\n\n')

    # 4. Remove extra whitespace
    cleaned_text = re.sub(r' {2,}', ' ', cleaned_text)
    
    # 5. *** MOST POWERFUL FIXES ***
    # Fix "word.Word" -> "word. Word"
    cleaned_text = re.sub(r'([.,;!?"])([a-zA-Z])', r'\1 \2', cleaned_text)
    # Fix "wordWord" -> "word Word"
    cleaned_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', cleaned_text)
    # Fix "word.word" -> "word. word"
    cleaned_text = re.sub(r'([.,;!?"])([a-z])', r'\1 \2', cleaned_text)
    
    # 6. Final cleanup
    cleaned_text = cleaned_text.strip()
    cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text) 

    # --- Save Cleaned Text ---
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
    print(f"Text cleaned and saved to '{output_filepath}'.")

# --- Configuration ---
input_file = "extracted_osho_text.txt"
output_file = "cleaned_osho_text_v4.txt"  # <-- V4 FILENAME

# --- Run Cleaning ---
if __name__ == "__main__":
    print(f"Starting cleaning process for '{input_file}'...")
    try:
        clean_osho_text(input_file, output_file)
        print("Cleaning complete.")
    except FileNotFoundError:
        print(f"ERROR: '{input_file}' not found. Please run 'extract_osho_text.py' first!")