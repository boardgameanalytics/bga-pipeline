/* Create boardgames table structure

This script is intended for use on a staging database, and will drop all
existing tables and recreate from scratch.

FK constraints are also disabled for loading purposes, and should be added after
loading with the enable_fk_constraints.sql script.
*/

DROP TABLE IF EXISTS
    game_artist,
    game_category,
    game_designer,
    game_mechanic,
    game_publisher,
    game_description,
    game,
    artist,
    designer,
    publisher,
    category,
    mechanic;

CREATE TABLE game (
    id              int PRIMARY KEY,
    title           text NOT NULL,
    release_year    int,
    avg_rating      real,
    bayes_rating    real,
    total_ratings   int NOT NULL,
    std_ratings     real,
    min_players     int,
    max_players     int,
    min_playtime    int,
    max_playtime    int,
    min_age         int,
    weight          real,
    owned_copies    int,
    wishlist        int,
    kickstarter     bool,
    popularity      real GENERATED ALWAYS AS (LN(ABS((bayes_rating - 5.5) * total_ratings) + 1) * SIGN((bayes_rating - 5.5))) STORED
);

CREATE TABLE mechanic (
    id     int PRIMARY KEY,
    name   text NOT NULL
);

CREATE TABLE category (
    id      int PRIMARY KEY,
    name    text NOT NULL
);

CREATE TABLE artist (
    id     int PRIMARY KEY,
    name   text NOT NULL
);

CREATE TABLE publisher (
    id      int PRIMARY KEY,
    name    text NOT NULL
);

CREATE TABLE designer (
    id     int PRIMARY KEY,
    name   text NOT NULL
);

CREATE TABLE game_description (
    game_id         int PRIMARY KEY,
    description     text NOT NULL
    -- CONSTRAINT fk_game_id
    --     FOREIGN KEY(game_id) 
    --     REFERENCES game(id)
);

CREATE TABLE game_mechanic (
    game_id      int,
    mechanic_id  int,
    PRIMARY KEY (game_id, mechanic_id)
    -- CONSTRAINT fk_game_id
    --     FOREIGN KEY(game_id) 
    --     REFERENCES game(id),
    -- CONSTRAINT fk_mech_id
    --     FOREIGN KEY(mechanic_id) 
    --     REFERENCES mechanic(id)
);

CREATE TABLE game_category (
    game_id     int,
    category_id int,
    PRIMARY KEY (game_id, category_id)
    -- CONSTRAINT fk_game_id
    --     FOREIGN KEY(game_id) 
    --     REFERENCES game(id),
    -- CONSTRAINT fk_cat_id
    --     FOREIGN KEY(category_id) 
    --     REFERENCES category(id)
);

CREATE TABLE game_designer (
    game_id     int,
    designer_id int,
    PRIMARY KEY (game_id, designer_id)
    -- CONSTRAINT fk_game_id
    --     FOREIGN KEY(game_id) 
    --     REFERENCES game(id),
    -- CONSTRAINT fk_cat_id
    --     FOREIGN KEY(designer_id) 
    --     REFERENCES designer(id)
);

CREATE TABLE game_artist (
    game_id     int,
    artist_id   int,
    PRIMARY KEY (game_id, artist_id)
    -- CONSTRAINT fk_game_id
    --     FOREIGN KEY(game_id) 
    --     REFERENCES game(id),
    -- CONSTRAINT fk_cat_id
    --     FOREIGN KEY(artist_id) 
    --     REFERENCES artist(id)
);

CREATE TABLE game_publisher (
    game_id     int,
    publisher_id   int,
    PRIMARY KEY (game_id, publisher_id)
    -- CONSTRAINT fk_game_id
    --     FOREIGN KEY(game_id) 
    --     REFERENCES game(id),
    -- CONSTRAINT fk_cat_id
    --     FOREIGN KEY(publisher_id) 
    --     REFERENCES publisher(id)
);