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
if tenant_profile:
    tenant_id, name , pay_status, rent, r_status, address, city=tenant_profile
    while True:
        print(f"\nWelcome Home, {name}! (ID: {tenant_id})")
        print("="*45)
        print("1. View My Lease & Property Details")
        print("2. Check My Balance & Rent Status")
        print("3. Logout & Exit")
        print("="*45)
        choice=input("\nSelect an action(1-3): ").strip()
        
        if choice=='1':
            print("\nYour Lease Agreement Details: ")
            print(f"Property Address: {address},{city}")
            print(f"Unit Status:      {r_status}")
            print(f"Commited Rent:    ${rent:,.2f} / month")
            print("-"*40)
        elif choice=='2':
            print("\nCurrent Account Invoice Status:")
            if pay_status=='paid':
                print("Status: Paid in Full")
                print(f"Next Bill Amount: ${rent:,.2f}")
            elif pay_status=='late':
                print("Status: Overdue (Late fees may apply!)")
                print(f"Outstanding Balance Due: ${rent:,.2f}")
            else:
                print("Status: Unpaid")
                print(f"Outstanding Balance Due: ${rent:,.2f}")
            print("-" * 40)
        elif choice=='3':
            print("Logging out of the resident portal")
            break
        else :
            print("\nInvalid chhoice! Please enter a number between 1 and 3.")
connection.close()