-- Problem Statement 1: Filtering Data
-- Your manager wants to see a list of all properties, but only those located in New York.
select * from properties where city='New York';

-- Problem Statement 2
-- "What is the total amount of money we spent purchasing properties in each city? I want to see the city name and the total purchase price side-by-side."
select city,sum(purchase_price) from properties group by city; 

--Problem Statement 3: The SQL JOIN 
-- Your manager wants a report showing the physical address of each property alongside its current monthly status ('Occupied' or 'Vacant').
select p.address, r.status from properties p inner join rentals r on p.property_id=r.property_id;

--Final Problem Statement: The Risk Assessment Report
-- Your manager needs a list of tenant names who have not paid their rent on time (late or unpaid), along with the address of the property they are living in.
select t.tenant_name,t.payment_status, p.address from properties p 
inner join rentals r on p.property_id=r.property_id
inner join tenants t on t.rental_id=r.rental_id
where t.payment_status!='paid';