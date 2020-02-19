--
-- Table structure for table merchandise
--
CREATE TYPE unit_type as ENUM('szt.', 'mb.');

DROP TABLE IF EXISTS merchandise;
CREATE TABLE merchandise (
  id SERIAL PRIMARY KEY,
  code text NOT NULL DEFAULT '',
  description text,
  unit unit_type DEFAULT NULL
);

DROP TABLE IF EXISTS price;
CREATE TABLE price (
  merchandise_id INT NOT NULL,
  value decimal(8,2) DEFAULT NULL,
  validFrom date NOT NULL DEFAULT '1000-01-01',
  validTo date NOT NULL DEFAULT '9999-12-31',
  CONSTRAINT fk_price_merchandise FOREIGN KEY (merchandise_id) REFERENCES merchandise (id)
);

