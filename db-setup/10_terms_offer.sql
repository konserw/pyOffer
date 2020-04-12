DROP TABLE IF EXISTS terms_offer;
CREATE TABLE terms_offer
(
    id        SERIAL,
    shortDesc text,
    longDesc  text,
    PRIMARY KEY (id)
);

--
-- data for table terms_offer
--

INSERT INTO terms_offer (shortDesc, longDesc)
VALUES ('3 miesiące', 'Niniejsza oferta jest ważna bez zobowiązań w okresie trzech miesięcy od daty jej sporządzenia.'),
       ('1 miesiąc', 'Niniejsza oferta jest ważna bez zobowiązań w okresie jednego miesięca od daty jej sporządzenia.'),
       ('nic', ''),
       ('Do końca roku', 'Niniejsza oferta zachowuje ważność bez zobowiązań do końca bieżącego roku.')
;
