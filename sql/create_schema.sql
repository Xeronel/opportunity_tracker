--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

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

--
-- Name: cut_added(); Type: FUNCTION; Schema: opportunity_tracker; Owner: postgres
--

CREATE FUNCTION cut_added() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
	NEW.remaining = NEW.qty - NEW.complete;
    RETURN NEW;
END
$$;


ALTER FUNCTION opportunity_tracker.cut_added() OWNER TO postgres;

--
-- Name: reel_added(); Type: FUNCTION; Schema: opportunity_tracker; Owner: postgres
--

CREATE FUNCTION reel_added() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
	NEW.current_qty = NEW.qty;
    RETURN NEW;
END$$;


ALTER FUNCTION opportunity_tracker.reel_added() OWNER TO postgres;

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
-- Name: kit_bom; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE kit_bom (
    kit_part_number text NOT NULL,
    part_number text NOT NULL,
    qty integer NOT NULL
);


ALTER TABLE kit_bom OWNER TO postgres;

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
-- Name: station; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE station (
    location text NOT NULL,
    ip_address inet,
    id integer NOT NULL,
    active_work_order integer,
    employee integer NOT NULL
);


ALTER TABLE station OWNER TO postgres;

--
-- Name: unit_of_measure; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE unit_of_measure (
    uom text NOT NULL,
    label text
);


ALTER TABLE unit_of_measure OWNER TO postgres;

--
-- Name: wire_station_id_seq; Type: SEQUENCE; Schema: opportunity_tracker; Owner: postgres
--

CREATE SEQUENCE wire_station_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE wire_station_id_seq OWNER TO postgres;

--
-- Name: wire_station_id_seq; Type: SEQUENCE OWNED BY; Schema: opportunity_tracker; Owner: postgres
--

ALTER SEQUENCE wire_station_id_seq OWNED BY station.id;


