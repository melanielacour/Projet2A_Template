classDiagram
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
        +url: string
        +add_film(Film): None
        +supp_film(Film): None
        +search_commented_film(id_film): Film
    }

    class FilmService {
        +search_film(str): Film
        +add_grade(): None
        +add_comment(): None
    }

    class UserDAO {
        +add_user(id_user): None
        +delete_user(id_user): None
        +search_user(id_user): User
        +update_user(id_user): None
    }

    class UserService {
        +log_in(id_user): None
        +get_scouts(user_id): List[Scout]
        +get_seen_films(user_id): List[Film]
        +get_to_watch_films(user_id): List[Film]
    }

    class Recommandation {
        +id_film: int
        +get_recommandation(id_film): List[Film]
    }

    class UserClient {
        +log_in(): None
        +add_client(id_user): None
        +delete_client(id_user): None
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
