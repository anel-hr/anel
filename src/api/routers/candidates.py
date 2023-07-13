from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def get_candidates():
    pass


@router.post("/")
async def create_candidate():
    pass


@router.get("/{candidate_id}")
async def get_candidate(candidate_id: int):
    pass


@router.put("/{candidate_id}")
async def update_candidate(candidate_id: int):
    pass


@router.delete("/{candidate_id}")
async def delete_candidate(candidate_id: int):
    pass
