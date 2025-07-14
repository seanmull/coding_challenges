from cut import get_columns

test_tsv = """Name	Age	Email
Alice	30	alice@example.com
Bob	25	bob@example.com
Charlie	35	charlie@example.com"""
test_csv = """Name,Age,Email
Alice,30,alice@example.com
Bob,25,bob@example.com
Charlie,35,charlie@example.com"""

test_tsv_result = """	Name
	Alice
	Bob
	Charlie"""

test_csv_result = """	Age
	30
	25
	35"""

def test_check_column_one():
    assert get_columns("1",None,test_tsv) == test_tsv_result

def test_check_column_two():
    assert get_columns("2",",",test_csv) == test_csv_result

