from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.pipeline import pipeline,GraphState

router=APIRouter()
class Chatrequest(BaseModel):
    query:str

class ChatResponse(BaseModel):
    answer:str

@router.post('/chat',response_model=ChatResponse)
def chat_endpoint(payload:Chatrequest):
    max_hit=6
    hit=0
    last_value=None
    app=pipeline(GraphState)
    inputs={"question":payload.query}
    for output in app.stream(inputs):
        hit+=1
        for key, value in output.items():
            print(f"Finished running: {key}:")
            last_value=value

        if hit >= max_hit:
            return {
                "answer": "I couldn’t find enough information to answer this properly. Try being more specific or include relevant details."
                        
            }
    answer=last_value["generation"]
    return {"answer":answer}