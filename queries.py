from sqlalchemy import select, func, desc, asc
from database import engine
from models import Customer, StoreSales

with engine.connect() as connection:

    # Q1. Display all columns from the first 10 customers
    query1 = select(Customer).limit(10)
    print("\nQ1. First 10 Customers:")
    for row in connection.execute(query1):
        print(row)

    # Q2. Display customer ID, first name, last name and email
    query2 = select(
        Customer.c_customer_id,
        Customer.c_first_name,
        Customer.c_last_name,
        Customer.c_email_address
    )
    print("\nQ2. Customer Details:")
    for row in connection.execute(query2).fetchmany(10):
        print(row)

    # Q3. Display customers born after 1980
    query3 = select(Customer).where(Customer.c_birth_year > 1980)
    print("\nQ3. Customers Born After 1980:")
    for row in connection.execute(query3).fetchmany(10):
        print(row)

    # Q4. Display preferred customers
    query4 = select(Customer).where(
        Customer.c_preferred_cust_flag == "Y"
    )
    print("\nQ4. Preferred Customers:")
    for row in connection.execute(query4).fetchmany(10):
        print(row)

    # Q5. Display the first 10 customers ordered by last name ascending
    query5 = (
        select(Customer.c_last_name)
        .order_by(asc(Customer.c_last_name))
        .limit(10)
    )
    print("\nQ5. Customers Ordered by Last Name:")
    for row in connection.execute(query5):
        print(row)

    # Q6. Display distinct birth countries
    query6 = select(Customer.c_birth_country).distinct()
    print("\nQ6. Distinct Birth Countries:")
    for row in connection.execute(query6):
        print(row)

    # Q7. Count the total number of customers
    query7 = select(func.count()).select_from(Customer)
    print("\nQ7. Total Customers:")
    print(connection.execute(query7).scalar_one())

    # Q8. Find minimum and maximum customer birth years
    query8 = select(
        func.min(Customer.c_birth_year).label("min_birth_year"),
        func.max(Customer.c_birth_year).label("max_birth_year")
    )
    print("\nQ8. Minimum and Maximum Birth Year:")
    print(connection.execute(query8).one())

    # Q9. Display 10 store sales records with price greater than 100
    query9 = (
        select(StoreSales)
        .where(StoreSales.ss_ext_sales_price > 100)
        .limit(10)
    )
    print("\nQ9. Store Sales Above 100:")
    for row in connection.execute(query9):
        print(row)

    # Q10. Calculate total extended sales price
    query10 = select(
        func.sum(StoreSales.ss_ext_sales_price)
        .label("total_extended_sales_price")
    )
    print("\nQ10. Total Extended Sales Price:")
    print(connection.execute(query10).scalar_one())

    # Q11. Display customer first names starting with A
    query11 = select(Customer.c_first_name).where(
        Customer.c_first_name.like("A%")
    )
    print("\nQ11. First Names Starting With A:")
    for row in connection.execute(query11).fetchmany(10):
        print(row)

    # Q12. Display customers born between 1980 and 1990
    query12 = select(Customer).where(
        Customer.c_birth_year.between(1980, 1990)
    )
    print("\nQ12. Customers Born Between 1980 and 1990:")
    for row in connection.execute(query12).fetchmany(10):
        print(row)

    # Q13. Display customers from the US or Canada
    query13 = select(Customer).where(
        Customer.c_birth_country.in_(["UNITED STATES", "CANADA"])
    )
    print("\nQ13. Customers From US or Canada:")
    for row in connection.execute(query13).fetchmany(10):
        print(row)

    # Q14. Display the 10 highest store sales prices
    query14 = (
        select(StoreSales)
        .order_by(desc(StoreSales.ss_ext_sales_price))
        .limit(10)
    )
    print("\nQ14. Top 10 Store Sales:")
    for row in connection.execute(query14):
        print(row)

    # Q15. Calculate average extended sales price
    query15 = select(
        func.avg(StoreSales.ss_ext_sales_price)
        .label("avg_extended_sales_price")
    )
    print("\nQ15. Average Extended Sales Price:")
    print(connection.execute(query15).scalar_one())