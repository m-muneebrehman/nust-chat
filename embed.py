from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load your data
with open("data.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Simple chunking
chunks = [chunk.strip() for chunk in text.split("\n") if chunk.strip()]

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert to embeddings
embeddings = model.encode(chunks)

# Store in FAISS
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Save index + chunks
faiss.write_index(index, "index.faiss")

import pickle
with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("Done: embeddings stored")