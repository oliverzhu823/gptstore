from components.store import get_storage_context
from llama_index import VectorStoreIndex
from llama_index.retrievers import (
    VectorIndexRetriever,
)
from models.gpts import get_gpts_by_uuids


def search_gpts(question):
    storage_context = get_storage_context()
    index = VectorStoreIndex.from_documents([], storage_context=storage_context)

    retriever = VectorIndexRetriever(index=index, similarity_top_k=10)

    nodes = retriever.retrieve(question)

    uuids = []
    uuids_with_scores = {}
    gpts = []
    for node in nodes:
        print("node metadata", node.metadata)
        if node.score > 0.80:
            uuid = node.metadata['uuid']
            uuids.append(uuid)
            uuids_with_scores[uuid] = node.score

    if len(uuids) == 0:
        return gpts

    rows = get_gpts_by_uuids(uuids)
    for row in rows:
        gpts.append({
            "uuid": row.uuid,
            "name": row.name,
            "description": row.description,
            "avatar_url": row.avatar_url,
            "author_name": row.author_name,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
            "visit_url": "https://chat.openai.com/g/" + row.short_url,
            "score": uuids_with_scores[row.uuid],
        })

    sorted_gpts = sorted(gpts, key=lambda x: x['score'], reverse=True)
    return sorted_gpts
    

