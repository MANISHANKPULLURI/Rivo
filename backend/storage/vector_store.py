import os
import chromadb
from dotenv import load_dotenv

load_dotenv()

class FinancialVectorStore:
    """
    Knowledge: This class manages the 'Semantic Memory'.
    It stores the text of SEC filings so the AI can search them later.
    """
    def __init__(self):
        # We use 'PersistentClient' so the data stays on your Mac after shutdown
        self.db_path = os.getenv("VECTOR_DB_PATH")
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # We create a 'Collection' (like a folder for SEC papers)
        self.collection = self.client.get_or_create_collection(name="sec_filings")

    def add_document(self, text: str, doc_id: str, metadata: dict):
        """
        Abstraction: Hides the complexity of vectorizing text.
        """
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def query_knowledge(self, query_text: str, n_results=3):
        """
        Deterministic Retrieval: Finds the most relevant facts.
        """
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
    def close(self):
        # This properly shuts down the database connection
        self.client = None