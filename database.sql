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
-- Name: url_checks; Type: TABLE; Schema: public; Owner: roman
--

CREATE TABLE public.url_checks (
    id bigint NOT NULL,
    url_id bigint,
    status_code integer,
    h1 text,
    title text,
    description text,
    created_at date
);


ALTER TABLE public.url_checks OWNER TO roman;

--
-- Name: url_checks_id_seq; Type: SEQUENCE; Schema: public; Owner: roman
--

ALTER TABLE public.url_checks ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.url_checks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: urls; Type: TABLE; Schema: public; Owner: roman
--

CREATE TABLE public.urls (
    id bigint NOT NULL,
    name character varying(255),
    created_at date
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
-- Data for Name: url_checks; Type: TABLE DATA; Schema: public; Owner: roman
--

COPY public.url_checks (id, url_id, status_code, h1, title, description, created_at) FROM stdin;
\.


--
-- Data for Name: urls; Type: TABLE DATA; Schema: public; Owner: roman
--

COPY public.urls (id, name, created_at) FROM stdin;
\.


--
-- Name: url_checks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: roman
--

SELECT pg_catalog.setval('public.url_checks_id_seq', 22, true);


--
-- Name: urls_id_seq; Type: SEQUENCE SET; Schema: public; Owner: roman
--

SELECT pg_catalog.setval('public.urls_id_seq', 35, true);


--
-- Name: url_checks url_checks_pkey; Type: CONSTRAINT; Schema: public; Owner: roman
--

ALTER TABLE ONLY public.url_checks
    ADD CONSTRAINT url_checks_pkey PRIMARY KEY (id);


--
-- Name: urls urls_pkey; Type: CONSTRAINT; Schema: public; Owner: roman
--

ALTER TABLE ONLY public.urls
    ADD CONSTRAINT urls_pkey PRIMARY KEY (id);


--
-- Name: url_checks url_checks_url_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: roman
--

ALTER TABLE ONLY public.url_checks
    ADD CONSTRAINT url_checks_url_id_fkey FOREIGN KEY (url_id) REFERENCES public.urls(id);


--
-- PostgreSQL database dump complete
--

