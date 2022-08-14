-- Load tables from csv files
COPY artist FROM 'data/csv/artist.csv' DELIMITER ',' CSV;
COPY category FROM 'data/csv/category.csv' DELIMITER ',' CSV;
COPY designer FROM 'data/csv/designer.csv' DELIMITER ',' CSV;
COPY mechanic FROM 'data/csv/mechanic.csv' DELIMITER ',' CSV;
COPY publisher FROM 'data/csv/publisher.csv' DELIMITER ',' CSV;
COPY game FROM 'data/csv/game.csv' DELIMITER ',' CSV;
COPY game_description FROM 'data/csv/game_description.csv' DELIMITER ',' CSV;
COPY game_designer FROM 'data/csv/game_designer.csv' DELIMITER ',' CSV;
COPY game_artist FROM 'data/csv/game_artist.csv' DELIMITER ',' CSV;
COPY game_category FROM 'data/csv/game_category.csv' DELIMITER ',' CSV;
COPY game_mechanic FROM 'data/csv/game_mechanic.csv' DELIMITER ',' CSV;
COPY game_publisher FROM 'data/csv/game_publisher.csv' DELIMITER ',' CSV;