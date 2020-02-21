--
-- Table structure for table saved_offers
--

DROP TABLE IF EXISTS saved_offers;
CREATE TABLE saved_offers (
  id SERIAL,
  offer_symbol TEXT NOT NULL,
  user_id int NOT NULL,
  customer_id int DEFAULT NULL,
  offer_date date NOT NULL,
  inquiry_date date DEFAULT NULL,
  inquiry_number text,
  terms_delivery int DEFAULT NULL,
  terms_delivery_date int DEFAULT NULL,
  terms_billing int DEFAULT NULL,
  terms_offer int DEFAULT NULL,
  remarks text NOT NULL,
  print_number BOOLEAN NOT NULL DEFAULT '1',
  print_details BOOLEAN NOT NULL DEFAULT '1',
  print_list_price BOOLEAN NOT NULL DEFAULT '1',
  print_discount BOOLEAN NOT NULL DEFAULT '1',
  print_price BOOLEAN NOT NULL DEFAULT '1',
  PRIMARY KEY (id),
  CONSTRAINT fk_saved_offers_billing FOREIGN KEY (terms_billing) REFERENCES terms_billing (id),
  CONSTRAINT fk_saved_offers_customer FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
  CONSTRAINT fk_saved_offers_delivery FOREIGN KEY (terms_delivery) REFERENCES terms_delivery (id),
  CONSTRAINT fk_saved_offers_deliveryDate FOREIGN KEY (terms_delivery_date) REFERENCES terms_delivery_date (id),
  CONSTRAINT fk_saved_offers_offer FOREIGN KEY (terms_offer) REFERENCES terms_offer (id),
  CONSTRAINT fk_saved_offers_user FOREIGN KEY (user_id) REFERENCES users (id)
);
