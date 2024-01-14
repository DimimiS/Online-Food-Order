CREATE TABLE IF NOT EXISTS Customer (
	
	-- accountId,first_name,last_name,email,address,address_number,floor

	accountId 	INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	first_name 	VARCHAR(255),
	last_name 	VARCHAR(255),
	email 		VARCHAR(255) UNIQUE NOT NULL,
	-- phone VARCHAR(255),
	address 	VARCHAR(255),
	address_number 	INTEGER,
	floor 			INTEGER,
	password 	VARCHAR(255),
	salt 		VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Store (
	storeId 	INTEGER PRIMARY key AUTOINCREMENT NOT NULL,
	name 		VARCHAR(255),
	workHours 	VARCHAR(255),
	location 	VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Category (
	name VARCHAR(255),
	PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS Delivery (
	AFM INTEGER,
	availability boolean,
	PRIMARY KEY (AFM)
);

CREATE TABLE IF NOT EXISTS CustomerSupport (
	AFM INTEGER,
	availability boolean,
	PRIMARY KEY (AFM)
);

CREATE TABLE IF NOT EXISTS Belongs (
	category VARCHAR(255),
	dishName VARCHAR(255),
	FOREIGN KEY (category) REFERENCES Category (name)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY (dishName) REFERENCES Dish (dishName)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Includes (
	orderId 	INTEGER,
	storeId 	INTEGER,
	dishName 	VARCHAR(255),
	quantity 	INTEGER,
	FOREIGN KEY (orderId) REFERENCES OrderT (orderId)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY (storeId) REFERENCES Dish (storeId)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY (dishName) REFERENCES Dish (dishName)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Favourite (
	storeId INTEGER,
	email 	VARCHAR(255),
	FOREIGN KEY (storeId) REFERENCES Store (storeId)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY (email) REFERENCES Customer (email)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Dish (
	dishName 	VARCHAR(255),
	storeId 	INTEGER,
	availability 	boolean,
	price 			decimal,
	PRIMARY KEY (dishName, storeId),
	FOREIGN KEY (storeId) REFERENCES Store (storeId)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS OrderT (
	orderId 	INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	comment 	text,
	accountId 	INTEGER,
	deliveryAFM 	INTEGER,
	orderTime 	timestamp,
	orderDate 	date,
	rateTime 	timestamp,
	rateText 	text,
	rateScore 	decimal,
	pickupTime 	timestamp,
	exp_deliveryTime timestamp,
	deliveryTime	 timestamp,
	address 	VARCHAR(255),
	FOREIGN KEY (accountId) REFERENCES Customer (accountId)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY (deliveryAFM) REFERENCES Delivery (AFM)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Change_request (
	requestId 	INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	orderId 	INTEGER,
	customerEmail VARCHAR(255),
	AFM 	INTEGER,
	time 	timestamp,
	payment VARCHAR(255),
	FOREIGN KEY (orderId) REFERENCES OrderT (orderId)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY (customerEmail) REFERENCES Customer (email)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY (AFM) REFERENCES CustomerSupport (AFM)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

