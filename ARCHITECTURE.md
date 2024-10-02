---
title: Architecture of python app with classes
---
graph LR
    USR((User)):::entity
    DB[("fa:fa-database App Database \n (PostgreSQL) \n : FilmDB, UserDB")]:::database
    API(fa:fa-python API / \n WebService):::controller
    DAO(fa:fa-python DAO):::dao
    SVC(fa:fa-python Service / \n Controllers):::service
    MDB[(fa:fa-database TheMovieDB)]:::database
    MDBAPI(TMDB API):::external

    USR<--->API
    subgraph PopcornCritic_python_app
        API<-->SVC<-->DAO
    end
    DAO<--->DB
    MDBAPI <--> MDB
    SVC <--> MDBAPI

    %% Insertion of the corresponding classes
    classDef entity fill:#f9f,stroke:#333,stroke-width:2px;
    classDef database fill:#bbf,stroke:#333,stroke-width:2px;
    classDef controller fill:#ffb,stroke:#333,stroke-width:2px;
    classDef dao fill:#ccf,stroke:#333,stroke-width:2px;
    classDef service fill:#cfc,stroke:#333,stroke-width:2px;
    classDef external fill:#f96,stroke:#333,stroke-width:2px;

    %% User, Scout, List_movie, Liste_user (Entities)
    USR-.->|Entities|User((User))
    User-.->Scout((Scout))

    %% FilmService, UserService, Recommandation (Services)
    SVC-.->FilmService((FilmService))
    SVC-.->UserService((UserService))
    SVC-.->Recommandation((Recommandation))

    %% FilmDAO, UserDAO (DAOs)
    DAO-.->FilmDAO((FilmDAO))
    DAO-.->UserDAO((UserDAO))

    %% FilmController (API)
    API-.->FilmController((FilmController))

    %% Film (Data entity)
    List_movie-.->Film((Film))
    Recommandation-.->Film
    FilmService-.->Film

