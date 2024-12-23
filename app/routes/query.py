# from fastapi import APIRouter, HTTPException
# from app.services.query_service import process_query

# router = APIRouter()

# @router.post("/")
# async def handle_query(query: str):
#     try:
#         response = process_query(query)
#         return {"response": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
