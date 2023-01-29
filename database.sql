--
-- PostgreSQL database dump
--

-- Dumped from database version 14.6 (Ubuntu 14.6-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.6 (Ubuntu 14.6-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: urls; Type: TABLE; Schema: public; Owner: roman
--

CREATE TABLE public.urls (
    id bigint NOT NULL,
    name character varying(255),
    created_at timestamp without time zone
);


ALTER TABLE public.urls OWNER TO roman;

--
-- Name: urls_id_seq; Type: SEQUENCE; Schema: public; Owner: roman
--

ALTER TABLE public.urls ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.urls_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: urls; Type: TABLE DATA; Schema: public; Owner: roman
--

COPY public.urls (id, name, created_at) FROM stdin;
1	Some	2023-01-03 19:10:25
\.


--
-- Name: urls_id_seq; Type: SEQUENCE SET; Schema: public; Owner: roman
--

SELECT pg_catalog.setval('public.urls_id_seq', 1, true);


--
-- Name: urls urls_pkey; Type: CONSTRAINT; Schema: public; Owner: roman
--

ALTER TABLE ONLY public.urls
    ADD CONSTRAINT urls_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

