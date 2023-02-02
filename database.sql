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
1	31	\N	\N	\N	\N	2023-01-30
2	31	\N	\N	\N	\N	2023-01-30
3	30	\N	\N	\N	\N	2023-01-30
4	31	\N	\N	\N	\N	2023-01-30
5	30	\N	\N	\N	\N	2023-01-30
6	31	\N	\N	\N	\N	2023-01-30
7	28	\N	\N	\N	\N	2023-01-30
8	29	\N	\N	\N	\N	2023-01-30
9	32	200	\N	\N	\N	2023-01-30
10	31	200	\N	\N	\N	2023-01-30
11	31	200	\N	\N	\N	2023-01-30
12	32	200	\N	\N	\N	2023-01-30
13	32	200	\N	Google	\N	2023-01-31
14	33	200	\N	The New York Times - Breaking News, US News, World News and Videos	Live news, investigations, opinion, photos and video by the journalists of The New York Times from more than 150 countries around the world. Subscribe for coverage of U.S. and international news, politics, business, technology, science, health, arts, sports and more.	2023-01-31
15	29	200	psycopg	PostgreSQL driver for Python — Psycopg	Python adapter for PostgreSQL	2023-01-31
16	33	200	\N	The New York Times - Breaking News, US News, World News and Videos	Live news, investigations, opinion, photos and video by the journalists of The New York Times from more than 150 countries around the world. Subscribe for coverage of U.S. and international news, politics, business, technology, science, health, arts, sports and more.	2023-02-01
17	33	200	\N	The New York Times - Breaking News, US News, World News and Videos	Live news, investigations, opinion, photos and video by the journalists of The New York Times from more than 150 countries around the world. Subscribe for coverage of U.S. and international news, politics, business, technology, science, health, arts, sports and more.	2023-02-02
18	30	200	\N	\N	\N	2023-02-02
19	28	200	\N	Яндекс	\N	2023-02-02
20	34	200	Онлайн-школа программирования, за выпускниками которой охотятся компании\n	Хекслет — больше чем школа программирования. Онлайн курсы, сообщество программистов	Живое онлайн сообщество программистов и разработчиков на JS, Python, Java, PHP, Ruby. Авторские программы обучения с практикой и готовыми проектами в резюме. Помощь в трудоустройстве после успешного окончания обучения	2023-02-02
21	35	200	\N	Новости дня в России и мире — РБК	Главные новости политики, экономики и бизнеса, комментарии аналитиков, финансовые данные с российских и мировых биржевых систем на сайте rbc.ru.	2023-02-02
22	28	200	\N	Ой!	\N	2023-02-02
\.


--
-- Data for Name: urls; Type: TABLE DATA; Schema: public; Owner: roman
--

COPY public.urls (id, name, created_at) FROM stdin;
27	https://www.psycop55g.org/	2023-01-27
28	https://yandex.kz/	2023-01-28
29	https://www.psycopg.org	2023-01-28
30	https://ya.ru	2023-01-29
31	https://dev.to	2023-01-29
32	https://www.google.com	2023-01-30
33	https://www.nytimes.com	2023-01-31
34	https://ru.hexlet.io	2023-02-02
35	https://www.rbc.ru	2023-02-02
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

