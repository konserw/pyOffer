--
-- Table structure for table deliveryDateTerms
--

DROP TABLE IF EXISTS terms_delivery_date;
CREATE TABLE terms_delivery_date
(
    id        SERIAL PRIMARY KEY,
    shortDesc text,
    longDesc  text
);

--
-- Dumping data for table deliveryDateTerms
--

INSERT INTO terms_delivery_date
VALUES (1, '1-2 dni', '1-2 dni roboczych od daty złożenia zamówienia.'),
       (2, '2-3 tygodnie', '2 do 3 tygodni roboczych od daty złożenia zamówienia.'),
       (3, '4-6 tygodni', '4 do 6 tygodni roboczych od daty złożenia zamówienia.'),
       (4, '2-3 dni', '2-3 dni roboczych od daty złożenia zamówienia.'),
       (5, '1-2 dni, magazyn 2-3 tyg', '1-2 dni roboczych od daty złożenia zamówienia; w przypadku braku towaru w magazynie w Oleśnicy - 2 do 3 tygodni roboczych od daty złożenia zamówienia.'),
       (6, '4 tygodnie', 'ok. 4 tygodnie robocze od daty złożenia zamówienia.'),
       (7, '2 tygodnie', 'ok. 2 tygodni roboczych od daty złożenia zamówienia'),
       (8, '6 tygodni', 'ok. 6 tygodni roboczych od daty złożenia zamówienia.'),
       (9, '5 dni', '5 dni roboczych od daty złożenia zamówienia.'),
       (10, '3-4 dni', '3-4 dni robocze od daty złożenia zamówienia'),
       (11, '4-5 tygodni', '4 do 5 tygodni roboczych od daty złożenia zamówienia.'),
       (12, '4-5 dni', '4-5 dni roboczych od daty złożenia zamówienia'),
       (13, '3-4 tygodnie', 'ok. 3-4 tyg. od daty złożenia zamówienia'),
       (14, '1-2 dni, magazyn 2 tyg', '1-2 dni roboczych od daty złożenia zamówienia; w przypadku braku towaru w magazynie w Oleśnicy - ok. 2 tygodnie robocze od daty złożenia zamówienia.'),
       (15, '1-2 dni, magazyn 2-4 tyg', '1-2 dni roboczych od daty złożenia zamówienia; w przypadku braku towaru w magazynie w Oleśnicy - 2 do 4 tygodni roboczych od daty złożenia zamówienia.'),
       (16, 'patrz uwagi', 'patrz uwagi'),
       (17, 'bez zmian', 'Bez zmian.'),
       (18, '1-2 dni, magazyn 3-4 tyg.', '1-2 dni roboczych od daty złożenia zamówienia; w przypadku braku towaru w magazynie w Oleśnicy- 3 do 4 tygodni roboczych od daty złożenia zamówienia.'),
       (19, '1 tydz.', 'ok. 1 tydz. od daty złożenia zamówienia'),
       (20, '10 dni roboczych', 'ok. 10 dni roboczych'),
       (21, '3 tyg.', 'ok. 3 tygodnie robocze od daty złożenia zamówienia.'),
       (22, '8-10 tygodni', '8-10 tygodni od daty złożenia zamówienia'),
       (24, '2-4 tygodnie', 'ok. 2-4 tygodni roboczych od daty złożenia zamówienia'),
       (25, '6-8 tygodni', '6-8 tygodni roboczych.'),
       (28, '5-6 tyg.', 'ok. 5-6 tygodni roboczych od daty złożenia zamówienia'),
       (29, '3-5 tyg.', 'ok. 3-5 tygodni roboczych od daty złożenia zamówienia'),
       (30, '5 tygodni', 'ok. 5 tygodni roboczych od daty złożenia zamówienia.');


-- Dump completed on 2020-02-15 15:35:10
