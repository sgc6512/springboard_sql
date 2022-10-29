-- from the terminal run:
-- psql < outer_space.sql

DROP DATABASE IF EXISTS outer_space;

CREATE DATABASE outer_space;

\c outer_space

CREATE TABLE planet
(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  orbital_period_in_years FLOAT NOT NULL,
  orbits_around int REFERENCES star
);

CREATE TABLE galaxy (
  id SERIAL PRIMARY KEY,
  name varchar NOT NULL,
  stars int REFERENCES star
);

CREATE TABLE moon (
  id SERIAL PRIMARY KEY,
  name varchar NOT NULL,
  orbital_period_in_years float NOT NULL,
  orbits_around int REFERENCES planet
);

CREATE TABLE star (
  id SERIAL PRIMARY KEY,
  name varchar NOT NULL,
  galaxy_id int REFERENCES galaxy
);
