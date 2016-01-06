---
--- Create schema
---
CREATE SCHEMA IF NOT EXISTS opportunity_tracker AUTHORIZATION postgres;
GRANT ALL ON SCHEMA opportunity_tracker TO postgres;

SET SCHEMA 'opportunity_tracker';

---
--- Create location table
---
CREATE TABLE location (
  id SERIAL PRIMARY KEY,
  address1 VARCHAR(80) NOT NULL,
  address2 VARCHAR(80),
  city VARCHAR(30) NOT NULL,
  state VARCHAR(2) NOT NULL,
  company_id INTEGER NOT NULL    -- Foreign key
);

---
--- Create company table
---
CREATE TABLE company (
  id SERIAL PRIMARY KEY,
  name VARCHAR(25) NOT NULL,
  industry VARCHAR(80),
  active BOOLEAN NOT NULL,
  employee_id INTEGER NOT NULL  -- Foreign key
);

---
--- Create employee table
---
CREATE TABLE employee (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(25),
  last_name VARCHAR(25),
  email VARCHAR(80),
  username VARCHAR(25) UNIQUE,
  pwhash TEXT
);

---
--- Create action table
---
CREATE TABLE action (
  id SERIAL PRIMARY KEY,
  company_id INTEGER,     -- Foreign key
  contact_id INTEGER,     -- Foreign key
  emplyee_id INTEGER,     -- Foreign key
  action_date TIMESTAMP WITH TIME ZONE,
  note VARCHAR(255)
);

---
--- Create industry table
---
CREATE TABLE industry (
  id SERIAL PRIMARY KEY,
  name VARCHAR(80)
);
