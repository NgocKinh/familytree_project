# test_core_path.py
from backend.core.relation_path_utils import find_shortest_path_db

# THAY A, B bằng ID thật trong DB của bạn
A = 37
B = 11 

path = find_shortest_path_db(A, B)
print("PATH:", path)



