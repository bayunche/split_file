from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import word_split

class SplitRequest(BaseModel):
    url: str
    chunk_size: int = 500
    overlap: int = 50
    mode: str = "paragraph"

app = FastAPI(
    title="Word Split Service",
    description="API 服务，用于从 URL 加载 Word 文档并按照指定模式切分。",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok"}

@app.post("/split", response_model=List[Dict])
async def split(req: SplitRequest):
    """
    接收 split 请求，返回切分结果
    """
    try:
        result = word_split.split_word_from_url(req.url, req.chunk_size, req.overlap, req.mode)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 如果直接运行该模块，可启动 Uvicorn 服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
