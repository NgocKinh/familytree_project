from src.relations.relationship_finder import find_relationship_bidirectional
from presentation.relation_naming import present_relation

print("=== TEST SPOUSE ===")
print(find_relationship_bidirectional(7, 10))

print("=== TEST CHA CON ===")
print(find_relationship_bidirectional(5, 11))

print("=== TEST NAMING ===")
print(present_relation({"direction": "UP", "generation": 1}, gender="male"))
