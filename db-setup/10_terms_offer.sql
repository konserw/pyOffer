DROP TABLE IF EXISTS terms_offer;
CREATE TABLE terms_offer (
  id SERIAL,
  shortDesc text,
  longDesc text,
  PRIMARY KEY (id)
);

--
-- Dumping data for table terms_offer
--

INSERT INTO terms_offer VALUES (1,'3 miesiące','Niniejsza oferta jest ważna bez zobowiązań w okresie trzech miesięcy od daty jej sporządzenia.'),(2,'1 miesiąc','Niniejsza oferta jest ważna bez zobowiązań w okresie jednego miesięca od daty jej sporządzenia.'),(3,'nic',''),(4,'Do końca roku','Niniejsza oferta zachowuje ważność bez zobowiązań do końca bieżącego roku.'),(5,'Koniec stycznia 2020','Oferta ważna do końca stycznia 2020r.'),(6,'Koniec lutego 2020r.','Oferta ważna do końca lutego 2020r.');

-- Dump completed on 2020-02-15 15:35:19