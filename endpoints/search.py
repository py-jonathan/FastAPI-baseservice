from fastapi import APIRouter, Query, HTTPException
from elasticsearch import AsyncElasticsearch
from config import app_config

router = APIRouter()
es = AsyncElasticsearch(hosts=[app_config["ELASTICSEARCH"]["host"]])

@router.get("/search")
async def search_messages(query: str = Query(..., description="Search query")):
    try:
        response = await es.search(index="chat_history", body={
            "query": {
                "fuzzy": {
                    "message": {
                        "value": query
                    }
                }
            }
        })
        return response["hits"]["hits"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add the router to your main FastAPI app
# In app.py
from endpoints import search

app.include_router(search.router, prefix="/search", tags=["Search"])
