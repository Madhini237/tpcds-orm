from sqlalchemy import (select, func, desc, asc, or_, and_, case, exists,
    union_all, Integer, extract, text, union, cast)
from sqlalchemy.orm import aliased
from models import Customer, StoreSales, DateDim, Item, Store

# Q1. Display all columns from the first 10 customers
def query1(connection):
    stmt = select(Customer).limit(10)
    return connection.execute(stmt).fetchall()

# Q2. Display customer ID, first name, last name and email
def query2(connection):
    stmt = select(Customer.c_customer_id,Customer.c_first_name,Customer.c_last_name,Customer.c_email_address)
    return connection.execute(stmt).fetchmany(10)

# Q3. Display customers born after 1980
def query3(connection):
    stmt = select(Customer).where(Customer.c_birth_year > 1980)
    return connection.execute(stmt).fetchmany(10)

# Q4. Display preferred customers
def query4(connection):
    stmt = select(Customer).where(Customer.c_preferred_cust_flag == "Y")
    return connection.execute(stmt).fetchmany(10)

# Q5. Display the first 10 customers ordered by last name ascending
def query5(connection):
    stmt = (select(Customer.c_last_name).order_by(asc(Customer.c_last_name)).limit(10))
    return connection.execute(stmt).fetchall()

# Q6. Display distinct birth countries
def query6(connection):
    stmt = select(Customer.c_birth_country).distinct()
    return connection.execute(stmt).fetchall()

# Q7. Count the total number of customers
def query7(connection):
    stmt = select(func.count()).select_from(Customer)
    return connection.execute(stmt).scalar_one()

# Q8. Find minimum and maximum customer birth years
def query8(connection):
    stmt = select(func.min(Customer.c_birth_year).label("min_birth_year"),
        func.max(Customer.c_birth_year).label("max_birth_year"))
    return connection.execute(stmt).one()

# Q9. Display 10 store sales records with price greater than 100
def query9(connection):
    stmt = (select(StoreSales).where(StoreSales.ss_ext_sales_price > 100).limit(10))
    return connection.execute(stmt).fetchall()

# Q10. Calculate total extended sales price
def query10(connection):
    stmt = select(func.sum(StoreSales.ss_ext_sales_price).label("total_extended_sales_price"))
    return connection.execute(stmt).scalar_one()

# Q11. Display customer first names starting with A
def query11(connection):
    stmt = select(Customer.c_first_name).where(Customer.c_first_name.like("A%"))
    return connection.execute(stmt).fetchmany(10)

# Q12. Display customers born between 1980 and 1990
def query12(connection):
    stmt = select(Customer).where(Customer.c_birth_year.between(1980, 1990))
    return connection.execute(stmt).fetchmany(10)

# Q13. Display customers from the US or Canada
def query13(connection):
    stmt = select(Customer).where(Customer.c_birth_country.in_(["UNITED STATES", "CANADA"]))
    return connection.execute(stmt).fetchmany(10)

# Q14. Display the 10 highest store sales prices
def query14(connection):
    stmt = (select(StoreSales).order_by(desc(StoreSales.ss_ext_sales_price)).limit(10))
    return connection.execute(stmt).fetchall()

# Q15. Calculate average extended sales price
def query15(connection):
    stmt = select(func.avg(StoreSales.ss_ext_sales_price).label("avg_extended_sales_price"))
    return connection.execute(stmt).scalar_one()


# Q16. Display customers whose birth year is above 1980 and whose preferred customer flag is Y
def query16(connection):
    stmt = select(Customer).where(
        and_(
            Customer.c_birth_year > 1980,
            Customer.c_preferred_cust_flag == "Y"))
    return connection.execute(stmt).fetchmany(10)

# Q17. Display customers whose first names do not start with A
def query17(connection):
    stmt = select(Customer.c_customer_id,Customer.c_first_name).where(Customer.c_first_name.not_like("A%"))
    return connection.execute(stmt).fetchmany(10)

