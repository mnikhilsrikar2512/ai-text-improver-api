from pydantic import BaseModel


class ImproveRequest(BaseModel):

    text: str
    force_llm: bool = False

class ImproveResponse(BaseModel):
    original: str
    suggestions: list[str]
    cached: bool
    latency_ms: int