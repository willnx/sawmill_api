CREATE SCHEMA api;

CREATE TABLE api.settings(
    section TEXT NOT NULL,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    PRIMARY KEY (section, name)
);
