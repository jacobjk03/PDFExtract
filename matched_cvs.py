import os
import torch
from transformers import DistilBertTokenizer, DistilBertModel
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load job descriptions and resume data from CSV files
job_descriptions = pd.read_csv("Result/job_description.csv")["Job_Description"]
resume_data = pd.read_csv("Result/resume_data.csv")

# Initialize DistilBERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertModel.from_pretrained("distilbert-base-uncased")

# Tokenize and embed job descriptions
job_description_embeddings = []
for description in job_descriptions:
    inputs = tokenizer(description, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    job_description_embeddings.append(embeddings)

job_description_embeddings = np.array(job_description_embeddings)

# Tokenize and embed resumes (combine skills and education)
resume_text = resume_data["Skills"].fillna("") + " " + resume_data["Education"].fillna("")
resume_embeddings = []
for text in resume_text:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    resume_embeddings.append(embeddings)

resume_embeddings = np.array(resume_embeddings)

# Calculate cosine similarities between job descriptions and resumes
similarities = cosine_similarity(job_description_embeddings, resume_embeddings)

# Create the Matched_data folder if it does not exist
os.makedirs("Result/Matched_data", exist_ok=True)

# Process each job description and save the top CVs into a new CSV file
for i, description in enumerate(job_descriptions):
    scores = list(enumerate(similarities[i]))  # scores = [(Index of CV, Score)], similarities[1] = 1st job description
    scores.sort(key=lambda x: x[1], reverse=True)
    top_cv_indices = [idx for idx, _ in scores[:5]]

    # Create a new DataFrame for the top CVs
    top_cvs_df = resume_data.iloc[top_cv_indices]

    # Define the path for the CSV file
    csv_filename = os.path.join("Result/Matched_data", f"top_cvs_job_{i + 1}.csv")

    # Save the top CVs to the CSV file
    top_cvs_df.to_csv(csv_filename, index=False)
