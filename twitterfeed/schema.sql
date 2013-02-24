DROP TABLE IF EXISTS statustable;

CREATE TABLE statustable
(
	id serial PRIMARY KEY,
	currently_being_modified boolean NOT NULL,
	last_id_recieved integer NOT NULL
);

INSERT INTO statustable (currently_being_modified,last_id_recieved)  VALUES (FALSE, 0);