from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from typing import Optional,List
from pydantic import BaseModel
from redis_storage import redis_storage
from contentbasedrecommendation import content_based_recommendation

app=FastAPI()



@app.post("/store-resume-embedding")
def create(user_id:str,parsed_resume:dict):
    ob=redis_storage()
    ob.concat_resume(parsed_resume)
    ob.embedding_generator()
    ob.store_embedding(user_id)
    return {"message":"resume embeddings stored successfully in redis"}




@app.websocket("/ws/get-job-recommendations-for-user")
async def websocket_fetch(websocket:WebSocket,user_id:str):
    await websocket.accept()


    try:
        while  True:
            job_descriptions=await websocket.receive_json()
            ob=content_based_recommendation(len(job_descriptions))
            ob.concatenate_job_fields(job_descriptions)
            ob.recommendation(user_id)
            await websocket.send_json(ob.job_recommendations)

    except WebSocketDisconnect:
        print("Client disconnected")

