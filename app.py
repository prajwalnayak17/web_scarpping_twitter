from config import (
    app,
    TwitterCredentials,
    List,
    HTTPException,
    BaseModel,
    db_service
)
from twitter_scrapper import TwitterScraper


class TrendingTopicsResponse(BaseModel):
    topics: List[str]


@app.post("/trending-topics", response_model=TrendingTopicsResponse)
async def get_trending_topics(credentials: TwitterCredentials):
    try:
        print("REACHED API")
        scraper = TwitterScraper(
            username=credentials.username,
            password=credentials.password,
            headless=True
        )

        try:
            if scraper.login():
                print("logged in successfully!")
                trending_topics = scraper.get_trending_topics()
                if trending_topics:
                    # Store topics in MongoDB
                    stored_document = db_service.store_trending_topics(trending_topics[:5])
                    print(stored_document)
                    return {"topics": trending_topics}
                raise HTTPException(status_code=404, detail="No trending topics found")
            raise HTTPException(status_code=401, detail="Login failed")

        finally:
            scraper.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Add this when shutting down your application
@app.on_event("shutdown")
async def shutdown_event():
    db_service.close()
