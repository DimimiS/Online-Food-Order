CREATE TABLE IF NOT EXISTS Customer (
	
	-- accountId,first_name,last_name,email,address,address_number,floor

	accountId VARCHAR(255) ,
	first_name VARCHAR(255),
	last_name VARCHAR(255),
	email VARCHAR(255),
	-- phone VARCHAR(255),
	address VARCHAR(255),
	address_number integer,
	floor integer,
	password VARCHAR(255),
	salt VARCHAR(255),
	PRIMARY KEY (email)
);

CREATE TABLE IF NOT EXISTS Store (
	storeId integer,
	workHours VARCHAR(255),
	location VARCHAR(255),
	PRIMARY KEY (storeId)
);

CREATE TABLE IF NOT EXISTS Category (
	name VARCHAR(255),
	PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS Delivery (
	AFM integer,
	availability boolean,
	PRIMARY KEY (AFM)
);

CREATE TABLE IF NOT EXISTS CustomerSupport (
	AFM integer,
	availability boolean,
	PRIMARY KEY (AFM)
);

CREATE TABLE IF NOT EXISTS Belongs (
	categoryName VARCHAR(255),
	dishName VARCHAR(255),
	FOREIGN KEY (categoryName) REFERENCES Category (name)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY (dishName) REFERENCES Dish (dishName)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Includes (
	orderId integer,
	storeId integer,
	dishName VARCHAR(255),
	quantity integer,
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
	storeId integer,
	email VARCHAR(255),
	FOREIGN KEY (storeId) REFERENCES Store (storeId)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY (email) REFERENCES Customer (email)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Dish (
	dishName VARCHAR(255),
	storeId integer,
	availability boolean,
	price decimal,
	PRIMARY KEY (dishName, storeId),
	FOREIGN KEY (storeId) REFERENCES Store (storeId)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS OrderT (
	orderId integer,
	comment text,
	customerEmail VARCHAR(255),
	deliveryAFM integer,
	orderTime timestamp,
	orderDate date,
	rateTime timestamp,
	rateText text,
	rateScore decimal,
	pickupTime timestamp,
	exp_deliveryTime timestamp,
	deliveryTime timestamp,
	address VARCHAR(255),
	PRIMARY KEY (orderId),
	FOREIGN KEY (customerEmail) REFERENCES Customer (email)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY (deliveryAFM) REFERENCES Delivery (AFM)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Change_request (
	requestId integer,
	orderId integer,
	customerEmail VARCHAR(255),
	AFM integer,
	time timestamp,
	payment VARCHAR(255),
	PRIMARY KEY (requestId),
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

