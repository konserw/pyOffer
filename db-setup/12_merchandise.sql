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

-- FUNCTION: public.create_merchandise(text, text, unit_type, text, numeric(8,2))
-- DROP FUNCTION public.create_merchandise(text, text, unit_type, text, numeric(8,2))

CREATE OR REPLACE FUNCTION public.create_merchandise(
    in_code text,
    in_description text,
    in_unit unit_type DEFAULT 'pc.',
    in_discount_group text DEFAULT '',
	in_price numeric(8,2) DEFAULT 0
	)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE

AS $BODY$
declare
  l_id integer;
begin
  l_id := nextval('merchandise_merchandise_id_seq');
  INSERT INTO public.merchandise(
	merchandise_id, code, description, unit, discount_group)
	VALUES (l_id, in_code, in_description, in_unit, in_discount_group);

  INSERT INTO public.price(
	merchandise_id, value, valid_from, valid_to)
	VALUES (l_id, in_price, DEFAULt, DEFAULT);

  if exists(select merchandise_id from public.merchandise where merchandise_id = l_id) and exists(select merchandise_id from public.price where merchandise_id = l_id) then
  	return l_id;
  else
    return -1;
  end if;
end;$BODY$;

ALTER FUNCTION public.create_merchandise(text, text, unit_type, text, numeric(8,2))
    OWNER TO postgres;

-- FUNCTION: public.update_price(text, numeric(8,2))
-- DROP FUNCTION public.update_price(text, numeric(8,2))

CREATE OR REPLACE FUNCTION public.update_price(
    in_code text,
	in_price numeric(8,2) DEFAULT 0
	)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE

AS $BODY$
declare
  l_id integer;
begin
  SELECT merchandise_id into l_id from public.merchandise WHERE code = in_code;
  if l_id is null then
    return -1;
  end if;


  if exists(select merchandise_id from public.price where merchandise_id = l_id) then
    update public.price set valid_to = current_date where merchandise_id = l_id and valid_to = '9999-12-31';
  end if;

  INSERT INTO public.price(
	merchandise_id, value, valid_from, valid_to)
	VALUES (l_id, in_price, current_date, DEFAULT);

  return l_id;
end;$BODY$;

ALTER FUNCTION public.update_price(text, numeric(8,2))
    OWNER TO postgres;
