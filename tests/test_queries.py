import pytest

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
    query51, query52, query53, query54)


#Instead of writing separate test functions , put all the functions into a list
#can access each function from this list and execute it 

queries= [query1, query2, query3, query4, query5,
    query6, query7, query8, query9, query10,
    query11, query12, query13, query14, query15,
    query16, query17, query18, query19, query20,
    query21, query22, query23, query24, query25,
    query26, query27, query28, query29, query30,
    query31, query32, query33, query34, query35,
    query36, query37, query38, query39, query40,
    query41, query42, query43, query44, query45,
    query46, query47, query48, query49, query50,
    query51, query52, query53, query54]

#pytest.mark.parametrize - run one test function with multiple sets of inputs
@pytest.mark.parametrize("query_function",queries,  #parameter name , all queries
    ids=[f"query{i}" for i in range(1, 55)])
def test_query_execution(connection, query_function):
    result = query_function(connection)
    assert result is not None  #verify the query result is not none