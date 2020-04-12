--
-- Table structure for table billingTerms
--

DROP TABLE IF EXISTS terms_billing;
CREATE TABLE terms_billing
(
    id        SERIAL PRIMARY KEY,
    shortDesc text,
    longDesc  text
);

--
-- Dumping data for table billingTerms
--

INSERT INTO terms_billing
VALUES (28, 'Przelew 7', 'Przelewem w terminie 7 dni.'),
       (5, 'przelew 14', 'Przelewem w terminie 14 dni od daty wystawienia faktury.'),
       (6, 'przelew 30', 'Przelewem w terminie 30 dni od daty wystawienia faktury.'),
       (7, 'przedpłata', 'Przedpłata.'),
       (8, 'pobranie', 'Za pobraniem.'),
       (9, 'wg. ustaleń', 'Zgodnie z ustaleniami.'),
       (12, 'dokumenty', 'Do uzgodnienia po otrzymaniu dokumentów firmy (tj. REGON, NIP, KRS).'),
       (14, 'przelew 60', 'Przelewem w terminie 60 dni od daty wystawienia faktury.'),
       (16, 'do uzgodnienia', 'Do uzgodnienia.'),
       (18, 'przedpłata/pobranie', 'Przedpłata lub za pobraniem.'),
       (20, 'przelew 21', 'Przelewem w terminie 21 dni od daty wystawienia faktury.'),
       (21, 'bez zmian', 'Bez zmian.'),
       (25, '50%przedp. / 50% po dost.', '50% przedpłata, 50% przelew po dostawie'),
       (29, 'Przelew 90', 'Przelewem w terminie 90 dni od daty wystwienia faktury.'),
       (30, 'przelew 45', 'Przelewem w terminie 45 dni od daty wystawienia faktury.')
;

-- Dump completed on 2020-02-15 15:35:15
