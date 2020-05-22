CREATE TYPE unit_type as ENUM ('pc.', 'm');

DROP TABLE IF EXISTS merchandise;
CREATE TABLE merchandise
(
    merchandise_id SERIAL PRIMARY KEY,
    code           text NOT NULL DEFAULT '',
    description    text,
    unit           unit_type     DEFAULT NULL,
    discount_group text          DEFAULT NULL
);

DROP TABLE IF EXISTS price;
CREATE TABLE price
(
    merchandise_id INT  NOT NULL,
    value          decimal(8, 2) DEFAULT NULL,
    valid_from     date NOT NULL DEFAULT '1000-01-01',
    valid_to       date NOT NULL DEFAULT '9999-12-31',
    CONSTRAINT fk_price_merchandise FOREIGN KEY (merchandise_id) REFERENCES merchandise (merchandise_id)
);


-- FUNCTION: public.merchandise_view(date)
-- DROP FUNCTION public.merchandise_view(date);

CREATE OR REPLACE FUNCTION public.merchandise_view(
	taget_date date DEFAULT current_date
	)
    RETURNS TABLE(merchandise_id integer, code text, description text, unit unit_type, discount_group text, list_price numeric)
    LANGUAGE 'sql'

    COST 100
    VOLATILE

AS $BODY$
select merchandise.merchandise_id AS merchandise_id,
       merchandise.code           AS code,
       merchandise.description    AS description,
       merchandise.unit           AS unit,
       merchandise.discount_group AS discount_group,
       price.value                AS list_price
FROM merchandise
         natural join price
WHERE $1 BETWEEN price.valid_from AND price.valid_to
$BODY$;

ALTER FUNCTION public.merchandise_view(date)
    OWNER TO postgres;
