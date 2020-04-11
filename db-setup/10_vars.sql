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

INSERT INTO vars
VALUES (1, 'order email', 'biuro.pl@aliaxis.com');