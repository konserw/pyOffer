--
-- Table structure for table customers
--

DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  short_name text NOT NULL,
  full_name text NOT NULL,
  title text NOT NULL,
  first_name text NOT NULL,
  last_name text NOT NULL,
  address_id int NOT NULL,
  CONSTRAINT fk_customers_address FOREIGN KEY (address_id) REFERENCES addresses (id)
);

-- Dump completed on 2020-02-15 15:35:09
