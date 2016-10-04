--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.2
-- Dumped by pg_dump version 9.5.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: opportunity_tracker; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA opportunity_tracker;


ALTER SCHEMA opportunity_tracker OWNER TO postgres;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA opportunity_tracker;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET search_path = opportunity_tracker, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: company; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE company (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    active boolean NOT NULL,
    employee integer,
    creator integer NOT NULL
);


ALTER TABLE company OWNER TO postgres;

--
-- Name: company_id_seq; Type: SEQUENCE; Schema: opportunity_tracker; Owner: postgres
--

CREATE SEQUENCE company_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE company_id_seq OWNER TO postgres;

--
-- Name: company_id_seq; Type: SEQUENCE OWNED BY; Schema: opportunity_tracker; Owner: postgres
--

ALTER SEQUENCE company_id_seq OWNED BY company.id;


--
-- Name: contact; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE contact (
    id integer NOT NULL,
    company integer NOT NULL,
    first_name character varying(25) NOT NULL,
    last_name character varying(25),
    title character varying(50),
    email character varying(255),
    phone character varying(30),
    ext text DEFAULT ''::text NOT NULL
);


ALTER TABLE contact OWNER TO postgres;

--
-- Name: contact_id_seq; Type: SEQUENCE; Schema: opportunity_tracker; Owner: postgres
--

CREATE SEQUENCE contact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE contact_id_seq OWNER TO postgres;

--
-- Name: contact_id_seq; Type: SEQUENCE OWNED BY; Schema: opportunity_tracker; Owner: postgres
--

ALTER SEQUENCE contact_id_seq OWNED BY contact.id;


--
-- Name: cost_type; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE cost_type (
    cost_type text NOT NULL
);


ALTER TABLE cost_type OWNER TO postgres;

--
-- Name: employee; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE employee (
    id integer NOT NULL,
    first_name character varying(25),
    last_name character varying(25),
    email character varying(255),
    username character varying(25),
    pwhash text
);


ALTER TABLE employee OWNER TO postgres;

--
-- Name: employee_id_seq; Type: SEQUENCE; Schema: opportunity_tracker; Owner: postgres
--

CREATE SEQUENCE employee_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE employee_id_seq OWNER TO postgres;

--
-- Name: employee_id_seq; Type: SEQUENCE OWNED BY; Schema: opportunity_tracker; Owner: postgres
--

ALTER SEQUENCE employee_id_seq OWNED BY employee.id;


--
-- Name: industry; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE industry (
    id integer NOT NULL,
    name character varying(80)
);


ALTER TABLE industry OWNER TO postgres;

--
-- Name: industry_id_seq; Type: SEQUENCE; Schema: opportunity_tracker; Owner: postgres
--

CREATE SEQUENCE industry_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE industry_id_seq OWNER TO postgres;

--
-- Name: industry_id_seq; Type: SEQUENCE OWNED BY; Schema: opportunity_tracker; Owner: postgres
--

ALTER SEQUENCE industry_id_seq OWNED BY industry.id;


--
-- Name: location; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE location (
    id integer NOT NULL,
    address1 character varying(80) NOT NULL,
    address2 character varying(80),
    city character varying(30) NOT NULL,
    state character varying(2) NOT NULL,
    company integer NOT NULL,
    postal_code character varying(10) NOT NULL,
    country character varying(2) NOT NULL
);


ALTER TABLE location OWNER TO postgres;

--
-- Name: location_id_seq; Type: SEQUENCE; Schema: opportunity_tracker; Owner: postgres
--

CREATE SEQUENCE location_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE location_id_seq OWNER TO postgres;

--
-- Name: location_id_seq; Type: SEQUENCE OWNED BY; Schema: opportunity_tracker; Owner: postgres
--

ALTER SEQUENCE location_id_seq OWNED BY location.id;


--
-- Name: notes; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE notes (
    id integer NOT NULL,
    note_type character varying(255) NOT NULL,
    contact integer,
    note_date date NOT NULL,
    company integer NOT NULL,
    note character varying(250) NOT NULL
);


ALTER TABLE notes OWNER TO postgres;

--
-- Name: notes_id_seq; Type: SEQUENCE; Schema: opportunity_tracker; Owner: postgres
--

CREATE SEQUENCE notes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notes_id_seq OWNER TO postgres;

--
-- Name: notes_id_seq; Type: SEQUENCE OWNED BY; Schema: opportunity_tracker; Owner: postgres
--

ALTER SEQUENCE notes_id_seq OWNED BY notes.id;


