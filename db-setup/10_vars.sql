--
-- Table structure for table vars
--

DROP TABLE IF EXISTS vars;
CREATE TABLE vars
(
    id    SERIAL PRIMARY KEY,
    key   TEXT DEFAULT NULL,
    value TEXT DEFAULT NULL
);

--
-- Dumping data for table vars
--

INSERT INTO public.vars
VALUES (1, 'order email', 'biuro.pl@aliaxis.com');

INSERT INTO public.vars
VALUES (2, 'HQ', 'Nicoll Polska Sp. z o.o.<br />ul. Energetyczna 6, 56-400 Oleśnica');
