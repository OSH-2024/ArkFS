import os
import torch
import clip
from PIL import Image
import numpy as np
import faiss

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Load the CLIP model and preprocessing function
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Directory containing the files
file_dir = r"C:\programming\codefile\newgit\osh\file_system_resembling_shell\target_folder"

# Initialize lists for features and file paths
features = []
file_paths = []

# Process the files in the directory
for fname in os.listdir(file_dir):
    file_path = os.path.join(file_dir, fname)
    try:
     if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # Process image files
        image = preprocess(Image.open(file_path)).unsqueeze(0).to(device)
        with torch.no_grad():
            feature = model.encode_image(image)
            features.append(feature.cpu().numpy())
            file_paths.append(file_path)
     # elif fname.lower().endswith('.txt'):
     #     # Process text files (if needed)
     #     with open(file_path, 'r') as f:
     #         text = f.read().strip()
     #     text_input = clip.tokenize([text]).to(device)
     #     with torch.no_grad():
     #         feature = model.encode_text(text_input)
     #     features.append(feature.cpu().numpy())
     #     file_paths.append(file_path)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Convert the list of feature vectors to a NumPy array and normalize
features = np.vstack(features)
features /= np.linalg.norm(features, axis=1, keepdims=True)

# Create a FAISS index and add the features
index = faiss.IndexFlatIP(features.shape[1])
index.add(features)

# Define the search function
def search_files(query, k=5):
    query_input = clip.tokenize([query]).to(device)
    with torch.no_grad():
        query_feature = model.encode_text(query_input).cpu().numpy()
    query_feature /= np.linalg.norm(query_feature)

    D, I = index.search(query_feature, k)
    return [(file_paths[i], D[0][j]) for j, i in enumerate(I[0])]

# Main loop for querying
while True:
    query = input("Enter search query (or 'exit' to quit): ")
    if query.lower() == 'exit':
        break
    results = search_files(query, k=5)
    for file_path, score in results:
        print(f"File: {file_path}, Similarity: {score:.4f}")