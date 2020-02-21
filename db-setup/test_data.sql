INSERT INTO public.addresses(
	address)
	VALUES ('Polna 1a/2\n41-300 Dąbrowa Górnicza');

INSERT INTO public.customers(
	short_name, full_name, title, first_name, last_name, address_id)
	VALUES ('PolImpEx', 'P.H.U. PolImpEx Sp. z o.o.', 'Pan', 'Jan', 'Kowalski', 1);
