from sqlalchemy import select, func, desc, asc,or_, and_, case , exists, union_all
from database import engine
from sqlalchemy.orm import aliased
from models import Customer, StoreSales

with engine.connect() as connection:

    # Q1. Display all columns from the first 10 customers
    query1 = select(Customer).limit(10)
    print("\nQ1. First 10 Customers:")
    for row in connection.execute(query1):
        print(row)

    # Q2. Display customer ID, first name, last name and email
    query2 = select(Customer.c_customer_id,Customer.c_first_name,Customer.c_last_name,Customer.c_email_address)
    print("\nQ2. Customer Details:")
    for row in connection.execute(query2).fetchmany(10):
        print(row)

    # Q3. Display customers born after 1980
    query3 = select(Customer).where(Customer.c_birth_year > 1980)
    print("\nQ3. Customers Born After 1980:")
    for row in connection.execute(query3).fetchmany(10):
        print(row)

    # Q4. Display preferred customers
    query4 = select(Customer).where(Customer.c_preferred_cust_flag == "Y")
    print("\nQ4. Preferred Customers:")
    for row in connection.execute(query4).fetchmany(10):
        print(row)

    # Q5. Display the first 10 customers ordered by last name ascending
    query5 = (select(Customer.c_last_name).order_by(asc(Customer.c_last_name)).limit(10))
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
    query8 = select(func.min(Customer.c_birth_year).label("min_birth_year"),func.max(Customer.c_birth_year).label("max_birth_year"))
    print("\nQ8. Minimum and Maximum Birth Year:")
    print(connection.execute(query8).one())

    # Q9. Display 10 store sales records with price greater than 100
    query9 = (select(StoreSales).where(StoreSales.ss_ext_sales_price > 100).limit(10))
    print("\nQ9. Store Sales Above 100:")
    for row in connection.execute(query9):
        print(row)

    # Q10. Calculate total extended sales price
    query10 = select(func.sum(StoreSales.ss_ext_sales_price).label("total_extended_sales_price"))
    print("\nQ10. Total Extended Sales Price:")
    print(connection.execute(query10).scalar_one())

    # Q11. Display customer first names starting with A
    query11 = select(Customer.c_first_name).where(Customer.c_first_name.like("A%"))
    print("\nQ11. First Names Starting With A:")
    for row in connection.execute(query11).fetchmany(10):
        print(row)

    # Q12. Display customers born between 1980 and 1990
    query12 = select(Customer).where(Customer.c_birth_year.between(1980, 1990))
    print("\nQ12. Customers Born Between 1980 and 1990:")
    for row in connection.execute(query12).fetchmany(10):
        print(row)

    # Q13. Display customers from the US or Canada
    query13 = select(Customer).where(Customer.c_birth_country.in_(["UNITED STATES", "CANADA"]))
    print("\nQ13. Customers From US or Canada:")
    for row in connection.execute(query13).fetchmany(10):
        print(row)

    # Q14. Display the 10 highest store sales prices
    query14 = (select(StoreSales).order_by(desc(StoreSales.ss_ext_sales_price)).limit(10))
    print("\nQ14. Top 10 Store Sales:")
    for row in connection.execute(query14):
        print(row)

    # Q15. Calculate average extended sales price
    query15 = select(func.avg(StoreSales.ss_ext_sales_price).label("avg_extended_sales_price"))
    print("\nQ15. Average Extended Sales Price:")
    print(connection.execute(query15).scalar_one())


    # Q16. Display customers whose birth year is above 1980 and whose preferred customer flag is Y
    query16 = select(Customer).where(and_(Customer.c_birth_year > 1980,Customer.c_preferred_cust_flag == "Y"))
    print("\nQ16. Customers Matching Multiple Conditions:")
    for row in connection.execute(query16).fetchmany(10):
        print(row)

    # Q17. Display customers whose first names do not start with A
    query17 = select(Customer.c_customer_id,Customer.c_first_name).where(Customer.c_first_name.not_like("A%"))
    print("\nQ17. First Names Not Starting With A:")
    for row in connection.execute(query17).fetchmany(10):
        print(row)

    # Q18. Display customers whose email address is NULL
    query18 = select(Customer.c_customer_id,Customer.c_first_name,Customer.c_email_address).where(Customer.c_email_address.is_(None))
    print("\nQ18. Customers Without Email Addresses:")
    for row in connection.execute(query18).fetchmany(10):
        print(row) 

    # Q19. Display customers whose email address is NOT NULL
    query19 = select(Customer.c_customer_id,Customer.c_first_name,Customer.c_email_address).where(Customer.c_email_address.is_not(None))
    print("\nQ19. Customers With Email Addresses:")
    for row in connection.execute(query19).fetchmany(10):
        print(row)

    # Q20. Display customers using pagination (skip first 10, display next 10)
    query20 = (select(Customer).order_by(Customer.c_customer_id).limit(10).offset(10))
    print("\nQ20. Customers Using Pagination:")
    for row in connection.execute(query20):
        print(row)

    # Q21. Count customers grouped by birth year, showing groups with more than 100 customers
    query21 = (select(Customer.c_birth_year,func.count().label("total_customers")).group_by(Customer.c_birth_year)
              .having(func.count() > 100).order_by(Customer.c_birth_year))
    print("\nQ21. Birth Years With More Than 100 Customers:")
    for row in connection.execute(query21):
        print(row)

    # Q22. Calculate an illustrative 10% amount on each store sales price
    query22 = select(StoreSales.ss_ext_sales_price,(StoreSales.ss_ext_sales_price * 0.10).label("estimated_amount")).where(
                StoreSales.ss_ext_sales_price.is_not(None)).limit(10)
    print("\nQ22. Store Sales With Calculated 10% Amount:")
    for row in connection.execute(query22):
        print(row)

    # Q23. Categorize customers using CASE WHEN
    query23 = select(Customer.c_customer_id,Customer.c_birth_year,case((Customer.c_birth_year < 1980, "Before 1980"),
                (Customer.c_birth_year <= 1990, "1980 to 1990"),else_="After 1990").label("birth_year_category")).where(
                Customer.c_birth_year.is_not(None))
    print("\nQ23. Customer Birth Year Categories:")
    for row in connection.execute(query23).fetchmany(10):
        print(row)

    # Q24. Display customers who have store sales above 100
    query24 = select(Customer).where(Customer.c_customer_sk.in_(select(StoreSales.ss_customer_sk).where(StoreSales.ss_ext_sales_price > 100)))
    print("\nQ24. Customers With Store Sales Above 100:")
    for row in connection.execute(query24).fetchmany(10):
        print(row)

    # Q25. Display customer IDs and their total store sales
    query25 = (select(Customer.c_customer_id,func.sum(StoreSales.ss_ext_sales_price
        ).label("total_sales")).join(StoreSales,Customer.c_customer_sk == StoreSales.ss_customer_sk)
        .group_by(Customer.c_customer_id).order_by(func.sum(StoreSales.ss_ext_sales_price).desc()).limit(10))
    print("\nQ25. Top 10 Customers By Total Store Sales:")
    for row in connection.execute(query25):
        print(row)

    # Q26. Display customers who have never made store purchases
    query26 = select(Customer.c_customer_id).where(Customer.c_customer_sk.not_in(select(StoreSales.ss_customer_sk).where(
                StoreSales.ss_customer_sk.is_not(None)))).limit(10)
    print("\nQ26. Customers Without Store Purchases:")
    for row in connection.execute(query26):
        print(row)

    # Q27. Display all customers and their store purchases using LEFT JOIN
    query27 = (select(Customer.c_customer_id, StoreSales.ss_ticket_number).select_from(Customer)
        .outerjoin(StoreSales, Customer.c_customer_sk == StoreSales.ss_customer_sk).limit(10))
    print("\nQ27. Customers With Their Store Purchases:")
    for row in connection.execute(query27):
        print(row)

    # Q28. Display customers whose purchase count is above the average purchase count per customer
    customer_counts = (select(func.count().label("purchase_count")).select_from(StoreSales)
        .where(StoreSales.ss_customer_sk.is_not(None)).group_by(StoreSales.ss_customer_sk).subquery())
    average_count = select(func.avg(customer_counts.c.purchase_count)).scalar_subquery()
    query28 = (select(Customer.c_customer_id,func.count().label("purchase_count"))
        .join(StoreSales, Customer.c_customer_sk == StoreSales.ss_customer_sk)
        .group_by(Customer.c_customer_sk, Customer.c_customer_id).having(func.count() > average_count).limit(10))
    print("\nQ28. Customers With Above-Average Purchase Counts:")
    for row in connection.execute(query28):
        print(row)

    # Q29. Display store sales records whose sales price is above that customer's average sales price
    inner_sales = aliased(StoreSales)
    average_customer_sales = (select(func.avg(inner_sales.ss_sales_price)).where(inner_sales.ss_customer_sk == StoreSales.ss_customer_sk)
        .correlate(StoreSales).scalar_subquery())
    query29 = (select(StoreSales.ss_customer_sk,StoreSales.ss_ticket_number,StoreSales.ss_sales_price)
        .where(StoreSales.ss_customer_sk.is_not(None)).where(StoreSales.ss_sales_price > average_customer_sales).limit(10))
    print("\nQ29. Sales Above Each Customer's Average Sales Price:")
    for row in connection.execute(query29):
        print(row)

    # Q30. Display customers who have made at least one store purchase using EXISTS
    purchase_exists = exists(select(1).select_from(StoreSales).where(StoreSales.ss_customer_sk == Customer.c_customer_sk))
    query30 = select(Customer.c_customer_id).where(purchase_exists).limit(10)
    print("\nQ30. Customers Who Have Made Store Purchases:")
    for row in connection.execute(query30):
        print(row)

    # Q31. Display customers who have never made store purchases using NOT EXISTS
    query31 = select(Customer.c_customer_id).where(~purchase_exists).limit(10)
    print("\nQ31. Customers Who Have Never Made Store Purchases:")
    for row in connection.execute(query31):
        print(row)

    # Q32. Count high-value and low-value store sales using conditional aggregation
    query32 = select(func.count(case((StoreSales.ss_sales_price > 100, 1))).label("high_value_sales"),
        func.count(case((StoreSales.ss_sales_price <= 100, 1))).label("low_value_sales"))
    print("\nQ32. High-Value and Low-Value Sales Counts:")
    for row in connection.execute(query32):
        print(row)

    # Q33. Display customers whose first names start with A
    query33 = (select(Customer.c_customer_id, Customer.c_first_name).where(func.lower(Customer.c_first_name).like("a%")).limit(10))
    print("\nQ33. Customers Whose First Names Start With A:")
    for row in connection.execute(query33):
        print(row)

