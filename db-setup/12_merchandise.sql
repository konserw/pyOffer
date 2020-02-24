CREATE TYPE unit_type as ENUM('szt.', 'mb.');

DROP TABLE IF EXISTS merchandise;
CREATE TABLE merchandise (
  merchandise_id SERIAL PRIMARY KEY,
  code text NOT NULL DEFAULT '',
  description text,
  unit unit_type DEFAULT NULL
);

DROP TABLE IF EXISTS price;
CREATE TABLE price (
  merchandise_id INT NOT NULL,
  value decimal(8,2) DEFAULT NULL,
  valid_from date NOT NULL DEFAULT '1000-01-01',
  valid_to date NOT NULL DEFAULT '9999-12-31',
  CONSTRAINT fk_price_merchandise FOREIGN KEY (merchandise_id) REFERENCES merchandise (merchandise_id)
);


CREATE OR REPLACE VIEW merchandise_view AS
select
  merchandise.merchandise_id AS merchandise_id,
  merchandise.code AS code,
  merchandise.description AS description,
  merchandise.unit AS unit,
  price.value AS listing_price
FROM merchandise natural join price
WHERE CURRENT_DATE BETWEEN price.valid_from AND price.valid_to;

