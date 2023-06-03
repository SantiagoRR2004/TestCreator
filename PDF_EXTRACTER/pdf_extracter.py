import os
import sys
import re

try:
    import pdfplumber
except:
    print('Module "pdfplumber" shall be previously installed.')



MAX_CHARACTERS = 4096 * 4  # Maximum number of characters per input (4096 tokens * 4-5 average)

def process_text(text):
    # Remove extra spaces and formatting
    text = ' '.join(text.split())  # Remove leading/trailing spaces and condense multiple spaces into one
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace characters with a single space
    return text

def convert_pdf_to_txt(pdf_file):
    text_list = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()  # Extract text from each page using pdfplumber
            text_list.append(text)  # Append the extracted text to the list

    # Combine the extracted text into a single string
    output = ' '.join(text_list)
    return output

def save_text_to_txt(txt_file, text):
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(text)

def split_text(text, max_characters):
    parts = []
    start = 0
    while start < len(text):
        parts.append(text[start : start + max_characters])  # Split the text into parts based on max_characters
        start += max_characters
    return parts

def convert_folder_to_txt(folder_path):
    # Get a list of PDF files in the folder
    pdf_files = [file for file in os.listdir(folder_path) if file.lower().endswith(".pdf")]

    # Convert each PDF file to text and save as .txt file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        output = convert_pdf_to_txt(pdf_path)

        # Remove formatting and split into parts
        processed_output = process_text(output)
        output_parts = split_text(processed_output, MAX_CHARACTERS)

        # Create a .txt file with the same name as the input PDF for each part
        base_name = os.path.splitext(pdf_file)[0]
        for i, part in enumerate(output_parts):
            txt_file = f"{base_name}_part{i+1}.txt"
            txt_path = os.path.join(folder_path, txt_file)
            save_text_to_txt(txt_path, part)
            print(f"Text saved to {txt_path}")

while True:
    print("Menu:")
    print("1. Select PDF")
    print("2. Select Folder")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        pdf_file = input("Enter the path to the PDF file: ")
        if not pdf_file:
             print(f"Invalid file path: file on path does not exist.")
        if os.path.exists(pdf_file):
            output = convert_pdf_to_txt(pdf_file)
            processed_output = process_text(output)
            output_parts = split_text(processed_output, MAX_CHARACTERS)
            for i, part in enumerate(output_parts):
                txt_file = f"output_part{i+1}.txt"
                save_text_to_txt(txt_file, part)
                print(f"Text saved to {txt_file}")
        else:
            print(f"Invalid PDF file path: '{pdf_file}' does not exist.")
    elif choice == "2":
        folder_path = input("Enter the path to the folder containing PDF files (leave blank for current folder): ")
        if not folder_path:
            folder_path = os.path.join(sys.path[0], "")  # Use current folder of the script
        if os.path.exists(folder_path):
            convert_folder_to_txt(folder_path)
        else:
            print(f"Invalid folder path: '{folder_path}' does not exist.")
    elif choice == "3":
        break
    else:
        print("Invalid choice. Please try again.")
