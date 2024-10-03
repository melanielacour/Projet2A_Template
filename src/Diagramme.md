# Class diagramm

```mermaid
---
title: Class diagramm of PopcornCritic python_app
---
classDiagram
    class Film {
        +id_film: int
        +id_tmdb: int
        +title: string
        +producer: string
        +category: string
        +date: string
        +average_rate: float
        +ratings: List[int]
        +calculation_mean(): float
        +add_rating(rating: int): None
    }

    class List_movie {
        +films: List[Film]
        +add_film(Film): None
        +remove_film(Film): None
        +get_all_films(): List[Film]
    }

    class User {
        +id_user: int
        +pseudo: string
        +password: string
        +seen: List[Film]
        +to_watch: List[Film]
        +scouts_list: List[Scout]
        +add_seen_film(Film): None
        +add_to_see_film(Film): None
        +add_scout(Scout): None
    }

    class Scout {
        +id_scout: int
        +pseudo_scout: string
        +film_list: List[Film]
        +rates_comments: Dict(Film, [int, string])
        +add_recommended_films(Film): None
        +delete_recommended_films(Film): None
        +get_followers(): List[User]
    }

    class Film {
        +id_film: int
        +id_tmdb: int
        +title: str
        +producer: str
        +category: str
        +date: Date
        +average_rate: float
        +calculation_mean(): float
    }

    class FilmDAO {
        +get_local_film(film_id: int): Film
        +add_local_film(Film): None
    }

    class FilmService {
        +search_film(query: string): Film
        +add_grade(Film, Grade): None
        +add_comment(Film, Comment): None
    }

    class UserDAO {
        +get_user(user_id: int): User
        +add_user(User): None
        +delete_user(user_id: int): None
        +get_followers_of_scout(scout_id: int): List[User]
    }

    class UserService {
        +log_in(id_user): None
        +get_scouts(user_id): List[Scout]
        +get_seen_films(user_id): List[Film]
        +get_to_watch_films(user_id): List[Film]
    }

    class Recommandation {
        +get_recommendation(film_id: int): List[Film]
    }

    class TMDBFilmController {
        +details_film(id_film): None
        +search_tmdb(query): List[Film]
        +get_film_details(id_film): Film
    }

User *-- UserService
Scout "1" o-- "*" Film
UserService "1" o-- "*" Film
User o-- Scout
Film *-- FilmService
Film *-- FilmDAO
Film *-- TMDBFilmController
User *-- UserDAO
FilmDAO --> TMDBFilmController
FilmService --> FilmDAO
Recommandation o-- Film
---
```
