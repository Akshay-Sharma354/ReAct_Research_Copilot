"""
RETRIEVER MODULE - Document Chunking, Embeddings, and Search
SIMPLIFIED VERSION using scikit-learn (no FAISS needed!)

This module handles:
1. Breaking large documents into chunks (smaller pieces)
2. Converting chunks to embeddings (numerical representations)
3. Searching for relevant chunks using similarity search

Think of it like:
- Documents = Books
- Chunks = Paragraphs
- Embeddings = Converting paragraphs to numbers
- Search = Finding most similar paragraphs to a query
"""

import os
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple

# sentence-transformers: Converts text to embeddings (numerical vectors)
from sentence_transformers import SentenceTransformer

# sklearn: For similarity search (much simpler than FAISS!)
from sklearn.metrics.pairwise import cosine_similarity

print("✅ Retriever module loaded successfully!")


class DocumentRetriever:
    """
    Handles document chunking, embedding, and retrieval.
    
    Process:
    1. Load documents from corpus folder
    2. Split into chunks (small pieces for better search)
    3. Convert chunks to embeddings (numbers)
    4. Search for relevant chunks using similarity
    5. Return most similar chunks
    """
    
    def __init__(self, corpus_path: str = "./corpus", embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the retriever.
        
        Args:
            corpus_path: Folder containing documents
            embedding_model: Which model to use for embeddings
                - "all-MiniLM-L6-v2": Fast, good for simple queries (recommended)
                - "all-mpnet-base-v2": Slower, better quality (if you have time)
        """
        self.corpus_path = corpus_path
        
        # Load embedding model
        print(f"📚 Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Will store documents and chunks
        self.documents = []  # Original documents
        self.chunks = []     # Split documents
        self.embeddings = None  # Numerical representations
        
        # Load and prepare everything
        self.load_and_prepare()
    
    def load_documents(self) -> List[Dict]:
        """
        Load documents from corpus folder.
        
        Looks for:
        - .md (markdown) files
        - .txt (text) files
        
        Returns:
            List of documents with content
        """
        documents = []
        corpus_folder = Path(self.corpus_path)
        
        # Check if folder exists
        if not corpus_folder.exists():
            print(f"⚠️  Corpus folder not found: {self.corpus_path}")
            return documents
        
        # Read all markdown and text files
        for file_path in corpus_folder.glob("*.*"):
            if file_path.suffix in [".md", ".txt"]:
                print(f"📄 Loading: {file_path.name}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    documents.append({
                        'filename': file_path.name,
                        'content': content,
                        'path': str(file_path)
                    })
                except Exception as e:
                    print(f"❌ Error loading {file_path.name}: {e}")
        
        print(f"✅ Loaded {len(documents)} documents")
        return documents
    
    def chunk_documents(self, chunk_size: int = 300, overlap: int = 50) -> List[Dict]:
        """
        Split documents into chunks (small pieces).
        
        Why chunks?
        - Better search relevance (find exact passages)
        - Fits in model context windows
        - Faster embedding
        
        Args:
            chunk_size: Characters per chunk (300 = ~50 words)
            overlap: Characters to overlap (helps maintain context)
        
        Returns:
            List of chunks with metadata
        """
        chunks = []
        chunk_id = 0
        
        for doc in self.documents:
            content = doc['content']
            filename = doc['filename']
            
            # Split document into overlapping chunks
            for start_idx in range(0, len(content), chunk_size - overlap):
                end_idx = min(start_idx + chunk_size, len(content))
                chunk_text = content[start_idx:end_idx]
                
                # Skip very small chunks
                if len(chunk_text.strip()) > 20:
                    chunks.append({
                        'id': chunk_id,
                        'text': chunk_text,
                        'filename': filename,
                        'start': start_idx,
                        'end': end_idx,
                        'document_id': self.documents.index(doc)
                    })
                    chunk_id += 1
        
        print(f"✅ Created {len(chunks)} chunks from {len(self.documents)} documents")
        return chunks
    
    def create_embeddings(self) -> np.ndarray:
        """
        Convert chunks to embeddings (numerical vectors).
        
        Embedding: Converts text to numbers that capture meaning
        - Similar text = similar numbers
        - Used for similarity search
        
        Returns:
            Numpy array of embeddings (384 dimensions for MiniLM)
        """
        chunk_texts = [chunk['text'] for chunk in self.chunks]
        
        print(f"🔢 Converting {len(chunk_texts)} chunks to embeddings...")
        
        # Convert text to embeddings (this takes a moment)
        embeddings = self.embedding_model.encode(
            chunk_texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        print(f"✅ Created embeddings with shape: {embeddings.shape}")
        return embeddings
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant chunks given a query.
        
        Steps:
        1. Convert query to embedding
        2. Calculate similarity with all chunks
        3. Return top_k most similar chunks
        
        Args:
            query: Search query (natural language)
            top_k: Number of top results to return
        
        Returns:
            List of most relevant chunks
        """
        if self.embeddings is None:
            print("❌ No embeddings found!")
            return []
        
        # Convert query to embedding
        query_embedding = self.embedding_model.encode(
            [query],
            convert_to_numpy=True
        )
        
        # Calculate similarity between query and all chunks
        # cosine_similarity returns values between -1 and 1
        # 1 = identical, 0 = orthogonal, -1 = opposite
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get indices of top_k most similar chunks
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Prepare results
        results = []
        for idx in top_indices:
            if idx >= 0:  # Valid index
                chunk = self.chunks[idx]
                similarity_score = float(similarities[idx])
                
                # Convert similarity score to percentage (0-1)
                # Cosine similarity ranges from -1 to 1, we normalize to 0-1
                normalized_similarity = (similarity_score + 1) / 2
                
                results.append({
                    'id': chunk['id'],
                    'text': chunk['text'],
                    'filename': chunk['filename'],
                    'similarity': normalized_similarity,
                    'start': chunk['start'],
                    'end': chunk['end']
                })
        
        return results
    
    def load_and_prepare(self):
        """
        Load documents, chunk them, and prepare for search.
        This is the complete pipeline.
        """
        print("\n" + "="*50)
        print("📚 PREPARING RETRIEVER")
        print("="*50)
        
        # Step 1: Load documents
        self.documents = self.load_documents()
        
        if not self.documents:
            print("⚠️  No documents found in corpus!")
            return
        
        # Step 2: Chunk documents
        self.chunks = self.chunk_documents()
        
        # Step 3: Create embeddings
        self.embeddings = self.create_embeddings()
        
        print("="*50)
        print("✅ RETRIEVER READY!")
        print("="*50 + "\n")
    
    def get_stats(self) -> Dict:
        """Get statistics about the retriever."""
        return {
            'num_documents': len(self.documents),
            'num_chunks': len(self.chunks),
            'embedding_dimension': self.embeddings.shape[1] if self.embeddings is not None else None,
        }


# Example usage (if you run this file directly)
if __name__ == "__main__":
    # Create retriever
    retriever = DocumentRetriever()
    
    # Example search
    print("\n🔍 EXAMPLE SEARCH:")
    print("-" * 50)
    
    query = "What are neural networks?"
    print(f"Query: {query}\n")
    
    results = retriever.search(query, top_k=3)
    
    for i, result in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"  Document: {result['filename']}")
        print(f"  Relevance: {result['similarity']:.2%}")
        print(f"  Text: {result['text'][:150]}...")
        print()