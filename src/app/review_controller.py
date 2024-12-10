from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.app.dependencies import get_current_user
from src.app.init_app import review_dao, review_service


review_router = APIRouter(prefix="/reviews", tags=["Reviews"])


class ReviewRequest(BaseModel):
    note: Optional[int] = None
    comment: Optional[str] = None


@review_router.post("/id_local/{id_local}")
async def post_review_by_id_local(
    id_local: int, review: ReviewRequest,
    id_user: int = Depends(get_current_user)
):
    try:
        return review_service.search_and_rate_movie_existing_movie(
            id_film=id_local, id_user=id_user, note=review.note,
            comment=review.comment
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@review_router.post("/id_tmdb/{id_tmdb}")
async def post_review_by_id_tmdb(
    id_tmdb: int,
    title: str,
    review: ReviewRequest,
    id_user: int = Depends(get_current_user),
):
    try:
        return review_service.search_and_rate_movie_by_idtmdb(
            id_tmdb=id_tmdb,
            title=title,
            id_user=id_user,
            note=review.note,
            comment=review.comment,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@review_router.put("/update_note")
async def update_note(
    id_film: int, note: int, id_user: int = Depends(get_current_user)
):
    try:
        return review_service.update_note(
            id_user=id_user, id_film=id_film, note=note
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@review_router.put("/update_comment")
async def update_comment(
    id_film: int, comment: str, id_user: int = Depends(get_current_user)
):
    try:
        return review_service.update_comment(
            id_user=id_user, id_film=id_film, comment=comment
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@review_router.delete("/delete_note")
async def delete_note(id_film: int, id_user: int = Depends(get_current_user)):
    try:
        return review_service.delete_note(id_film=id_film, id_user=id_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@review_router.delete("/delete_comment")
async def delete_comment(
    id_film: int, id_user: int = Depends(get_current_user)
):
    try:
        return review_service.delete_comment(id_film=id_film, id_user=id_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@review_router.get("/average_rating/{id_film}")
async def get_average_rating(id_film: int):
    return {"average_rating": review_service.get_average_rating(id_film)}


@review_router.get("/reviews_by_id_film/{id_film}")
async def get_reviews_by_film_id(
    id_film: int, id_user2: int = Depends(get_current_user)
):
    print(
        f"Recherche des critiques pour le film avec id_film={id_film}, ",
        f"utilisateur authentifié={id_user2}"
    )
    reviews = review_service.get_reviews_by_film_id(id_film)
    print(f"Résultats trouvés : {reviews}")
    return reviews


@review_router.get("/reviews_by_id_user/{id_user}")
async def get_reviews_by_user_id(
    id_user: int, id_user2: int = Depends(get_current_user)
):
    print(
        f"Recherche des critiques pour l'utilisateur avec id_user={id_user}, ",
        f"utilisateur authentifié={id_user2}"
    )
    reviews = review_dao.get_all_reviews_by_user_id(id_user)
    print(f"Résultats trouvés : {reviews}")
    return reviews