# Q18. Display customers whose email address is NULL
def query18(connection):
    stmt = select(
        Customer.c_customer_id,Customer.c_first_name,Customer.c_email_address).where(Customer.c_email_address.is_(None))
    return connection.execute(stmt).fetchmany(10) 

# Q19. Display customers whose email address is NOT NULL
def query19(connection):
    stmt = select(
        Customer.c_customer_id,Customer.c_first_name,Customer.c_email_address).where(Customer.c_email_address.is_not(None))
    return connection.execute(stmt).fetchmany(10)

# Q20. Display customers using pagination (skip first 10, display next 10)
def query20(connection):
    stmt = (select(Customer).order_by(Customer.c_customer_id).limit(10).offset(10))
    return connection.execute(stmt).fetchall()

# Q21. Count customers grouped by birth year, showing groups with more than 100 customers
def query21(connection):
    stmt = (select(Customer.c_birth_year,func.count().label("total_customers"))
        .group_by(Customer.c_birth_year).having(func.count() > 100).order_by(Customer.c_birth_year))
    return connection.execute(stmt).fetchall()

# Q22. Calculate an illustrative 10% amount on each store sales price
def query22(connection):
    stmt = select(StoreSales.ss_ext_sales_price,(StoreSales.ss_ext_sales_price * 0.10).label("estimated_amount")
        ).where(StoreSales.ss_ext_sales_price.is_not(None)).limit(10)
    return connection.execute(stmt).fetchall()

# Q23. Categorize customers using CASE WHEN
def query23(connection):
    stmt = select(Customer.c_customer_id,Customer.c_birth_year,case(
            (Customer.c_birth_year < 1980, "Before 1980"),
            (Customer.c_birth_year <= 1990, "1980 to 1990"),
            else_="After 1990").label("birth_year_category")).where(Customer.c_birth_year.is_not(None))
    return connection.execute(stmt).fetchmany(10)

# Q24. Display customers who have store sales above 100
def query24(connection):
    stmt = select(Customer).where(Customer.c_customer_sk.in_(select(StoreSales.ss_customer_sk).where(
        StoreSales.ss_ext_sales_price > 100)))
    return connection.execute(stmt).fetchmany(10)

# Q25. Display customer IDs and their total store sales
def query25(connection):
    stmt = (select(Customer.c_customer_id,func.sum(StoreSales.ss_ext_sales_price).label("total_sales"))
        .join(StoreSales,Customer.c_customer_sk == StoreSales.ss_customer_sk)
        .group_by(Customer.c_customer_id).order_by(func.sum(StoreSales.ss_ext_sales_price).desc()).limit(10))
    return connection.execute(stmt).fetchall()

# Q26. Display customers who have never made store purchases
def query26(connection):
    stmt = select(Customer.c_customer_id).where(Customer.c_customer_sk.not_in(select(StoreSales.ss_customer_sk).where(
        StoreSales.ss_customer_sk.is_not(None)))).limit(10)
    return connection.execute(stmt).fetchall()

# Q27. Display all customers and their store purchases using LEFT JOIN
def query27(connection):
    stmt = (select(Customer.c_customer_id,StoreSales.ss_ticket_number)
        .select_from(Customer).outerjoin(StoreSales,Customer.c_customer_sk == StoreSales.ss_customer_sk).limit(10))
    return connection.execute(stmt).fetchall()

# Q28. Display customers whose purchase count is above the average purchase count per customer
def query28(connection):
    customer_counts = (select(func.count().label("purchase_count"))
        .select_from(StoreSales).where(StoreSales.ss_customer_sk.is_not(None))
        .group_by(StoreSales.ss_customer_sk).subquery())
    average_count = (select(func.avg(customer_counts.c.purchase_count)).scalar_subquery())
    stmt = (select(Customer.c_customer_id,func.count().label("purchase_count"))
        .join(StoreSales,Customer.c_customer_sk == StoreSales.ss_customer_sk)
        .group_by(Customer.c_customer_sk,Customer.c_customer_id).having(func.count() > average_count).limit(10))
    return connection.execute(stmt).fetchall()


