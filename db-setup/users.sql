--
-- Table structure for table users
--

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id SERIAL,
  name text NOT NULL,
  mail text NOT NULL,
  male BOOLEAN NOT NULL DEFAULT '1',
  phone TEXT DEFAULT NULL,
  current_offer_number int NOT NULL DEFAULT '0',
  current_offer_number_date date NOT NULL DEFAULT '2018-01-01',
  char_for_offer_symbol char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (id)
);

