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
  company_id INTEGER NOT NULL    -- Foreign key set later
);