import chromadb
from typing import List, Dict, Any, Optional
from ..config.settings import settings
from .llm_service import llm_service

class RAGService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
        # Get or create the collection
        self.collection_name = "legal_clauses"
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_clauses(self, document_id: int, clauses: List[Dict[str, Any]]):
        """
        Adds a list of clauses to the vector store.
        Each clause is expected to have: 'type', 'content', 'risk_level', and optional 'page_num'.
        """
        if not clauses:
            return

        ids = []
        embeddings = []
        metadatas = []
        documents = []

        for idx, clause in enumerate(clauses):
            clause_id = f"doc_{document_id}_clause_{idx}"
            content = clause.get("content", "")
            if not content.strip():
                continue
                
            # Generate embedding using LLM service
            embedding = llm_service.generate_embeddings(content)

            ids.append(clause_id)
            embeddings.append(embedding)
            metadatas.append({
                "document_id": document_id,
                "clause_type": clause.get("type", "Other"),
                "risk_level": clause.get("risk_level", "Low"),
                "page_num": clause.get("page_num", 0)
            })
            documents.append(content)

        if ids:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents
            )

    def query_clauses(self, query_text: str, document_id: Optional[int] = None, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Searches ChromaDB for relevant clauses.
        Optionally filters by document_id.
        """
        query_embedding = llm_service.generate_embeddings(query_text)
        
        where_clause = None
        if document_id is not None:
            where_clause = {"document_id": document_id}

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_clause
        )

        formatted_results = []
        if results and "documents" in results and results["documents"]:
            # Chroma DB query returns a list of lists since it supports batch queries
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            distances = results["distances"][0] if "distances" in results else [0.0] * len(docs)
            ids = results["ids"][0]

            for i in range(len(docs)):
                formatted_results.append({
                    "id": ids[i],
                    "content": docs[i],
                    "metadata": metas[i],
                    "distance": distances[i]
                })

        return formatted_results

    def delete_document_clauses(self, document_id: int):
        """
        Deletes all clause embeddings associated with a document.
        """
        self.collection.delete(
            where={"document_id": document_id}
        )

rag_service = RAGService()