--
-- Name: notification; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE notification (
    id integer NOT NULL,
    employee integer NOT NULL,
    company integer NOT NULL,
    notify_date date NOT NULL,
    note character varying(255) NOT NULL,
    sent boolean DEFAULT false NOT NULL
);


ALTER TABLE notification OWNER TO postgres;

--
-- Name: notification_id_seq; Type: SEQUENCE; Schema: opportunity_tracker; Owner: postgres
--

CREATE SEQUENCE notification_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notification_id_seq OWNER TO postgres;

--
-- Name: notification_id_seq; Type: SEQUENCE OWNED BY; Schema: opportunity_tracker; Owner: postgres
--

ALTER SEQUENCE notification_id_seq OWNED BY notification.id;


--
-- Name: part; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE part (
    id integer NOT NULL,
    part_number text NOT NULL,
    description text,
    uom text NOT NULL,
    part_type text NOT NULL,
    cost numeric(15,3)
);


ALTER TABLE part OWNER TO postgres;

--
-- Name: COLUMN part.uom; Type: COMMENT; Schema: opportunity_tracker; Owner: postgres
--

COMMENT ON COLUMN part.uom IS 'unit of measure';


--
-- Name: part_id_seq; Type: SEQUENCE; Schema: opportunity_tracker; Owner: postgres
--

CREATE SEQUENCE part_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE part_id_seq OWNER TO postgres;

--
-- Name: part_id_seq; Type: SEQUENCE OWNED BY; Schema: opportunity_tracker; Owner: postgres
--

ALTER SEQUENCE part_id_seq OWNED BY part.id;


--
-- Name: part_type; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE part_type (
    part_type text NOT NULL
);


ALTER TABLE part_type OWNER TO postgres;

--
-- Name: permissions; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE permissions (
    employee integer NOT NULL,
    add_user boolean DEFAULT false NOT NULL,
    delete_user boolean DEFAULT false NOT NULL,
    change_password boolean DEFAULT true NOT NULL,
    change_other_password boolean DEFAULT false NOT NULL,
    admin boolean DEFAULT false NOT NULL,
    developer boolean DEFAULT false NOT NULL
);


ALTER TABLE permissions OWNER TO postgres;

--
-- Name: price; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE price (
    company integer NOT NULL,
    part_number text NOT NULL,
    sell numeric(15,3) NOT NULL,
    cost numeric(15,3) NOT NULL,
    multiplier numeric(2,2),
    cost_type text
);


ALTER TABLE price OWNER TO postgres;

--
-- Name: project; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE project (
    name text NOT NULL,
    description text,
    company integer NOT NULL,
    path text NOT NULL
);


ALTER TABLE project OWNER TO postgres;

--
-- Name: session; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE session (
    id integer NOT NULL,
    access_token text NOT NULL,
    employee integer NOT NULL,
    expire_dt timestamp with time zone NOT NULL,
    last_ip cidr NOT NULL
);


ALTER TABLE session OWNER TO postgres;

--
-- Name: session_id_seq; Type: SEQUENCE; Schema: opportunity_tracker; Owner: postgres
--

CREATE SEQUENCE session_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE session_id_seq OWNER TO postgres;

--
-- Name: session_id_seq; Type: SEQUENCE OWNED BY; Schema: opportunity_tracker; Owner: postgres
--

ALTER SEQUENCE session_id_seq OWNED BY session.id;


--
-- Name: unit_of_measure; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE unit_of_measure (
    uom text NOT NULL
);


ALTER TABLE unit_of_measure OWNER TO postgres;

