--
-- Table structure for table terms_delivery
--

DROP TABLE IF EXISTS terms_delivery;
CREATE TABLE terms_delivery
(
    id        SERIAL PRIMARY KEY,
    short_desc text,
    long_desc  text
);

--
-- data for table terms_delivery
--

INSERT INTO terms_delivery (short_desc, long_desc)
VALUES ('dostawcy', 'Na koszt dostawcy.'),
       ('dostawcy, rury przecięte', 'Na koszt dostawcy (rury przecięte na pół).'),
       ('dostawcy, bez rur', 'Na koszt dostawcy (nie dot. rur w odcinkach 5 i 6 m).'),
       ('dostawcy pow. 1500, bez rur', 'Na koszt dostawcy przy zamówieniach powyżej 1500,- zł netto (nie dot. rur).'),
       ('dostawcy pow 2000, bez rur', 'Na koszt dostawcy przy zamówieniu powyżej 2000,- zł. netto. (nie dot. rur)'),
       ('dostawcy powyżej 2500', 'Na koszt dostawcy przy zamówieniu powyżej 2500,- zł. netto.'),
       ('dostawcy pow 3000', 'Na koszt dostawcy przy zamówieniu powyżej 3000,- zł. netto.'),
       ('dostawcy pow 3000, bez rur', 'Na koszt dostawcy przy zamówieniu powyżej 3000,- zł. netto (nie dot. rur).'),
       ('odbiorcy', 'Na koszt odbiorcy z magazynu w Oleśnicy.'),
       ('odbiorcy, bez rur', 'Na koszt odbiorcy z magazynu w Oleśnicy (nie dotyczy rur).'),
       ('odbiór własny.', 'Odbiór własny z magazynu w Oleśnicy, po uprzednim uzgodnieniu.'),
       ('do uzgodnienia', 'Do uzgodnienia.'),
       ('wg. ustaleń', 'Zgodnie z ustaleniami.'),
       ('patrz uwagi', 'patrz uwagi')
;
