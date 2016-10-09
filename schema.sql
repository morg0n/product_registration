CREATE SCHEMA `product_registration` ;

CREATE TABLE `product_registration`.`product` (
  `uuid` CHAR(36) NOT NULL,
  `email` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`uuid`),
  UNIQUE INDEX `uuid_UNIQUE` (`uuid` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC));
