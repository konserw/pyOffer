DROP TABLE IF EXISTS companies;
CREATE TABLE companies
(
    company_id SERIAL PRIMARY KEY,
    short_name text NOT NULL,
    full_name  text NOT NULL,
    address    text
);

DROP TABLE IF EXISTS customers;
CREATE TABLE customers
(
    customer_id SERIAL PRIMARY KEY,
    title       text NOT NULL,
    first_name  text NOT NULL,
    last_name   text NOT NULL,
    company_id  int  NOT NULL,
    CONSTRAINT fk_customers_companies FOREIGN KEY (company_id) REFERENCES companies (company_id)
);

CREATE OR REPLACE VIEW customers_view AS
select customers.customer_id AS customer_id,
       companies.short_name  AS short_name,
       companies.full_name   AS full_name,
       customers.title       AS title,
       customers.first_name  AS first_name,
       customers.last_name   AS last_name,
       companies.address     AS address
FROM customers
         natural join companies;