# Q29. Display store sales records whose sales price is above that customer's average sales price
def query29(connection):
    inner_sales = aliased(StoreSales)
    average_customer_sales = (select(func.avg(inner_sales.ss_sales_price))
        .where(inner_sales.ss_customer_sk == StoreSales.ss_customer_sk).correlate(StoreSales).scalar_subquery())
    stmt = (select(StoreSales.ss_customer_sk,StoreSales.ss_ticket_number,StoreSales.ss_sales_price)
        .where(StoreSales.ss_customer_sk.is_not(None)).where(StoreSales.ss_sales_price > average_customer_sales).limit(10))
    return connection.execute(stmt).fetchall()

# Q30. Display customers who have made at least one store purchase using EXISTS
def query30(connection):
    purchase_exists = exists(select(1).select_from(StoreSales)
        .where(StoreSales.ss_customer_sk == Customer.c_customer_sk))
    stmt = select(Customer.c_customer_id).where(purchase_exists).limit(10)
    return connection.execute(stmt).fetchall()

# Q31. Display customers who have never made store purchases using NOT EXISTS
def query31(connection):
    purchase_exists = exists(
        select(1).select_from(StoreSales).where(StoreSales.ss_customer_sk == Customer.c_customer_sk))
    stmt = (select(Customer.c_customer_id).where(~purchase_exists).limit(10))

    return connection.execute(stmt).fetchall()


# Q32. Count high-value and low-value store sales using conditional aggregation
def query32(connection):
    stmt = select(func.count(case((StoreSales.ss_sales_price > 100, 1))).label("high_value_sales"),
        func.count(case((StoreSales.ss_sales_price <= 100, 1))).label("low_value_sales"))

    return connection.execute(stmt).fetchall()


# Q33. Display customers whose first names start with A
def query33(connection):
    stmt = (select(Customer.c_customer_id,Customer.c_first_name)
        .where(func.lower(Customer.c_first_name).like("a%")).limit(10))
    return connection.execute(stmt).fetchall()


# Q34. Display customers from Canada or the United States
def query34(connection):
    stmt = select(Customer).where(
        or_(
            Customer.c_birth_country == "CANADA",
            Customer.c_birth_country == "UNITED STATES"))
    return connection.execute(stmt).fetchmany(10)


# Q35. Display customers not born in 1980
def query35(connection):
    stmt = select(Customer).where(Customer.c_birth_year != 1980)
    return connection.execute(stmt).fetchmany(10)


# Q36. Display customers born after 1980 who are preferred customers
def query36(connection):
    stmt = select(Customer).where(
        and_(
            Customer.c_birth_year > 1980,
            Customer.c_preferred_cust_flag == "Y"))
    return connection.execute(stmt).fetchmany(10)


# Q37. Display customers whose first name ends with 'a'
def query37(connection):
    stmt = select(Customer).where(Customer.c_first_name.endswith("a"))
    return connection.execute(stmt).fetchmany(10)


# Q38. Display customers whose first name contains 'an'
def query38(connection):
    stmt = select(Customer).where(Customer.c_first_name.contains("an"))
    return connection.execute(stmt).fetchmany(10)


# Q39. Display customer names in uppercase
def query39(connection):
    stmt = select(Customer.c_customer_id,func.upper(Customer.c_first_name).label("uppercase_name"))
    return connection.execute(stmt).fetchmany(10)


# Q40. Display customers with the length of their first name
def query40(connection):
    stmt = select(Customer.c_customer_id,Customer.c_first_name,
        func.length(Customer.c_first_name).label("name_length"))
    return connection.execute(stmt).fetchmany(10)


# Q41. Display customer email addresses; show 'No Email' if NULL
def query41(connection):
    stmt = select(Customer.c_customer_id,func.coalesce(Customer.c_email_address,"No Email").label("email"))
    return connection.execute(stmt).fetchmany(10)

