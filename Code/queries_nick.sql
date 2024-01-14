
-- Getting the working hours 
SELECT storeId, workHours from Store 
-- And then cross checking it by the day it is and the time it is in python
-- WHERE day = DAYOFWEEK(NOW()) AND workHours = HOUR(NOW())


-- --------------------------------

-- Getting the order based on an email 

Select 
OrderId, customerEmail
-- *
-- OrderID, OrderDate,orderTime
 from OrderT join Customer on Customer.email=OrderT.customerEmail
 
--  where Customer.email='?'
order by OrderDate DESC,OrderTime DESC


-- --------------------------------

-- All good 

-- Find restaurant menu

SELECT DISTINCT dishName 
FROM Store NATURAL JOIN Includes
WHERE storeId = ?

-- --------------------------------

-- Find restaurants based on categories

SELECT DISTINCT s.location
FROM Store as s, Includes as i,Belongs as b
WHERE s.storeId = i.storeId and i.dishName = b.dishName and b.category=?

-- --------------------------------

-- Find restaurants based on dish name

SELECT DISTINCT s.location
FROM Store as s, Includes as i
WHERE s.storeId = i.storeId and i.dishName = ?

-- --------------------------------

-- Find dishes based on categories

Select dishName
FROM Belongs
WHERE category= ?

-- --------------------------------

-- Find customer information

Select fname
FROM Customer
WHERE email= ?

-- --------------------------------

-- Find order change appeals

Select *
FROM Change_request
WHERE orderID=?

-- --------------------------------

-- Find order change from customer

Select *
FROM Change_request
WHERE customerEmail=?

-- --------------------------------

-- Find favourite restaurants

SELECT location
FROM Store NATURAL JOIN Favourite
WHERE email = ?

-- --------------------------------

-- Find what restaurants are close (Area Code)

SELECT storeId, location
FROM Store
WHERE ...

-- --------------------------------


Create an order (include score)
Create favourite restaurants
Create order change appeal

Update an order
Update favourite restaurants
Update customer information

Delete an order
Delete favourite restaurants
Delete customer information

