DROP TABLE IF EXISTS statustable;

CREATE TABLE statustable
(
	id serial PRIMARY KEY,
	currently_being_modified boolean NOT NULL,
	last_id_recieved integer NOT NULL
);

INSERT INTO statustable (currently_being_modified,last_id_recieved)  VALUES (FALSE, 1);

DROP TABLE IF EXISTS teams CASCADE;
CREATE TABLE teams
(
	id serial PRIMARY KEY,
	team_number integer NOT NULL UNIQUE

);


DROP TABLE IF EXISTS events CASCADE;
CREATE TABLE events
(
	id serial PRIMARY KEY,
	year integer NOT NULL,
	name text NOT NULL,
	UNIQUE (year,name)
);

DROP TABLE IF EXISTS event_team_relationships;
CREATE TABLE event_team_relationships
(
	id serial PRIMARY KEY,
	event_id integer REFERENCES events (id),
	team_id integer REFERENCES teams (id),
	UNIQUE(event_id,team_id)
);