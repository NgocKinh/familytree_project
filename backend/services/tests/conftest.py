import pytest
import mysql.connector

@pytest.fixture
def db():
    conn = mysql.connector.connect(
        host="localhost",
        user="test_user",
        password="Msand@167",
        database="family_test",
    )
    yield conn
    conn.close()
