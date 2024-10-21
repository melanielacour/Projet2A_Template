import requests
from fastapi import FastAPI

app = FastAPI()
TMDB_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YTM1YmQwMDE2Mzk5MDNmNWM4MzBlODhkZDg2ZWQzMCIsIm5iZiI6MTcyNjgxOTk4Mi42NzA1NDQsInN1YiI6IjY2ZTQ0NmI5OTAxM2ZlODcyMjI0MTc1MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mUjUWmMcf2k7lyf4V7sJTn3X8eDGgYSpYDrhKippftg"

@app.get("/movies")
async def get_movies():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=fr-FR&page=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["results"]
    else:
        return {"error": "Erreur lors de la récupération des films"}
