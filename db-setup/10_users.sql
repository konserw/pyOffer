--
-- Table structure for table users
--

DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    user_id               SERIAL,
    name                  text    NOT NULL,
    mail                  text    NOT NULL,
    male                  BOOLEAN NOT NULL DEFAULT TRUE,
    phone                 TEXT             DEFAULT NULL,
    current_offer_number  int     NOT NULL DEFAULT '0',
    current_offer_date    date    NOT NULL DEFAULT '2018-01-01',
    char_for_offer_symbol char(1) NOT NULL DEFAULT '',
    business_symbol       char(1) NOT NULL DEFAULT 'I',
    PRIMARY KEY (user_id)
);

-- FUNCTION: public.get_new_offer_number(integer)

CREATE OR REPLACE FUNCTION public.get_new_offer_number(
    in_user_id integer DEFAULT 0)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
AS
$BODY$
DECLARE
    new_number integer;
    old_number integer;
    old_date   date;
BEGIN
    SELECT current_offer_number, current_offer_date
    INTO old_number, old_date
    FROM users
    where users.user_id = in_user_id;

    if extract(year from old_date) < extract(year from current_date) or extract(month from old_date) < extract(month from current_date) then
        new_number := 1;
    else
        new_number := old_number + 1;
    end if;

    update users
    set current_offer_date=current_date,
        current_offer_number=new_number
    where users.user_id = in_user_id;

    RETURN new_number;
END;
$BODY$;

ALTER FUNCTION public.get_new_offer_number(integer)
    OWNER TO postgres;
