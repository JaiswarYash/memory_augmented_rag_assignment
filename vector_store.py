from qdrant_client import QdrantClient
from config import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION
from qdrant_client.models import Distance, VectorParams
import uuid

class SimpleVectorStore:
    """
    Small local vector store using Qdrant.

    Good for learning and demos and practicing for understanding Qdrant services and how to connect. Leter, use these services in production.
    In production, replace this with pgvector, Qdrant,
    Pinecone, Weaviate, OpenSearch, etc.
    """

    def __init__(self, embedding_service):
        self.embedding_service = embedding_service
        self.client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )
        if not self.client.collection_exists(QDRANT_COLLECTION):
            self.client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )


    def add(self, text: str):
        vector = self.embedding_service.embed(
            text
        )

        self.client.upsert(
            collection_name = QDRANT_COLLECTION,
            points = [
                {
                    "id": str(uuid.uuid4()),
                    "vector": vector.tolist(),
                    "payload": {"text": text},
                }
            ]
        )

    def search(self, query: str, k: int = 3):
        if not self.client.collection_exists(QDRANT_COLLECTION):
            return

        query_vector = self.embedding_service.embed(
            query
        )

        search_result = self.client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=query_vector.tolist(),
        with_payload=True,
        limit=k
        ).points

        return [point.payload["text"] for point in search_result]