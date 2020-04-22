DROP TABLE IF EXISTS customers;
CREATE TABLE customers
(
    customer_id SERIAL PRIMARY KEY,
    title       text NOT NULL,
    first_name  text NOT NULL,
    last_name   text NOT NULL,
    company_name  text NOT NULL,
    address    text
);