--
-- Name: work_order; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE work_order (
    id integer NOT NULL,
    station integer NOT NULL,
    complete boolean DEFAULT false NOT NULL,
    creator integer NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE work_order OWNER TO postgres;

--
-- Name: work_order_consumable; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE work_order_consumable (
    id integer NOT NULL,
    part_number text NOT NULL,
    qty integer NOT NULL,
    work_order integer,
    current_qty integer
);


ALTER TABLE work_order_consumable OWNER TO postgres;

--
-- Name: work_order_items; Type: TABLE; Schema: opportunity_tracker; Owner: postgres
--

CREATE TABLE work_order_items (
    id integer NOT NULL,
    part_number text NOT NULL,
    qty integer NOT NULL,
    work_order integer NOT NULL,
    complete integer DEFAULT 0 NOT NULL,
    consume_qty integer NOT NULL,
    remaining integer
);


ALTER TABLE work_order_items OWNER TO postgres;

--
-- Name: work_order_cuts_id_seq; Type: SEQUENCE; Schema: opportunity_tracker; Owner: postgres
--

CREATE SEQUENCE work_order_cuts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE work_order_cuts_id_seq OWNER TO postgres;

--
-- Name: work_order_cuts_id_seq; Type: SEQUENCE OWNED BY; Schema: opportunity_tracker; Owner: postgres
--

ALTER SEQUENCE work_order_cuts_id_seq OWNED BY work_order_items.id;


--
-- Name: work_order_id_seq; Type: SEQUENCE; Schema: opportunity_tracker; Owner: postgres
--

CREATE SEQUENCE work_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE work_order_id_seq OWNER TO postgres;

--
-- Name: work_order_id_seq; Type: SEQUENCE OWNED BY; Schema: opportunity_tracker; Owner: postgres
--

ALTER SEQUENCE work_order_id_seq OWNED BY work_order.id;


--
-- Name: work_order_reels_id_seq; Type: SEQUENCE; Schema: opportunity_tracker; Owner: postgres
--

CREATE SEQUENCE work_order_reels_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE work_order_reels_id_seq OWNER TO postgres;

--
-- Name: work_order_reels_id_seq; Type: SEQUENCE OWNED BY; Schema: opportunity_tracker; Owner: postgres
--

ALTER SEQUENCE work_order_reels_id_seq OWNED BY work_order_consumable.id;


--
-- Name: company id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY company ALTER COLUMN id SET DEFAULT nextval('company_id_seq'::regclass);


--
-- Name: contact id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY contact ALTER COLUMN id SET DEFAULT nextval('contact_id_seq'::regclass);


--
-- Name: employee id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY employee ALTER COLUMN id SET DEFAULT nextval('employee_id_seq'::regclass);


--
-- Name: location id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY location ALTER COLUMN id SET DEFAULT nextval('location_id_seq'::regclass);


--
-- Name: notes id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notes ALTER COLUMN id SET DEFAULT nextval('notes_id_seq'::regclass);


--
-- Name: notification id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notification ALTER COLUMN id SET DEFAULT nextval('notification_id_seq'::regclass);


--
-- Name: session id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY session ALTER COLUMN id SET DEFAULT nextval('session_id_seq'::regclass);


--
-- Name: station id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY station ALTER COLUMN id SET DEFAULT nextval('wire_station_id_seq'::regclass);


--
-- Name: work_order id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY work_order ALTER COLUMN id SET DEFAULT nextval('work_order_id_seq'::regclass);


--
-- Name: work_order_consumable id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY work_order_consumable ALTER COLUMN id SET DEFAULT nextval('work_order_reels_id_seq'::regclass);


--
-- Name: work_order_items id; Type: DEFAULT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY work_order_items ALTER COLUMN id SET DEFAULT nextval('work_order_cuts_id_seq'::regclass);


--
-- Name: company company_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY company
    ADD CONSTRAINT company_pkey PRIMARY KEY (id);


--
-- Name: contact contact_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY contact
    ADD CONSTRAINT contact_pkey PRIMARY KEY (id);


--
-- Name: cost_type cost_type_pk; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY cost_type
    ADD CONSTRAINT cost_type_pk PRIMARY KEY (cost_type);


--
-- Name: employee employee_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (id);


--
-- Name: employee employee_username_key; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY employee
    ADD CONSTRAINT employee_username_key UNIQUE (username);


--
-- Name: notification id_pk; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notification
    ADD CONSTRAINT id_pk PRIMARY KEY (id);


--
-- Name: kit_bom kit_bom_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY kit_bom
    ADD CONSTRAINT kit_bom_pkey PRIMARY KEY (kit_part_number, part_number);


--
-- Name: location location_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY location
    ADD CONSTRAINT location_pkey PRIMARY KEY (id);


--
-- Name: notes note_pk; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notes
    ADD CONSTRAINT note_pk PRIMARY KEY (id);


--
-- Name: part part_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY part
    ADD CONSTRAINT part_pkey PRIMARY KEY (part_number);


--
-- Name: part_type part_type_pk; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY part_type
    ADD CONSTRAINT part_type_pk PRIMARY KEY (part_type);


--
-- Name: permissions pk_employee; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY permissions
    ADD CONSTRAINT pk_employee PRIMARY KEY (employee);


--
-- Name: price price_pk; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY price
    ADD CONSTRAINT price_pk PRIMARY KEY (company, part_number);


--
-- Name: project project_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_pkey PRIMARY KEY (path, company);


--
-- Name: session session_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY session
    ADD CONSTRAINT session_pkey PRIMARY KEY (id);


--
-- Name: company unique_name; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY company
    ADD CONSTRAINT unique_name UNIQUE (name);


--
-- Name: unit_of_measure unit_of_measure_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY unit_of_measure
    ADD CONSTRAINT unit_of_measure_pkey PRIMARY KEY (uom);


--
-- Name: station wire_station_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY station
    ADD CONSTRAINT wire_station_pkey PRIMARY KEY (id);


--
-- Name: work_order_items work_order_cuts_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY work_order_items
    ADD CONSTRAINT work_order_cuts_pkey PRIMARY KEY (id);


--
-- Name: work_order work_order_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY work_order
    ADD CONSTRAINT work_order_pkey PRIMARY KEY (id);


--
-- Name: work_order_consumable work_order_reels_pkey; Type: CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY work_order_consumable
    ADD CONSTRAINT work_order_reels_pkey PRIMARY KEY (id);


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
-- Name: fki_kit_bom_part_number; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX fki_kit_bom_part_number ON kit_bom USING btree (part_number);


--
-- Name: fki_kit_part_number; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX fki_kit_part_number ON kit_bom USING btree (kit_part_number);


--
-- Name: fki_part_part_type_fk; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX fki_part_part_type_fk ON part USING btree (part_type);


--
-- Name: fki_part_uom_fk; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX fki_part_uom_fk ON part USING btree (uom);


--
-- Name: fki_price_cost_type_fk; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX fki_price_cost_type_fk ON price USING btree (cost_type);


--
-- Name: fki_price_part_number_fk; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX fki_price_part_number_fk ON price USING btree (part_number);


--
-- Name: i_project_customer; Type: INDEX; Schema: opportunity_tracker; Owner: postgres
--

CREATE INDEX i_project_customer ON project USING btree (company);


--
-- Name: work_order_consumable new_reel; Type: TRIGGER; Schema: opportunity_tracker; Owner: postgres
--

CREATE TRIGGER new_reel BEFORE INSERT ON work_order_consumable FOR EACH ROW EXECUTE PROCEDURE reel_added();


--
-- Name: work_order_items remaining_update; Type: TRIGGER; Schema: opportunity_tracker; Owner: postgres
--

CREATE TRIGGER remaining_update BEFORE INSERT OR UPDATE ON work_order_items FOR EACH ROW EXECUTE PROCEDURE cut_added();


--
-- Name: notification company_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notification
    ADD CONSTRAINT company_fk FOREIGN KEY (company) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: notes company_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notes
    ADD CONSTRAINT company_fk FOREIGN KEY (company) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: location company_fkey; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY location
    ADD CONSTRAINT company_fkey FOREIGN KEY (company) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: contact contact_company_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY contact
    ADD CONSTRAINT contact_company_fk FOREIGN KEY (company) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: notes contact_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notes
    ADD CONSTRAINT contact_fk FOREIGN KEY (contact) REFERENCES contact(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: company creator_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY company
    ADD CONSTRAINT creator_fk FOREIGN KEY (creator) REFERENCES employee(id) ON UPDATE CASCADE;


--
-- Name: company employee_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY company
    ADD CONSTRAINT employee_fk FOREIGN KEY (employee) REFERENCES employee(id) ON UPDATE CASCADE;


--
-- Name: notification employee_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY notification
    ADD CONSTRAINT employee_fk FOREIGN KEY (employee) REFERENCES employee(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: permissions fk_employee; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY permissions
    ADD CONSTRAINT fk_employee FOREIGN KEY (employee) REFERENCES employee(id) ON DELETE CASCADE;


--
-- Name: work_order fk_work_order_employee; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY work_order
    ADD CONSTRAINT fk_work_order_employee FOREIGN KEY (creator) REFERENCES employee(id);


--
-- Name: work_order fk_work_order_station; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY work_order
    ADD CONSTRAINT fk_work_order_station FOREIGN KEY (station) REFERENCES station(id);


--
-- Name: kit_bom kit_bom_kit_part_number_fkey; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY kit_bom
    ADD CONSTRAINT kit_bom_kit_part_number_fkey FOREIGN KEY (kit_part_number) REFERENCES part(part_number) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: kit_bom kit_bom_part_number_fkey; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY kit_bom
    ADD CONSTRAINT kit_bom_part_number_fkey FOREIGN KEY (part_number) REFERENCES part(part_number);


--
-- Name: part part_part_type_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY part
    ADD CONSTRAINT part_part_type_fk FOREIGN KEY (part_type) REFERENCES part_type(part_type);


--
-- Name: part part_uom_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY part
    ADD CONSTRAINT part_uom_fk FOREIGN KEY (uom) REFERENCES unit_of_measure(uom);


--
-- Name: price price_company_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY price
    ADD CONSTRAINT price_company_fk FOREIGN KEY (company) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: price price_cost_type_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY price
    ADD CONSTRAINT price_cost_type_fk FOREIGN KEY (cost_type) REFERENCES cost_type(cost_type) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: price price_part_number_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY price
    ADD CONSTRAINT price_part_number_fk FOREIGN KEY (part_number) REFERENCES part(part_number) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: project project_company_fk; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_company_fk FOREIGN KEY (company) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: session session_employee_fkey; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY session
    ADD CONSTRAINT session_employee_fkey FOREIGN KEY (employee) REFERENCES employee(id);


--
-- Name: station wire_station_active_work_order_fkey; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY station
    ADD CONSTRAINT wire_station_active_work_order_fkey FOREIGN KEY (active_work_order) REFERENCES work_order(id);


--
-- Name: station wire_station_employee_fkey; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY station
    ADD CONSTRAINT wire_station_employee_fkey FOREIGN KEY (employee) REFERENCES employee(id);


--
-- Name: work_order_items work_order_cuts_part_number_fkey; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY work_order_items
    ADD CONSTRAINT work_order_cuts_part_number_fkey FOREIGN KEY (part_number) REFERENCES part(part_number);


--
-- Name: work_order_items work_order_cuts_work_order_fkey; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY work_order_items
    ADD CONSTRAINT work_order_cuts_work_order_fkey FOREIGN KEY (work_order) REFERENCES work_order(id);


--
-- Name: work_order_consumable work_order_reels_part_number_fkey; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY work_order_consumable
    ADD CONSTRAINT work_order_reels_part_number_fkey FOREIGN KEY (part_number) REFERENCES part(part_number);


--
-- Name: work_order_consumable work_order_reels_work_order_fkey; Type: FK CONSTRAINT; Schema: opportunity_tracker; Owner: postgres
--

ALTER TABLE ONLY work_order_consumable
    ADD CONSTRAINT work_order_reels_work_order_fkey FOREIGN KEY (work_order) REFERENCES work_order(id);


--
-- PostgreSQL database dump complete
--

