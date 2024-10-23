CREATE SCHEMA IF NOT EXISTS test_pg;
SET SEARCH_PATH = test_pg;

-- Table: rxnconso
-- DROP TABLE IF EXISTS rxnconso;
CREATE TABLE IF NOT EXISTS rxnconso
(
    "RXCUI" character varying(8) COLLATE pg_catalog."default" NOT NULL,
    "LAT" character varying(3) COLLATE pg_catalog."default" NOT NULL DEFAULT 'ENG'::character varying,
    "TS" character varying(1) COLLATE pg_catalog."default",
    "LUI" character varying(8) COLLATE pg_catalog."default",
    "STT" character varying(3) COLLATE pg_catalog."default",
    "SUI" character varying(8) COLLATE pg_catalog."default",
    "ISPREF" character varying(1) COLLATE pg_catalog."default",
    "RXAUI" character varying(8) COLLATE pg_catalog."default" NOT NULL,
    "SAUI" character varying(50) COLLATE pg_catalog."default",
    "SCUI" character varying(50) COLLATE pg_catalog."default",
    "SDUI" character varying(50) COLLATE pg_catalog."default",
    "SAB" character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "TTY" character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "CODE" character varying(50) COLLATE pg_catalog."default" NOT NULL,
    "STR" character varying(3000) COLLATE pg_catalog."default" NOT NULL,
    "SRL" character varying(10) COLLATE pg_catalog."default",
    "SUPPRESS" character varying(1) COLLATE pg_catalog."default",
    "CVF" character varying(50) COLLATE pg_catalog."default",
    create_file_date date,
    last_update_file_date date,
    CONSTRAINT uk_rxnconso UNIQUE NULLS NOT DISTINCT("RXAUI", "RXCUI", "LAT", "SAB", "TTY", "CODE", "STR", "TS", "LUI", "STT", "SUI", "ISPREF", "SAUI", "SCUI", "SDUI", "SRL", "SUPPRESS", "CVF")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

-- Table: rxncuichanges
-- DROP TABLE IF EXISTS rxncuichanges;
CREATE TABLE IF NOT EXISTS rxncuichanges
(
    "RXAUI" character varying(8) COLLATE pg_catalog."default",
    "CODE" character varying(50) COLLATE pg_catalog."default",
    "SAB" character varying(20) COLLATE pg_catalog."default",
    "TTY" character varying(20) COLLATE pg_catalog."default",
    "STR" character varying(3000) COLLATE pg_catalog."default",
    "OLD_RXCUI" character varying(8) COLLATE pg_catalog."default" NOT NULL,
    "NEW_RXCUI" character varying(8) COLLATE pg_catalog."default" NOT NULL,
    create_file_date date,
    last_update_file_date date,
    CONSTRAINT uk_rxncuichanges UNIQUE NULLS NOT DISTINCT ("OLD_RXCUI", "NEW_RXCUI", "RXAUI", "CODE", "SAB", "TTY", "STR")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

-- Table: rxnrel
-- DROP TABLE IF EXISTS rxnrel;
CREATE TABLE IF NOT EXISTS rxnrel
(
    "RXCUI1" character varying(8) COLLATE pg_catalog."default",
    "RXAUI1" character varying(8) COLLATE pg_catalog."default",
    "STYPE1" character varying(50) COLLATE pg_catalog."default",
    "REL" character varying(4) COLLATE pg_catalog."default",
    "RXCUI2" character varying(8) COLLATE pg_catalog."default",
    "RXAUI2" character varying(9) COLLATE pg_catalog."default",
    "STYPE2" character varying(50) COLLATE pg_catalog."default",
    "RELA" character varying(100) COLLATE pg_catalog."default",
    "RUI" character varying(10) COLLATE pg_catalog."default",
    "SRUI" character varying(50) COLLATE pg_catalog."default",
    "SAB" character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "SL" character varying(1000) COLLATE pg_catalog."default",
    "DIR" character varying(1) COLLATE pg_catalog."default",
    "RG" character varying(10) COLLATE pg_catalog."default",
    "SUPPRESS" character varying(1) COLLATE pg_catalog."default",
    "CVF" character varying(50) COLLATE pg_catalog."default",
    create_file_date date,
    last_update_file_date date,
    CONSTRAINT uk_rxnrel UNIQUE NULLS NOT DISTINCT ("RXAUI1", "RXCUI1", "RXAUI2", "RXCUI2", "REL", "RUI", "RELA", "SAB", "STYPE1", "STYPE2", "SRUI", "SL", "DIR", "RG", "SUPPRESS", "CVF")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

-- Table: rxnsat
-- DROP TABLE IF EXISTS rxnsat;
CREATE TABLE IF NOT EXISTS rxnsat
(
    "RXCUI" character varying(8) COLLATE pg_catalog."default",
    "LUI" character varying(8) COLLATE pg_catalog."default",
    "SUI" character varying(8) COLLATE pg_catalog."default",
    "RXAUI" character varying(9) COLLATE pg_catalog."default",
    "STYPE" character varying(50) COLLATE pg_catalog."default",
    "CODE" character varying(50) COLLATE pg_catalog."default",
    "ATUI" character varying(11) COLLATE pg_catalog."default",
    "SATUI" character varying(50) COLLATE pg_catalog."default",
    "ATN" character varying(1000) COLLATE pg_catalog."default" NOT NULL,
    "SAB" character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "ATV" character varying(4000) COLLATE pg_catalog."default",
    "SUPPRESS" character varying(1) COLLATE pg_catalog."default",
    "CVF" character varying(50) COLLATE pg_catalog."default",
    create_file_date date,
    last_update_file_date date,
    CONSTRAINT uk_rxnsat UNIQUE NULLS NOT DISTINCT ("RXAUI", "RXCUI", "SAB", "ATN", "ATV", "LUI", "SUI", "STYPE", "CODE", "ATUI", "SATUI", "SUPPRESS", "CVF")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

-- Table: rxnsty
-- DROP TABLE IF EXISTS rxnsty;
CREATE TABLE IF NOT EXISTS rxnsty
(
    "RXCUI" character varying(8) COLLATE pg_catalog."default" NOT NULL,
    "TUI" character varying(4) COLLATE pg_catalog."default",
    "STN" character varying(100) COLLATE pg_catalog."default",
    "STY" character varying(50) COLLATE pg_catalog."default",
    "ATUI" character varying(11) COLLATE pg_catalog."default",
    "CVF" character varying(50) COLLATE pg_catalog."default",
    create_file_date date,
    last_update_file_date date,
    CONSTRAINT uk_rxnsty UNIQUE NULLS NOT DISTINCT ("RXCUI", "STY", "TUI", "STN", "ATUI", "CVF") 
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;