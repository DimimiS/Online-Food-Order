CREATE TABLE IF NOT EXISTS "Customer" (
	"email" string,
	"card" string,
	"fullName" string,
	"accountId" string,
	PRIMARY KEY ("email")
);

CREATE TABLE IF NOT EXISTS "Store" (
	"storeId" integer,
	"workHours" string,
	"location" string,
	PRIMARY KEY ("storeId")
);

CREATE TABLE IF NOT EXISTS "Category" (
	"name" string,
	PRIMARY KEY ("name")
);

CREATE TABLE IF NOT EXISTS "Delivery" (
	"AFM" integer,
	"availability" boolean,
	PRIMARY KEY ("AFM")
);

CREATE TABLE IF NOT EXISTS "Customer Support" (
	"AFM" integer,
	"availability" boolean,
	PRIMARY KEY ("AFM")
);

CREATE TABLE IF NOT EXISTS "Belongs" (
	"categoryName" string,
	"dishName" string,
	FOREIGN KEY ("name") REFERENCES "Category" ("name")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("dishName") REFERENCES "Dish" ("dishName")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "Includes" (
	"orderId" integer,
	"storeId" integer,
	"dishName" string,
	"quantity" integer,
	FOREIGN KEY ("orderId") REFERENCES "Order" ("orderId")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("storeId") REFERENCES "Dish" ("storeId")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("dishName") REFERENCES "Dish" ("dishName")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "Sets Favourite" (
	"storeId" integer,
	"email" string,
	FOREIGN KEY ("storeId") REFERENCES "Store" ("storeId")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("email") REFERENCES "Customer" ("email")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "Dish" (
	"dishName" string,
	"storeId" integer,
	"availability" boolean,
	"price" decimal,
	PRIMARY KEY ("dishName", "storeId"),
	FOREIGN KEY ("storeId") REFERENCES "Store" ("storeId")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "Order" (
	"orderId" integer,
	"comment" text,
	"customerEmail" string,
	"deliveryAFM" integer,
	"orderTime" timestamp,
	"orderDate" date,
	"rateTime" timestamp,
	"rateText" text,
	"rateScore" decimal,
	"pickupTime" timestamp,
	"exp_deliveryTime" timestamp,
	"deliveryTime" timestamp,
	"address" string,
	PRIMARY KEY ("orderId"),
	FOREIGN KEY ("customerEmail") REFERENCES "Customer" ("email")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("deliveryAFM") REFERENCES "Delivery" ("AFM")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "Change request" (
	"requestId" integer,
	"orderId" integer,
	"customerEmail" string,
	"AFM" integer,
	"time" timestamp,
	"payment" string,
	PRIMARY KEY ("requestId"),
	FOREIGN KEY ("orderId") REFERENCES "Order" ("orderId")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("customerEmail") REFERENCES "Customer" ("email")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("AFM") REFERENCES "Customer Support" ("AFM")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

