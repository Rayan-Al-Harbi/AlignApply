import os

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
USE_MEMORY = os.getenv("QDRANT_MEMORY", "false").lower() == "true"

if QDRANT_URL:
    qdrant = QdrantClient(url=QDRANT_URL)
elif USE_MEMORY:
    qdrant = QdrantClient(":memory:")
else:
    qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

COLLECTION_NAME = "cv_chunks"
EMBEDDING_DIM = 384

# Cache embeddings to avoid redundant model calls
_embedding_cache: dict[str, list[float]] = {}


def get_embedding(text: str) -> list[float]:
    if text in _embedding_cache:
        return _embedding_cache[text]
    vec = embedding_model.encode(text).tolist()
    _embedding_cache[text] = vec
    return vec


def batch_embed(texts: list[str]) -> list[list[float]]:
    """Embed multiple texts in a single model call — much faster than one-by-one."""
    uncached = [t for t in texts if t not in _embedding_cache]
    if uncached:
        vectors = embedding_model.encode(uncached).tolist()
        for t, v in zip(uncached, vectors):
            _embedding_cache[t] = v
    return [_embedding_cache[t] for t in texts]


def clear_embedding_cache():
    _embedding_cache.clear()


def store_cv_chunks(chunks: list[str]):
    if not qdrant.collection_exists(COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE,
            ),
        )

    # Batch embed all chunks in one call
    vectors = batch_embed(chunks)
    points = [
        PointStruct(id=i, vector=vec, payload={"text": chunk})
        for i, (chunk, vec) in enumerate(zip(chunks, vectors))
    ]

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)


def retrieve_relevant_chunks(query: str, top_k: int = 3) -> list[dict]:
    query_vector = get_embedding(query)

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    ).points

    return [
        {"text": hit.payload["text"], "score": hit.score}
        for hit in results
    ]


TOKEN_THRESHOLD = 200


def keyword_search(skill: str) -> list[str]:
    all_chunks = qdrant.scroll(
        collection_name=COLLECTION_NAME,
        limit=100,
        with_payload=True,
    )[0]
    return [p.payload["text"] for p in all_chunks if skill.lower() in p.payload["text"].lower()]


def precompute_skill_embeddings(skills: list[str]):
    """Pre-embed all skills in a single batch call before the per-skill loop."""
    batch_embed(skills)


def get_cv_context(cv_text: str, skill: str, chunks_stored: bool) -> str:
    if len(cv_text.split()) < TOKEN_THRESHOLD:
        return cv_text  # short CV, just use the whole thing

    keyword_matches = keyword_search(skill)
    semantic_chunks = [c["text"] for c in retrieve_relevant_chunks(query=skill, top_k=3)]

    # merge, keeping keyword matches first, deduplicating by content
    seen = set()
    merged = []
    for chunk in keyword_matches + semantic_chunks:
        if chunk not in seen:
            seen.add(chunk)
            merged.append(chunk)

    return "\n".join(merged)
