import pytest
from database import engine
@pytest.fixture   #for reusable test fixture
def connection():
    with engine.connect() as conn: 
        yield conn     #provides connection to the test