
-- customer

INSERT INTO public.companies(
    short_name, full_name, address)
	VALUES ('PolImpEx', 'P.H.U. PolImpEx Sp. z o.o.', 'Polna 1a/2\n41-300 Dąbrowa Górnicza');

INSERT INTO public.customers(
	title, first_name, last_name, company_id)
	VALUES 
        ('Pan', 'Jan', 'Kowalski', 1),
        ('Pani', 'Jane', 'Doe', 1);


-- merchandise


INSERT INTO public.merchandise(
	code, description, unit)
	VALUES ('CODE123', 'some description', 'pc.');

INSERT INTO public.price(
	merchandise_id, value, valid_from, valid_to)
	VALUES (1, 19.99, '1000-01-01', '9999-12-31');
	
INSERT INTO public.merchandise(
	code, description, unit)
	VALUES ('CODE456', 'some other description', 'm');

INSERT INTO public.price(
	merchandise_id, value, valid_from, valid_to)
	VALUES (2, 4.49, '1000-01-01', '2015-12-31');

INSERT INTO public.price(
	merchandise_id, value, valid_from, valid_to)
	VALUES (2, 5.49, '2016-01-01', '9999-12-31');

-- users

INSERT INTO public.users(
	name, mail, male, phone, current_offer_number, current_offer_date, char_for_offer_symbol, business_symbol )
	VALUES ('Mark Salesman', 'mark@salesman.com', TRUE, '555 55 55', 22, '1999-01-01', 'M', 'I');

INSERT INTO public.users(
	name, mail, male, phone, current_offer_number, current_offer_date, char_for_offer_symbol, business_symbol )
	VALUES ('Agatha Salesman', 'agatha@salesman.com', FALSE, '555 55 50', 2322, '2020-03-28', 'A', 'X');

