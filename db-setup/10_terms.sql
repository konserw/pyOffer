--
-- Table structure for table terms
--

DROP TABLE IF EXISTS terms_billing;
CREATE TABLE terms
(
    term_id    SERIAL PRIMARY KEY,
    term_type  int,
    short_desc text,
    long_desc  text
);
--    delivery = 0
--    offer = 1
--    billing = 2
--    delivery_date = 3
--    remarks = 4

--
-- data for table terms
--

-- delivery
INSERT INTO terms (term_type, short_desc, long_desc)
VALUES (0, 'dostawcy', 'Na koszt dostawcy.'),
       (0, 'dostawcy, rury przecięte', 'Na koszt dostawcy (rury przecięte na pół).'),
       (0, 'dostawcy, bez rur', 'Na koszt dostawcy (nie dot. rur w odcinkach 5 i 6 m).'),
       (0, 'dostawcy pow. 1500, bez rur', 'Na koszt dostawcy przy zamówieniach powyżej 1500,- zł netto (nie dot. rur).'),
       (0, 'dostawcy pow 2000, bez rur', 'Na koszt dostawcy przy zamówieniu powyżej 2000,- zł. netto. (nie dot. rur)'),
       (0, 'dostawcy powyżej 2500', 'Na koszt dostawcy przy zamówieniu powyżej 2500,- zł. netto.'),
       (0, 'dostawcy pow 3000', 'Na koszt dostawcy przy zamówieniu powyżej 3000,- zł. netto.'),
       (0, 'dostawcy pow 3000, bez rur', 'Na koszt dostawcy przy zamówieniu powyżej 3000,- zł. netto (nie dot. rur).'),
       (0, 'odbiorcy', 'Na koszt odbiorcy z magazynu w Oleśnicy.'),
       (0, 'odbiorcy, bez rur', 'Na koszt odbiorcy z magazynu w Oleśnicy (nie dotyczy rur).'),
       (0, 'odbiór własny.', 'Odbiór własny z magazynu w Oleśnicy, po uprzednim uzgodnieniu.'),
       (0, 'do uzgodnienia', 'Do uzgodnienia.'),
       (0, 'wg. ustaleń', 'Zgodnie z ustaleniami.'),
       (0, 'patrz uwagi', 'patrz uwagi')
;

-- offer
INSERT INTO terms (term_type, short_desc, long_desc)
VALUES (1, '3 miesiące', 'Niniejsza oferta jest ważna bez zobowiązań w okresie trzech miesięcy od daty jej sporządzenia.'),
       (1, '1 miesiąc', 'Niniejsza oferta jest ważna bez zobowiązań w okresie jednego miesięca od daty jej sporządzenia.'),
       (1, 'nic', ''),
       (1, 'Do końca roku', 'Niniejsza oferta zachowuje ważność bez zobowiązań do końca bieżącego roku.')
;

-- billing
INSERT INTO terms (term_type, short_desc, long_desc)
VALUES (2, 'Przelew 7', 'Przelewem w terminie 7 dni.'),
       (2, 'przelew 14', 'Przelewem w terminie 14 dni od daty wystawienia faktury.'),
       (2, 'przelew 21', 'Przelewem w terminie 21 dni od daty wystawienia faktury.'),
       (2, 'przelew 30', 'Przelewem w terminie 30 dni od daty wystawienia faktury.'),
       (2, 'przelew 60', 'Przelewem w terminie 60 dni od daty wystawienia faktury.'),
       (2, 'przelew 45', 'Przelewem w terminie 45 dni od daty wystawienia faktury.'),
       (2, 'Przelew 90', 'Przelewem w terminie 90 dni od daty wystawienia faktury.'),
       (2, 'przedpłata', 'Przedpłata.'),
       (2, 'pobranie', 'Za pobraniem.'),
       (2, 'przedpłata/pobranie', 'Przedpłata lub za pobraniem.'),
       (2, '50% przedp. / 50% po dost.', '50% przedpłata, 50% przelew po dostawie'),
       (2, 'wg. ustaleń', 'Zgodnie z ustaleniami.'),
       (2, 'dokumenty', 'Do uzgodnienia po otrzymaniu dokumentów firmy (tj. REGON, NIP, KRS).'),
       (2, 'do uzgodnienia', 'Do uzgodnienia.'),
       (2, 'bez zmian', 'Bez zmian.')
