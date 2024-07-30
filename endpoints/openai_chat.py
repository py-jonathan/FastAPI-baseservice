from elasticsearch import AsyncElasticsearch
from config import app_config

es = AsyncElasticsearch(hosts=[app_config["ELASTICSEARCH"]["host"]])

async def search_messages(query: str):
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
        raise Exception(f"Elasticsearch error: {str(e)}")
