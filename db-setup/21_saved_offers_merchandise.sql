DROP TABLE IF EXISTS saved_offers_merchandise;
CREATE TABLE saved_offers_merchandise (
  offer_id int NOT NULL,
  sequence_number int DEFAULT NULL,
  merchandise_id int NOT NULL,
  quantity real DEFAULT NULL,
  discount real DEFAULT NULL,
  CONSTRAINT fk_saved_offers_merchandise_merchandise FOREIGN KEY (merchandise_id) REFERENCES merchandise (id),
  CONSTRAINT fk_saved_offers_merchandise_offer FOREIGN KEY (offer_id) REFERENCES saved_offers (id) ON DELETE CASCADE ON UPDATE CASCADE
);