;

-- delivery date
INSERT INTO terms (term_type, short_desc, long_desc)
VALUES (3, '1-2 dni', '1-2 dni roboczych od daty złożenia zamówienia.'),
       (3, '1-2 dni, magazyn 2 tyg', '1-2 dni roboczych od daty złożenia zamówienia; w przypadku braku towaru w magazynie w Oleśnicy - ok. 2 tygodnie robocze od daty złożenia zamówienia.'),
       (3, '1-2 dni, magazyn 2-3 tyg', '1-2 dni roboczych od daty złożenia zamówienia; w przypadku braku towaru w magazynie w Oleśnicy - 2 do 3 tygodni roboczych od daty złożenia zamówienia.'),
       (3, '1-2 dni, magazyn 2-4 tyg', '1-2 dni roboczych od daty złożenia zamówienia; w przypadku braku towaru w magazynie w Oleśnicy - 2 do 4 tygodni roboczych od daty złożenia zamówienia.'),
       (3, '1-2 dni, magazyn 3-4 tyg.', '1-2 dni roboczych od daty złożenia zamówienia; w przypadku braku towaru w magazynie w Oleśnicy - 3 do 4 tygodni roboczych od daty złożenia zamówienia.'),
       (3, '2-3 dni', '2-3 dni roboczych od daty złożenia zamówienia.'),
       (3, '3-4 dni', '3-4 dni robocze od daty złożenia zamówienia'),
       (3, '4-5 dni', '4-5 dni roboczych od daty złożenia zamówienia'),
       (3, '5 dni', '5 dni roboczych od daty złożenia zamówienia.'),
       (3, '10 dni roboczych', 'ok. 10 dni roboczych'),
       (3, '1 tydz.', 'ok. 1 tydzień od daty złożenia zamówienia'),
       (3, '2 tygodnie', 'ok. 2 tygodni roboczych od daty złożenia zamówienia'),
       (3, '2-3 tygodnie', '2 do 3 tygodni roboczych od daty złożenia zamówienia.'),
       (3, '2-4 tygodnie', 'ok. 2-4 tygodni roboczych od daty złożenia zamówienia'),
       (3, '3 tygodnie', 'ok. 3 tygodnie robocze od daty złożenia zamówienia.'),
       (3, '3-4 tygodnie', 'ok. 3-4 tygodni roboczych od daty złożenia zamówienia'),
       (3, '3-5 tyg.', 'ok. 3-5 tygodni roboczych od daty złożenia zamówienia'),
       (3, '4 tygodnie', 'ok. 4 tygodnie robocze od daty złożenia zamówienia.'),
       (3, '4-5 tygodni', '4 do 5 tygodni roboczych od daty złożenia zamówienia.'),
       (3, '4-6 tygodni', '4 do 6 tygodni roboczych od daty złożenia zamówienia.'),
       (3, '5 tygodni', 'ok. 5 tygodni roboczych od daty złożenia zamówienia.'),
       (3, '5-6 tygodni', 'ok. 5-6 tygodni roboczych od daty złożenia zamówienia'),
       (3, '6 tygodni', 'ok. 6 tygodni roboczych od daty złożenia zamówienia.'),
       (3, '6-8 tygodni', '6-8 tygodni roboczych.'),
       (3, '8-10 tygodni', '8-10 tygodni od daty złożenia zamówienia'),
       (3, 'patrz uwagi', 'patrz uwagi'),
       (3, 'bez zmian', 'Bez zmian.')
;
