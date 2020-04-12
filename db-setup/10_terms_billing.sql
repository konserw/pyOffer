--
-- Table structure for table billingTerms
--

DROP TABLE IF EXISTS terms_billing;
CREATE TABLE terms_billing
(
    id        SERIAL PRIMARY KEY,
    short_desc text,
    long_desc  text
);

--
-- data for table billingTerms
--

INSERT INTO terms_billing (short_desc, long_desc)
VALUES ('Przelew 7', 'Przelewem w terminie 7 dni.'),
       ('przelew 14', 'Przelewem w terminie 14 dni od daty wystawienia faktury.'),
       ('przelew 21', 'Przelewem w terminie 21 dni od daty wystawienia faktury.'),
       ('przelew 30', 'Przelewem w terminie 30 dni od daty wystawienia faktury.'),
       ('przelew 60', 'Przelewem w terminie 60 dni od daty wystawienia faktury.'),
       ('przelew 45', 'Przelewem w terminie 45 dni od daty wystawienia faktury.'),
       ('Przelew 90', 'Przelewem w terminie 90 dni od daty wystawienia faktury.'),
       ('przedpłata', 'Przedpłata.'),
       ('pobranie', 'Za pobraniem.'),
       ('przedpłata/pobranie', 'Przedpłata lub za pobraniem.'),
       ('50% przedp. / 50% po dost.', '50% przedpłata, 50% przelew po dostawie'),
       ('wg. ustaleń', 'Zgodnie z ustaleniami.'),
       ('dokumenty', 'Do uzgodnienia po otrzymaniu dokumentów firmy (tj. REGON, NIP, KRS).'),
       ('do uzgodnienia', 'Do uzgodnienia.'),
       ('bez zmian', 'Bez zmian.')
;
