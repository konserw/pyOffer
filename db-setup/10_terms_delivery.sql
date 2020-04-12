--
-- Table structure for table terms_delivery
--

DROP TABLE IF EXISTS terms_delivery;
CREATE TABLE terms_delivery
(
    id        SERIAL PRIMARY KEY,
    shortDesc text,
    longDesc  text
);

--
-- Dumping data for table terms_delivery
--

INSERT INTO terms_delivery
VALUES (1, 'dostawcy pow 3000, bez rur', 'Na koszt dostawcy przy zamówieniu powyżej 3000,- zł. netto (nie dot. rur).'),
       (2, 'dostawcy', 'Na koszt dostawcy.'),
       (3, 'odbiorcy', 'Na koszt odbiorcy z magazynu w Oleśnicy.'),
       (4, 'dostawcy pow 3000', 'Na koszt dostawcy przy zamówieniu powyżej 3000,- zł. netto.'),
       (5, 'dostawcy, bez rur', 'Na koszt dostawcy (nie dot. rur w odcinkach 5 i 6 m).'),
       (6, 'dostawcy pow 2000, bez rur', 'Na koszt dostawcy przy zamówieniu powyżej 2000,- zł. netto. (nie dot. rur)'),
       (7, 'do uzgodnienia', 'Do uzgodnienia.'),
       (8, 'wg. ustaleń', 'Zgodnie z ustaleniami.'),
       (9, 'odbiorcy, bez rur', 'Na koszt odbiorcy z magazynu w Oleśnicy (nie dotyczy rur).'),
       (12, 'dostawcy pow. 1500, bez rur', 'Na koszt dostawcy przy zamówieniach powyżej 1500,- zł netto (nie dot. rur).'),
       (13, 'patrz uwagi', 'patrz uwagi'),
       (21, 'Odbiór własny.', 'Odbiór własny z magazynu w Oleśnicy, po uprzednim uzgodnieniu.'),
       (25, 'Dostawcy powyżej 2500', 'Na koszt dostawcy przy zamówieniu powyżej 2.500,- zł. netto.'),
       (26, 'Dostawcy, rury przecięte', 'Na koszt dostawcy (rury przecięte na pół).');

-- Dump completed on 2020-02-15 15:35:16
