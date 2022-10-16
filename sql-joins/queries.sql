-- write your queries here
-- Join the two tables so that every record appears --
SELECT * FROM owners FULL JOIN vehicles ON owners.id = vehicles.owner_id;

-- Count the number of cars for each owner --
SELECT owners.first_name, owners.last_name, COUNT(*) as count FROM owners JOIN vehicles 
ON owners.id = vehicles.owner_id GROUP BY owners.first_name,  owners.last_name ORDER BY owners.first_name ASC;

-- Count the number of cars for each over and display the average price for each --
SELECT owners.first_name, owners.last_name, CAST(AVG(vehicles.price) AS int) as average_price, COUNT(*) as count FROM owners JOIN vehicles 
ON owners.id = vehicles.owner_id GROUP BY owners.first_name, owners.last_name HAVING AVG(vehicles.price) > 10000 and COUNT(*) > 1 ORDER BY owners.first_name DESC;
