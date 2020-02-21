--
-- Table structure for table billingTerms
--

DROP TABLE IF EXISTS terms_billing;
CREATE TABLE terms_billing (
  id SERIAL PRIMARY KEY,
  shortDesc text,
  longDesc text
);

--
-- Dumping data for table billingTerms
--

INSERT INTO terms_billing VALUES (1,'przelew 14','Przelewem w terminie 14 dni od daty wystawienia faktury w złotych polskich wg. kursu sprzedaży euro w NBP obowiązującego w dniu wystawienia faktury.'),(2,'przelew 30','Przelewem w terminie 30 dni od daty wystawienia faktury w złotych polskich wg. kursu sprzedaży euro w NBP obowiązującego w dniu wystawienia faktury.'),(3,'przedpłata','Przedpłata w złotych polskich wg. kursu sprzedaży euro w NBP obowiązującego w dniu wystawienia faktury.'),(4,'pobranie','Za pobraniem w złotych polskich wg. kursu sprzedaży euro w NBP obowiązującego w dniu wystawienia faktury.'),(5,'przelew 14 zl','Przelewem w terminie 14 dni od daty wystawienia faktury.'),(6,'przelew 30 zl','Przelewem w terminie 30 dni od daty wystawienia faktury.'),(7,'przedpłata zl','Przedpłata.'),(8,'pobranie zl','Za pobraniem.'),(9,'wg. ustaleń','Zgodnie z ustaleniami.'),(10,'przedpłata, pro-forma','Przedpłata w złotych polskich wg. kursu sprzedaży euro w NBP obowiązującego w dniu wystawienia faktury pro-forma.'),(11,'dokumenty','Do uzgodnienia po otrzymaniu dokumentów firmy (tj. REGON, NIP, KRS) w złotych polskich wg. kursu sprzedaży euro w NBP obowiązującego w dniu wystawienia faktury.'),(12,'dokumenty zl','Do uzgodnienia po otrzymaniu dokumentów firmy (tj. REGON, NIP, KRS).'),(13,'przelew 30 od otrzymania','Przelewem w terminie 30 dni od daty otrzymania faktury w złotych polskich wg. kursu sprzedaży euro w NBP obowiązującego w dniu wystawienia faktury.'),(14,'przelew 60 zl','Przelewem w terminie 60 dni od daty wystawienia faktury.'),(15,'przelew 60','Przelewem w terminie 60 dni od daty wystawienia faktury w złotych polskich wg. kursu sprzedaży euro w NBP obowiązującego w dniu wystawienia faktury.'),(16,'do uzgodnienia','Do uzgodnienia.'),(17,'przedpłata/pobranie','Przedpłata lub za pobraniem w złotych polskich wg. kursu sprzedaży euro w NBP obowiązującego w dniu wystawienia faktury.'),(18,'przedpłata/pobranie zl','Przedpłata lub za pobraniem.'),(19,'przelew 21','Przelewem w terminie 21 dni od daty wystawienia faktury w złotych polskich wg. kursu sprzedaży euro w NBP obowiązującego w dniu wystawienia faktury.'),(20,'przelew 21 zl','Przelewem w terminie 21 dni od daty wystawienia faktury.'),(21,'bez zmian','Bez zmian.'),(22,'przelew 45','Przelewem w terminie 45 dni od daty wystawienia faktury w złotych polskich wg. kursu sprzedaży euro w NBP obowiązującego w dniu wystawienia faktury.'),(25,'50%przedp. / 50% po dost.','50% przedpłata, 50% przelew po dostawie'),(26,'przelew 60','Przelewem w terminie 60 dni od daty wystawienia faktury w złotych polskich wg. kursu sprzedaży euro w NBP obowiązującego w dniu wystawienia faktury.'),(27,'przelew 7','Przelewem w terminie 7 dni od daty wystawienia faktury w złotych polskich wg. kursu sprzedaży euro w NBP obowiązującego w dniu wystawienia faktury.'),(28,'Przelew 7 zł','Przelewem w terminie 9 dni.'),(29,'Przelew 90 zł','Przelewem w terminie 90 dni od daty wystwienia faktury.'),(30,'przelew 45 zł','Przelewem w terminie 45 dni od daty wystawienia faktury.'),(31,'do końca stycznia 2020','Oferta ważna do końca stycznia 2020.');

-- Dump completed on 2020-02-15 15:35:15
