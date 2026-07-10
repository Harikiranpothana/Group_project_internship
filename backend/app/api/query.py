from fastapi import APIRouter, HTTPException

from app.models.request_models import QueryRequest
from app.models.response_models import QueryResponse
from app.services.query_pipeline import query_pipeline

router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse
)
def process_query(request: QueryRequest):

    try:

        return query_pipeline.process_query(
            request.question
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )