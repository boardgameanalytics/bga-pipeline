/* Add foreign key constraints to game_description and relationship tables */

ALTER TABLE game_description
    ADD CONSTRAINT fk_game_id
        FOREIGN KEY(game_id) 
        REFERENCES game(id);

ALTER TABLE game_mechanic
    ADD CONSTRAINT fk_game_id
        FOREIGN KEY(game_id) 
        REFERENCES game(id),
    ADD CONSTRAINT fk_mech_id
        FOREIGN KEY(mechanic_id) 
        REFERENCES mechanic(id);

ALTER TABLE game_category
    ADD CONSTRAINT fk_game_id
        FOREIGN KEY(game_id) 
        REFERENCES game(id),
    ADD CONSTRAINT fk_cat_id
        FOREIGN KEY(category_id) 
        REFERENCES category(id);

ALTER TABLE game_designer
    ADD CONSTRAINT fk_game_id
        FOREIGN KEY(game_id) 
        REFERENCES game(id),
    ADD CONSTRAINT fk_cat_id
        FOREIGN KEY(designer_id) 
        REFERENCES designer(id);

ALTER TABLE game_artist
    ADD CONSTRAINT fk_game_id
        FOREIGN KEY(game_id) 
        REFERENCES game(id),
    ADD CONSTRAINT fk_cat_id
        FOREIGN KEY(artist_id) 
        REFERENCES artist(id);

ALTER TABLE game_publisher
    ADD CONSTRAINT fk_game_id
        FOREIGN KEY(game_id) 
        REFERENCES game(id),
    ADD CONSTRAINT fk_cat_id
        FOREIGN KEY(publisher_id) 
        REFERENCES publisher(id);