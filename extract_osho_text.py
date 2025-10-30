import pdfplumber
import os

def extract_text_from_pdf(pdf_path, output_txt_path, num_pages=None):
    """
    Extracts text from a PDF file.
    Optionally extracts only a specified number of initial pages.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at '{pdf_path}'")
        return

    full_text = []
    print(f"Opening PDF: '{pdf_path}'")
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        
        # Determine pages to process
        pages_to_process = pdf.pages
        if num_pages and num_pages > 0:
            pages_to_process = pdf.pages[:num_pages]
            total_pages_to_extract = min(num_pages, total_pages)
        else:
            total_pages_to_extract = total_pages
        
        print(f"Extracting text from {total_pages_to_extract} pages...")

        for i, page in enumerate(pages_to_process):
            print(f"Extracting text from page {i + 1}...")
            
            # *** Setting x_tolerance=1 ***
            text = page.extract_text(x_tolerance=1) 
            
            if text:
                full_text.append(text)
            else:
                full_text.append(f"\n[No text found on page {i+1}, potentially an image-only page]\n")
    
    extracted_raw_text = "\n".join(full_text)

    # Save to file
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write(extracted_raw_text)
    
    print(f"Successfully extracted text from {total_pages_to_extract} pages of '{os.path.basename(pdf_path)}' to '{output_txt_path}'.")

    # Display preview
    print("\n--- BEGIN EXTRACTED CONTENT PREVIEW (first 500 characters) ---")
    preview = extracted_raw_text[:500] if len(extracted_raw_text) > 500 else extracted_raw_text
    print(preview)
    print("--- END PREVIEW ---")
    print(f"\nCheck the file '{output_txt_path}' for the full extracted text.")

# --- Configuration ---
pdf_file = "From Sex to Superconsciousness"
pdf_path = f"{pdf_file}.pdf"
output_text_file = "extracted_osho_text.txt"
# We'll extract 10 pages for a fast test.
NUM_PAGES_TO_EXTRACT = 10 

if __name__ == "__main__":
    print("Starting PDF text extraction process...")
    # *** THIS IS THE FIX (line 64) ***
    extract_text_from_pdf(pdf_path, output_text_file, NUM_PAGES_TO_EXTRACT) # Fixed variable name
    print("PDF text extraction process finished.")