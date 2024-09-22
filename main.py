from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from scraper import Scraper

app = FastAPI()

class ScrapeRequest(BaseModel):
    limit: int = Field(default=5, gt=0)  # Ensure limit is greater than 0
    proxy: str = Field(default=None)      # Make proxy optional

def authenticate(token: str):
    if token != "ankur_token":  # Replace with your actual token
        raise HTTPException(status_code=403, detail="Not authorized")

@app.post("/scrape/")
async def scrape(request: ScrapeRequest, token: str = Depends(authenticate)):
    scraper = Scraper()
    result = await scraper.scrape_products(request.limit, request.proxy)
    return {"message": f"Scraped {result} products."}

# Function to test the scraping directly
async def test_scraping():
    request = ScrapeRequest(limit=5)  # proxy can be omitted as it's optional
    token = "ankur_token"

    # Simulate calling the scrape function
    response = await scrape(request, token=token)
    print(response)

# Run the test function
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_scraping())
