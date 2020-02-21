INSERT INTO public.companies(
    short_name, full_name, address)
	VALUES ('PolImpEx', 'P.H.U. PolImpEx Sp. z o.o.', 'Polna 1a/2\n41-300 Dąbrowa Górnicza');

INSERT INTO public.customers(
	title, first_name, last_name, company_id)
	VALUES ('Pan', 'Jan', 'Kowalski', 1), ('Pani', 'Jane', 'Doe', 1);
