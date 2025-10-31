import json

# --- Configuration ---
file_book_1 = "osho_embeddings_v4.json"      # Your first book
file_book_2 = "osho_embeddings_book_2.json"  # Your second book

master_output_file = "osho_master_embeddings.json" # The final combined file

# --- Run Combining ---
if __name__ == "__main__":
    print(f"Loading Book 1: '{file_book_1}'...")
    with open(file_book_1, 'r', encoding='utf-8') as f:
        data_book_1 = json.load(f)
    print(f"Loaded {len(data_book_1)} chunks from Book 1.")

    print(f"Loading Book 2: '{file_book_2}'...")
    with open(file_book_2, 'r', encoding='utf-8') as f:
        data_book_2 = json.load(f)
    print(f"Loaded {len(data_book_2)} chunks from Book 2.")

    # Combine the lists
    master_data = data_book_1 + data_book_2
    print(f"\nTotal chunks combined: {len(master_data)}")

    # Save the master file
    print(f"Saving master embeddings file to '{master_output_file}'...")
    with open(master_output_file, 'w', encoding='utf-8') as f:
        json.dump(master_data, f, indent=2, ensure_ascii=False)

    print("Combining complete. You are ready to update 'app.py'!")