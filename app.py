import sqlite3

connection = sqlite3.connect("portfolio.db")
cursor = connection.cursor()

# drop tables for easy future tweaks/ add-ons
cursor.execute("DROP TABLE IF EXISTS tenants;")   # temporary code
cursor.execute("DROP TABLE IF EXISTS rentals;")   #tempporary code
cursor.execute("DROP TABLE IF EXISTS properties;")#temporary code  

#CREATING TABLES
cursor.execute(""" 
CREATE TABLE properties (
    property_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_type TEXT NOT NULL,
    purchase_price REAL NOT NULL CHECK(purchase_price >= 0),
    address TEXT NOT NULL,
    city TEXT NOT NULL
);
""")
print("Properties table created successfully")

cursor.execute("""
CREATE TABLE rentals (
    rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    monthly_rent REAL CHECK(monthly_rent >= 0),
    status TEXT CHECK(status IN ('Occupied', 'Vacant')),
    FOREIGN KEY (property_id) REFERENCES properties(property_id)
);
""")
print("Rentals table created successfully")

cursor.execute("""
CREATE TABLE tenants (
    tenant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rental_id INTEGER NOT NULL,
    tenant_name TEXT NOT NULL,
    payment_status TEXT NOT NULL CHECK(payment_status IN ('paid', 'late', 'unpaid')),
    FOREIGN KEY (rental_id) REFERENCES rentals(rental_id)
);
""")
print("Tenants table created successfully")
# connection.close()

# INSERTING TEMPORARY/SAMPLE DATA
cursor.execute("select count(*) from properties;")
if cursor.fetchone()[0]==0:
    print("database is empty. Inserting sample data. . .")
    cursor.executemany("""
    INSERT INTO properties (property_type, purchase_price, address, city)
    VALUES (?, ?, ?, ?);
    """, [
        ('Apartment', 250000.00, '123 Broadway St', 'New York'),
        ('House', 600000.00, '456 Sunset Blvd', 'Los Angeles'),
        ('Commercial', 1200000.00, '789 Michigan Ave', 'Chicago')
    ])

    cursor.executemany("""
    INSERT INTO rentals (property_id, monthly_rent, status)
    VALUES (?, ?, ?);
    """, [
        (1, 2200.00, 'Occupied'),
        (2, 4500.00, 'Occupied'),
        (3, 9500.00, 'Occupied')
    ])

    cursor.executemany("""
    INSERT INTO tenants (rental_id, tenant_name, payment_status)
    VALUES (?, ?, ?);
    """, [
        (1, 'John Doe', 'paid'),
        (2, 'Jane Smith', 'late'),
        (3, 'Acme Corp', 'paid')
    ])
    connection.commit()
    print("Sample data saved successfully!\n")
else:
    print("Database already contains data. Skipping insertion.\n")

# GENERATING REPORT 
while True:
    print("\n Real Estate Portfolio Management ")
    print("1. View Risk Assessment Report")
    print("2. View Financial Analytics Summary")
    print("3. Exit Add a New Property")
    print("4. Exit Application")
    choice=input("Enter your choice(1-4): ")
    if choice=="1":
        print("generating Risk Assessment report. . .\n")
        query="""
        select t.tenant_name, t.payment_status,p.address
        from properties p
        inner join rentals r on p.property_id=r.property_id
        inner join tenants t on  t.rental_id=r.rental_id 
        where t.payment_status!="paid";"""
        cursor.execute(query)
        risk_records=cursor.fetchall()
        if risk_records:
            for name, status, address in risk_records:
                print(f"ALERT: Tenant '{name}' is '{status}' at property: {address}\n")
        else:
            print("All accounts are up to date!\n")
    #connection.close()
    elif choice=='2':
        print("Generating financial Analytics Report. . .\n")
        cursor.execute("select sum(purchase_price) from properties;")
        total_value=cursor.fetchone()[0]
        cursor.execute("select sum(monthly_rent) from rentals where status='Occupied';")
        total_rent=cursor.fetchone()[0]
        print(f"Total Portfolio Value: ${total_value:,.2f}\n")
        print(f"Total Monthly revenue: ${total_rent:,.2f}\n")
    elif choice=='3':
        print("\nAdda  New poperty to Portfolio")
        p_type=input("Enter property type (Apartment/House/Commercial): ")
        try:
            p_price=float(input("Enter purchase price: $"))
        except ValueError:
            print("Invalid price!")
            continue
        p_address=input("Enter street address: ")
        p_city=input("Enter city: ")
        cursor.execute("""
            insert into properties (property_type, purchase_price, address, city)
            values (?,?,?,?);""",(p_type,p_price,p_address,p_city))
        connection.commit()
        print(f"Successfully added property at '{p_address}' to the database. ")
    elif choice=='4':
        print("Exiting application. GoodBye")
        break
    else:
        print("Invalid option! enter a number between 1 and 3.")

connection.close()
