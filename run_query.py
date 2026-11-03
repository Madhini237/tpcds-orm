from database import engine

from queries import (
    query1, query2, query3, query4, query5,
    query6, query7, query8, query9, query10,
    query11, query12, query13, query14, query15,
    query16, query17, query18, query19, query20,
    query21, query22, query23, query24, query25,
    query26, query27, query28, query29, query30,
    query31, query32, query33, query34, query35,
    query36, query37, query38, query39, query40,
    query41, query42, query43, query44, query45,
    query46, query47, query48, query49, query50,
    query51, query52, query53, query54
)

# Store all query functions in a list
queries = [
    query1, query2, query3, query4, query5,
    query6, query7, query8, query9, query10,
    query11, query12, query13, query14, query15,
    query16, query17, query18, query19, query20,
    query21, query22, query23, query24, query25,
    query26, query27, query28, query29, query30,
    query31, query32, query33, query34, query35,
    query36, query37, query38, query39, query40,
    query41, query42, query43, query44, query45,
    query46, query47, query48, query49, query50,
    query51, query52, query53, query54
]

# Establish database connection
with engine.connect() as connection:

    # Execute all queries one by one
    for i, query_function in enumerate(queries, start=1):  #returns both the index and the corresponding element from a list

        print(f"\n{'=' * 50}")
        print(f"QUERY {i} OUTPUT")

        try:
            result = query_function(connection)

            if result is None:
                print("No result returned.")

            elif hasattr(result, "all"):
                for row in result.all():
                    print(row)

            else:
                print(result)

        except Exception as e:
            print(f"Query {i} failed: {e}")