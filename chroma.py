import chromadb
import pandas as pd

client = chromadb.PersistentClient(path="/Users/muralik/chroma_db")
print(client.list_collections())

collection = client.get_collection(name="JPMorgan")

# 1. Fetch the raw data dictionary
raw_data = collection.get()

# 2. Convert directly to a DataFrame
df = pd.DataFrame({
    'id': raw_data['ids'],
    'document': raw_data['documents'],
    'metadata': raw_data['metadatas']
})

print(df)

