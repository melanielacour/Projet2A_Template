# Diagramme de classes des objets métiers

```mermaid
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
        +seen: List_movie
        +to_watch: List_movie
        +scouts_list: Liste_user
        +add_seen_film(Film): None
        +add_to_see_film(Film): None
        +add_scout(Scout): None
    }

    class Scout {
        +id_scout: int
        +pseudo_scout: string
        +password: string
        +recommended_films: List_movie
        +add_recommended_film(Film): None
    }

    class Liste_user {
        +users: List[User]
        +add_user(User): None
        +remove_user(User): None
        +get_all_users(): List[User]
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
        +log_in(user_id: int): None
        +become_scout(user_id: int): None
        +get_scouts(user_id: int): List[Scout]
        +get_seen_films(user_id: int): List[Film]
        +get_to_watch_films(user_id: int): List[Film]
    }

    class Recommandation {
        +get_recommendation(film_id: int): List[Film]
    }

    class FilmController {
        +get_film_details_from_tmdb(film_id: int): None
        +search_films_in_tmdb(query: string): None
    }

    User <|-- Scout
    User o-- List_movie
    User o-- Liste_user
    List_movie o-- Film
    FilmService o-- Film
    FilmDAO o-- Film
    UserService o-- User
    UserDAO o-- User
    Recommandation o-- Film
    FilmController o-- FilmService

```
