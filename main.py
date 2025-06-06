from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict
import word_split
from docx import Document
import io
import datetime

class SplitRequest(BaseModel):
    url: str
    chunk_size: int = 500
    overlap: int = 50
    mode: str = "paragraph"

class DocxRequest(BaseModel):
    text_content: str

app = FastAPI(
    title="Word Split Service",
    description="API 服务，用于从 URL 加载 Word 文档并按照指定模式切分，并支持生成 DOCX 文件。",
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

@app.post("/generate_docx")
async def generate_docx(req: DocxRequest):
    """
    接收文本内容，生成并返回 .docx 文件。
    """
    if not req.text_content:
        raise HTTPException(status_code=400, detail="text_content 不能为空")

    try:
        document = Document()
        document.add_paragraph(req.text_content)
        
        file_stream = io.BytesIO()
        document.save(file_stream)
        file_stream.seek(0)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"填充后文件_{timestamp}.docx"
        
        headers = {
            "Content-Disposition": f"attachment; filename=\"{filename}\"",
            "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }
        
        return StreamingResponse(file_stream, headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件生成失败: {str(e)}")

# 如果直接运行该模块，可启动 Uvicorn 服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
