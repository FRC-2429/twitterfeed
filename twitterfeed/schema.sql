DROP TABLE IF EXISTS statustable;

CREATE TABLE statustable
(
	id serial PRIMARY KEY,
	currently_being_modified boolean NOT NULL,
	last_id_recieved integer NOT NULL
);

INSERT INTO statustable (currently_being_modified,last_id_recieved)  VALUES (FALSE, 0);

DROP TABLE IF EXISTS teams;
CREATE TABLE teams
(
	id serial PRIMARY KEY,
	team_number integer PRIMARY KEY

);


DROP TABLE IF EXISTS events;
CREATE TABLE events
(
	id serial PRIMARY KEY,
	year integer NOT NULL,
	name text NOT NULL
);

DROP TABLE IF EXISTS event_team_relationships;
CREATE TABLE event_team_relationships
(
	id serial PRIMARY KEY,
	event_id integer REFERENCES events (id),
	team_id integer REFERENCES teams (id)
);