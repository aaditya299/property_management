create table properties(
  property_id serial primary key,
  address varchar(100) not null,
  property_type varchar(100) not null,
  purchase_price numeric(10,2) not null check (purchase_price>=0) ,
  city varchar(100) not null
);
  
create table rentals(
  rental_id serial primary key,
  property_id int not null,
  monthly_rent numeric(10,2) check (monthly_rent >=0),
  status varchar(50) check (status in('Occupied','Vacant')),
  foreign key (property_id) references properties(property_id)
);
  
create table tenants(
  tenant_id serial primary key,
  rental_id int not null,
  tenant_name varchar(100) not null,
  payment_status varchar(50) not null check (payment_status in ('paid','late','unpaid')),
  foreign key(rental_id) references rentals(rental_id)
);

INSERT INTO properties (address, property_type, purchase_price, city) VALUES
('123 Broadway St', 'Apartment', 250000.00, 'New York'),
('456 Sunset Blvd', 'House', 600000.00, 'Los Angeles'),
('789 Michigan Ave', 'Commercial', 1200000.00, 'Chicago'),
('101 Queens Rd', 'Apartment', 180000.00, 'New York'),
('202 Hollywood Ln', 'Apartment', 320000.00, 'Los Angeles');

INSERT INTO rentals (property_id, monthly_rent, status) VALUES
(1, 2200.00, 'Occupied'),
(2, 4500.00, 'Occupied'),
(3, 9500.00, 'Occupied'),
(4, 0.00, 'Vacant'), 
(5, 2800.00, 'Occupied');

INSERT INTO tenants (rental_id, tenant_name, payment_status) VALUES
(1, 'John Doe', 'paid'),
(2, 'Jane Smith', 'late'),
(3, 'Acme Corp', 'paid'),
(5, 'Alice Brown', 'unpaid');