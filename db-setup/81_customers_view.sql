
CREATE OR REPLACE VIEW customers_view AS
select
  customers.id AS customer_id,
  customers.short_name AS short_name,
  customers.full_name AS full_name,
  customers.title AS title,
  customers.first_name AS first_name,
  customers.last_name AS last_name,
  addresses.address AS address
from customers natural join addresses;
