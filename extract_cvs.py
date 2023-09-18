import os
import PyPDF2 as pdf
import re
import csv

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file_path):
    try:
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_reader = pdf.PdfReader(pdf_file)
            resume_text = ''

            for page in pdf_reader.pages:
                resume_text += page.extract_text()

            return resume_text.strip()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Function to extract skills under a "Skills" subheading
def extract_skills_from_text(text):
    # Search for the "Skills" subheading and the text below it
    skills_pattern = r'Skills\n((?:.*?\n)+)'
    skills_section_match = re.search(skills_pattern, text, re.IGNORECASE)
    
    if skills_section_match:
        skills_text = skills_section_match.group(1)
        # Extract skills from the skills text
        skills = [skill.strip() for skill in skills_text.split('\n') if skill.strip()]
        return skills
    else:
        return []

# Function to extract education details
def extract_education(text):
    # Define a pattern to search for education information (customize this based on your dataset)
    education_pattern = r'(?i)education[^a-z]*((?:(?![a-z]+:)[^\n])+)'
    education_match = re.search(education_pattern, text, re.DOTALL)
    
    if education_match:
        education = education_match.group(1).strip()
        return education
    else:
        return None

# Function to process resumes in a folder
def process_resumes_in_folder(folder_path, output_csv):
    job_role = os.path.basename(folder_path)

    with open(output_csv, mode='a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_file_path = os.path.join(root, file)
                    extracted_text = extract_text_from_pdf(pdf_file_path)

                    if extracted_text:
                        skills = extract_skills_from_text(extracted_text)
                        education = extract_education(extracted_text)

                        # Store the extracted data in a CSV file
                        csv_writer.writerow([job_role, ', '.join(skills), education])

# Main program
if __name__ == "__main__":
    resumes_folder = "data"
    output_csv = "Result/resume_data.csv"

    # Check if the directory exists
    if not os.path.exists("Result"):
    # If it doesn't exist, create it
        os.makedirs("Result")

    # Write CSV file if doesn't exist
    if not os.path.isfile(output_csv):
        with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Job_Role', 'Skills', 'Education'])

    for job_role_folder in os.listdir(resumes_folder):
        job_role_folder_path = os.path.join(resumes_folder, job_role_folder)

        if os.path.isdir(job_role_folder_path):
            print(f"Processing job role: {job_role_folder}")
            process_resumes_in_folder(job_role_folder_path, output_csv)

    print("Extraction completed. Data stored in 'resume_data.csv'.")
