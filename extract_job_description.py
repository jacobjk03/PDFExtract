import os
import pandas as pd
from datasets import load_dataset

# Define the CSV file path
csv_file_path = "Result/job_description.csv"

# Check if the CSV file already exists
if not os.path.isfile(csv_file_path):
    # The CSV file doesn't exist, so create an empty DataFrame with the desired columns
    df = pd.DataFrame(columns=["Job Description"])

    # Save the empty DataFrame to create the CSV file
    df.to_csv(csv_file_path, index=False)
    print(f"Created an empty CSV file: {csv_file_path}")

# Load the Hugging Face dataset by name
dataset = load_dataset("jacob-hugging-face/job-descriptions")

# Access the dataset's "train" split (you can change to "test" or "validation" if needed)
data = dataset["train"]

# Extract only 10-15 job descriptions
job_descriptions = data["job_description"][:15]

# Create a DataFrame with the job descriptions
df = pd.DataFrame({"Job_Description": job_descriptions})

# Save the DataFrame to a CSV file with proper encoding
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

print(f"Job descriptions saved to {csv_file_path}")