--
-- Name: id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY company ALTER COLUMN id SET DEFAULT nextval('company_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY contact ALTER COLUMN id SET DEFAULT nextval('contact_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY employee ALTER COLUMN id SET DEFAULT nextval('employee_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY industry ALTER COLUMN id SET DEFAULT nextval('industry_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY location ALTER COLUMN id SET DEFAULT nextval('location_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notes ALTER COLUMN id SET DEFAULT nextval('notes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notification ALTER COLUMN id SET DEFAULT nextval('notification_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY part ALTER COLUMN id SET DEFAULT nextval('part_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY session ALTER COLUMN id SET DEFAULT nextval('session_id_seq'::regclass);


--
-- Name: company_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY company
    ADD CONSTRAINT company_pkey PRIMARY KEY (id);


--
-- Name: contact_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY contact
    ADD CONSTRAINT contact_pkey PRIMARY KEY (id);


--
-- Name: cost_type_pk; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY cost_type
    ADD CONSTRAINT cost_type_pk PRIMARY KEY (cost_type);


--
-- Name: employee_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (id);


--
-- Name: employee_username_key; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY employee
    ADD CONSTRAINT employee_username_key UNIQUE (username);


--
-- Name: id_pk; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notification
    ADD CONSTRAINT id_pk PRIMARY KEY (id);


--
-- Name: industry_name_key; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY industry
    ADD CONSTRAINT industry_name_key UNIQUE (name);


--
-- Name: industry_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY industry
    ADD CONSTRAINT industry_pkey PRIMARY KEY (id);


--
-- Name: location_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY location
    ADD CONSTRAINT location_pkey PRIMARY KEY (id);


--
-- Name: note_pk; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notes
    ADD CONSTRAINT note_pk PRIMARY KEY (id);


--
-- Name: part_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY part
    ADD CONSTRAINT part_pkey PRIMARY KEY (id);


--
-- Name: part_type_pk; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY part_type
    ADD CONSTRAINT part_type_pk PRIMARY KEY (part_type);


--
-- Name: pk_employee; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY permissions
    ADD CONSTRAINT pk_employee PRIMARY KEY (employee);


--
-- Name: price_pk; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY price
    ADD CONSTRAINT price_pk PRIMARY KEY (company, part_number);


--
-- Name: project_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_pkey PRIMARY KEY (path, company);


--
-- Name: session_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY session
    ADD CONSTRAINT session_pkey PRIMARY KEY (id);


--
-- Name: unique_name; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY company
    ADD CONSTRAINT unique_name UNIQUE (name);


--
-- Name: unit_of_measure_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY unit_of_measure
    ADD CONSTRAINT unit_of_measure_pkey PRIMARY KEY (uom);


--
-- Name: fki_company_fk; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX fki_company_fk ON notes USING btree (company);


--
-- Name: fki_company_fkey; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX fki_company_fkey ON location USING btree (company);


--
-- Name: fki_contact_fk; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX fki_contact_fk ON notes USING btree (contact);


--
-- Name: fki_creator_fk; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX fki_creator_fk ON company USING btree (creator);


--
-- Name: fki_employee_fk; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX fki_employee_fk ON company USING btree (employee);


--
-- Name: fki_part_part_type_fk; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX fki_part_part_type_fk ON part USING btree (part_type);


--
-- Name: fki_part_uom_fk; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX fki_part_uom_fk ON part USING btree (uom);


--
-- Name: i_project_customer; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX i_project_customer ON project USING btree (company);


--
-- Name: company_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notification
    ADD CONSTRAINT company_fk FOREIGN KEY (company) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: company_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notes
    ADD CONSTRAINT company_fk FOREIGN KEY (company) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: company_fkey; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY location
    ADD CONSTRAINT company_fkey FOREIGN KEY (company) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: contact_company_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY contact
    ADD CONSTRAINT contact_company_fk FOREIGN KEY (company) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: contact_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notes
    ADD CONSTRAINT contact_fk FOREIGN KEY (contact) REFERENCES contact(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: creator_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY company
    ADD CONSTRAINT creator_fk FOREIGN KEY (creator) REFERENCES employee(id) ON UPDATE CASCADE;


--
-- Name: employee_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY company
    ADD CONSTRAINT employee_fk FOREIGN KEY (employee) REFERENCES employee(id) ON UPDATE CASCADE;


--
-- Name: employee_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notification
    ADD CONSTRAINT employee_fk FOREIGN KEY (employee) REFERENCES employee(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fk_employee; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY permissions
    ADD CONSTRAINT fk_employee FOREIGN KEY (employee) REFERENCES employee(id) ON DELETE CASCADE;


--
-- Name: part_part_type_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY part
    ADD CONSTRAINT part_part_type_fk FOREIGN KEY (part_type) REFERENCES part_type(part_type);


--
-- Name: part_uom_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY part
    ADD CONSTRAINT part_uom_fk FOREIGN KEY (uom) REFERENCES unit_of_measure(uom);


--
-- Name: price_company_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY price
    ADD CONSTRAINT price_company_fk FOREIGN KEY (company) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: price_cost_type_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY cost_type
    ADD CONSTRAINT price_cost_type_fk FOREIGN KEY (cost_type) REFERENCES cost_type(cost_type);


--
-- Name: session_employee_fkey; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY session
    ADD CONSTRAINT session_employee_fkey FOREIGN KEY (employee) REFERENCES employee(id);


--
-- Name: opportunity_tracker; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA opportunity_tracker FROM PUBLIC;
REVOKE ALL ON SCHEMA opportunity_tracker FROM postgres;
GRANT ALL ON SCHEMA opportunity_tracker TO postgres;


--
-- PostgreSQL database dump complete
--

