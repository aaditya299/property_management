import sqlite3
connection=sqlite3.connect("portfolio.db")
cursor=connection.cursor()
def tenant_login():
    print("welcome to Resident Tenant Portal")
    print("-"*40)
    tenant_name=input("Enter your full name to login: ").strip()
    query="""
    select t.tenant_id,t.tenant_name,t.payment_status,r.monthly_rent,r.status,p.address,p.city
    from tenants t
    inner join rentals r on t.rental_id=r.rental_id
    inner join properties p on r.property_id=p.property_id
    where trim(t.tenant_name) like trim(?);"""
    cursor.execute(query,(tenant_name,))
    account=cursor.fetchone()
    if account:
        return account
    else:
        print("Error: No resident profile found matching that name.")
        return None
tenant_profile=tenant_login()