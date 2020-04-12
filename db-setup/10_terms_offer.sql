DROP TABLE IF EXISTS terms_offer;
CREATE TABLE terms_offer
(
    id        SERIAL,
    short_desc text,
    long_desc  text,
    PRIMARY KEY (id)
);

--
-- data for table terms_offer
--

INSERT INTO terms_offer (short_desc, long_desc)
VALUES ('3 miesiące', 'Niniejsza oferta jest ważna bez zobowiązań w okresie trzech miesięcy od daty jej sporządzenia.'),
       ('1 miesiąc', 'Niniejsza oferta jest ważna bez zobowiązań w okresie jednego miesięca od daty jej sporządzenia.'),
       ('nic', ''),
       ('Do końca roku', 'Niniejsza oferta zachowuje ważność bez zobowiązań do końca bieżącego roku.')
;
