from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from recommend_alternatives_fixed import RecommenderFixed

app = FastAPI(title="Ecowrap API")

reco = RecommenderFixed()

class RecommendRequest(BaseModel):
    product_name: str | None = None
    code: str | None = None
    top_k: int = 5


@app.post("/recommend")
def recommend(req: RecommendRequest):
    result = reco.recommend(
        name=req.product_name,
        code=req.code,
        top_k=req.top_k
    )

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return {"brand": "Ecowrap", "result": result}


@app.get("/health")
def health():
    return {"status": "ok"}
