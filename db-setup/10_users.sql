--
-- Table structure for table users
--

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id SERIAL,
  name text NOT NULL,
  mail text NOT NULL,
  male BOOLEAN NOT NULL DEFAULT TRUE,
  phone TEXT DEFAULT NULL,
  current_offer_number int NOT NULL DEFAULT '0',
  current_offer_date date NOT NULL DEFAULT '2018-01-01',
  char_for_offer_symbol char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (id)
);

-- FUNCTION: public.get_new_offer_number(integer)

CREATE OR REPLACE FUNCTION public.get_new_offer_number(
	uid integer DEFAULT 0)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE

AS $BODY$DECLARE
	new_number integer;
	old_number integer;
    old_date date;
BEGIN
    SELECT current_offer_number, current_offer_date
    INTO old_number, old_date
    FROM users
    where users.id = uid;

    if extract(year from old_date) < extract(year from current_date) or extract(month from old_date) < extract(month from current_date) then
		new_number := 1;
		update users
        set current_offer_date=current_date, current_offer_number=new_number
        where users.id = uid;
    else
		new_number := old_number+1;
		update users
        set current_offer_number = new_number
        where users.id = uid;
	end if;

RETURN new_number;
END;$BODY$;

ALTER FUNCTION public.get_new_offer_number(integer)
    OWNER TO postgres;
