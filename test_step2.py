from backend.core.relation_path_utils import find_shortest_path_db
from backend.core.family_relation import build_relation_steps, interpret_step_path
from backend.core.family_relation import analyze_direction_and_generation
from backend.presentation.relation_naming import present_relation
from backend.presentation.relation_naming import present_uncle_aunt
from backend.presentation.relation_naming import invert_relation

path = find_shortest_path_db(37, 11)
print("PATH:", path)

steps = build_relation_steps(path)
print("STEPS:", steps)

relation = interpret_step_path(steps)
print("RELATION:", relation)

info = analyze_direction_and_generation(['MOTHER', 'MOTHER', 'FATHER'])
print(info)

label = present_relation({
    "direction": "UP",
    "generation": 3,
    "side": "MATERNAL"
})

print("LABEL:", label)


info = {
    "direction": "UP",
    "generation": 3,
    "side": "MATERNAL"
}

print(present_relation(info, gender="male"))
print(present_relation(info, gender="male", is_spouse_side=True))

info = {
    "direction": "UP",
    "generation": 2,
    "side": "MATERNAL"
}

print(present_uncle_aunt(info, gender="male"))     # Cậu
print(present_uncle_aunt(info, gender="female"))   # Dì

tests = [
    "Cậu",
    "Dì",
    "Bác",
    "Ông cố ngoại",
    "Anh",
    "Em",
    "Cha",
]

for t in tests:
    print(t, "→", invert_relation(t))