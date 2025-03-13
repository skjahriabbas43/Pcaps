import os
import argparse

def search_keyword_in_files(directory, keyword):
    try:
        # Ensure the directory exists
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        # Loop through all files in the specified directory
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        if keyword in line:
                            print(f"Match found in {filename} at line {i + 1}:")
                            print(f"{i + 1}: {line.strip()}")
                            print("-" * 80)
            except IOError as e:
                print(f"Error reading file {filepath}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search keyword in text files and display matching lines.")
    parser.add_argument('-k', '--keyword', required=True, help="Keyword to search for")
    args = parser.parse_args()

    directory = r"C:\Users\Admin\OneDrive - Subex Limited\Documents\Rules\sectriolabupdates\Rules"
    search_keyword_in_files(directory, args.keyword)
