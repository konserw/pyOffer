--
-- Table structure for table deliveryDateTerms
--

DROP TABLE IF EXISTS terms_delivery_date;
CREATE TABLE terms_delivery_date
(
    id        SERIAL PRIMARY KEY,
    short_desc text,
    long_desc  text
);

--
-- data for table deliveryDateTerms
--

INSERT INTO terms_delivery_date (short_desc, long_desc)
VALUES ('1-2 dni', '1-2 dni roboczych od daty złożenia zamówienia.'),
       ('1-2 dni, magazyn 2 tyg', '1-2 dni roboczych od daty złożenia zamówienia; w przypadku braku towaru w magazynie w Oleśnicy - ok. 2 tygodnie robocze od daty złożenia zamówienia.'),
       ('1-2 dni, magazyn 2-3 tyg', '1-2 dni roboczych od daty złożenia zamówienia; w przypadku braku towaru w magazynie w Oleśnicy - 2 do 3 tygodni roboczych od daty złożenia zamówienia.'),
       ('1-2 dni, magazyn 2-4 tyg', '1-2 dni roboczych od daty złożenia zamówienia; w przypadku braku towaru w magazynie w Oleśnicy - 2 do 4 tygodni roboczych od daty złożenia zamówienia.'),
       ('1-2 dni, magazyn 3-4 tyg.', '1-2 dni roboczych od daty złożenia zamówienia; w przypadku braku towaru w magazynie w Oleśnicy - 3 do 4 tygodni roboczych od daty złożenia zamówienia.'),
       ('2-3 dni', '2-3 dni roboczych od daty złożenia zamówienia.'),
       ('3-4 dni', '3-4 dni robocze od daty złożenia zamówienia'),
       ('4-5 dni', '4-5 dni roboczych od daty złożenia zamówienia'),
       ('5 dni', '5 dni roboczych od daty złożenia zamówienia.'),
       ('10 dni roboczych', 'ok. 10 dni roboczych'),
       ('1 tydz.', 'ok. 1 tydzień od daty złożenia zamówienia'),
       ('2 tygodnie', 'ok. 2 tygodni roboczych od daty złożenia zamówienia'),
       ('2-3 tygodnie', '2 do 3 tygodni roboczych od daty złożenia zamówienia.'),
       ('2-4 tygodnie', 'ok. 2-4 tygodni roboczych od daty złożenia zamówienia'),
       ('3 tygodnie', 'ok. 3 tygodnie robocze od daty złożenia zamówienia.'),
       ('3-4 tygodnie', 'ok. 3-4 tygodni roboczych od daty złożenia zamówienia'),
       ('3-5 tyg.', 'ok. 3-5 tygodni roboczych od daty złożenia zamówienia'),
       ('4 tygodnie', 'ok. 4 tygodnie robocze od daty złożenia zamówienia.'),
       ('4-5 tygodni', '4 do 5 tygodni roboczych od daty złożenia zamówienia.'),
       ('4-6 tygodni', '4 do 6 tygodni roboczych od daty złożenia zamówienia.'),
       ('5 tygodni', 'ok. 5 tygodni roboczych od daty złożenia zamówienia.'),
       ('5-6 tygodni', 'ok. 5-6 tygodni roboczych od daty złożenia zamówienia'),
       ('6 tygodni', 'ok. 6 tygodni roboczych od daty złożenia zamówienia.'),
       ('6-8 tygodni', '6-8 tygodni roboczych.'),
       ('8-10 tygodni', '8-10 tygodni od daty złożenia zamówienia'),
       ('patrz uwagi', 'patrz uwagi'),
       ('bez zmian', 'Bez zmian.')
;