# Q42. Return NULL for birth year 2000; otherwise display the birth year
def query42(connection):
    stmt = select(Customer.c_customer_id,func.nullif(Customer.c_birth_year,2000).label("birth_year"))
    return connection.execute(stmt).fetchmany(10)

# Q43. Convert customer ID to an integer
def query43(connection):
    stmt = select(cast(Customer.c_customer_id,Integer).label("customer_id"))
    return connection.execute(stmt).fetchmany(10)

# Q44. Display dates from the years 2000 to 2005
def query44(connection):
    stmt = select(DateDim).where(DateDim.d_year.between(2000, 2005))
    return connection.execute(stmt).fetchmany(10)

# Q45. Display dates from March to June in the year 2000
def query45(connection):
    stmt = select(DateDim).where(DateDim.d_year == 2000,DateDim.d_moy.between(3, 6))
    return connection.execute(stmt).fetchmany(10)

# Q46. Extract the year from each date
def query46(connection):
    stmt = select(DateDim.d_date,extract("YEAR", DateDim.d_date).label("year"))
    return connection.execute(stmt).fetchmany(10)

# Q47. Display dates belonging to the year 2000
def query47(connection):
    stmt = select(DateDim.d_date).where(extract("YEAR", DateDim.d_date) == 2000)
    return connection.execute(stmt).fetchmany(10)

# Q48. Display the current date
def query48(connection):
    stmt = select(func.current_date().label("current_date"))
    return connection.execute(stmt).fetchall()

# Q49. Display the date and the date one day later
def query49(connection):
    stmt = select(DateDim.d_date,func.date_add(DateDim.d_date,text("INTERVAL 1 DAY")).label("next_date"))
    return connection.execute(stmt).fetchmany(10)


# Q50. Display total sales for each year
def query50(connection):
    stmt = (select(DateDim.d_year,
        func.sum(StoreSales.ss_ext_sales_price).label("total_sales")).select_from(StoreSales)
        .join(DateDim,StoreSales.ss_sold_date_sk == DateDim.d_date_sk
        ).group_by(DateDim.d_year).order_by(DateDim.d_year))
    return connection.execute(stmt).fetchall()

# Q51. Display total sales for each year and month
def query51(connection):
    stmt = (select(DateDim.d_year,DateDim.d_moy,
            func.sum(StoreSales.ss_ext_sales_price).label("total_sales")).select_from(StoreSales)
        .join(DateDim,StoreSales.ss_sold_date_sk == DateDim.d_date_sk)
        .group_by(DateDim.d_year,DateDim.d_moy).order_by(DateDim.d_year,DateDim.d_moy))
    return connection.execute(stmt).fetchmany(20)

# Q52. Display years where total sales exceed 1,00,000
def query52(connection):
    stmt = (select(DateDim.d_year,func.sum(StoreSales.ss_ext_sales_price).label("total_sales")).select_from(StoreSales)
        .join( DateDim,StoreSales.ss_sold_date_sk == DateDim.d_date_sk)
        .group_by(DateDim.d_year).having(func.sum(StoreSales.ss_ext_sales_price) > 100000).order_by(DateDim.d_year))
    return connection.execute(stmt).fetchall()


# Q53. Display customer IDs from Canada and the United States,retaining duplicates (UNION ALL)
def query53(connection):
    query53a = select(Customer.c_customer_id).where(Customer.c_birth_country == "CANADA")
    query53b = select(Customer.c_customer_id).where(Customer.c_birth_country == "UNITED STATES")
    stmt = union_all(query53a, query53b)
    return connection.execute(stmt).fetchmany(20)

# Q54. Display customer IDs from Canada and the United States,removing duplicates (UNION)
def query54(connection):
    query54a = select(Customer.c_customer_id).where(Customer.c_birth_country == "CANADA")
    query54b = select(Customer.c_customer_id).where(Customer.c_birth_country == "UNITED STATES")
    stmt = union(query54a, query54b)
    return connection.execute(stmt).fetchmany(20)