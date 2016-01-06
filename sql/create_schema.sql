---
--- Create schema
---
CREATE SCHEMA IF NOT EXISTS opportunity_tracker AUTHORIZATION postgres;
GRANT ALL ON SCHEMA opportunity_tracker TO postgres;

SET SCHEMA 'opportunity_tracker';

---
--- Create employee table
---
CREATE TABLE employee (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(25),
  last_name VARCHAR(25),
  email VARCHAR(255),
  username VARCHAR(25) UNIQUE,
  pwhash TEXT
);

---
--- Create industry table
---
CREATE TABLE industry (
  id SERIAL PRIMARY KEY,
  name VARCHAR(80) UNIQUE
);

---
--- Create company table
---
CREATE TABLE company (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  active BOOLEAN NOT NULL,
  industry INTEGER REFERENCES industry (id),
  employee INTEGER REFERENCES employee (id)
);

---
--- Create location table
---
CREATE TABLE location (
  id SERIAL PRIMARY KEY,
  address1 VARCHAR(80) NOT NULL,
  address2 VARCHAR(80),
  city VARCHAR(30) NOT NULL,
  state VARCHAR(2) NOT NULL,
  company INTEGER NOT NULL REFERENCES company (id)
);

---
--- Create contact table
---
CREATE TABLE contact (
  id SERIAL PRIMARY KEY,
  company INTEGER NOT NULL REFERENCES company (id),
  location INTEGER NOT NULL REFERENCES location (id),
  first_name VARCHAR(25) NOT NULL,
  last_name VARCHAR(25),
  email VARCHAR(255),
  phone VARCHAR(15)
);

---
--- Create action table
---
CREATE TABLE action (
  id SERIAL PRIMARY KEY,
  company INTEGER,     -- Foreign key
  contact INTEGER,     -- Foreign key
  emplyee INTEGER,     -- Foreign key
  action_date TIMESTAMP WITH TIME ZONE,
  note VARCHAR(255)
);
