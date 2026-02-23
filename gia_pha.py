people = {
    "A": {
        "father": None,
        "mother": None,
        "spouse": "B",
        "gender": "M",
        "gen": 0
    },
    "B": {
        "father": None,
        "mother": None,
        "spouse": "A",
        "gender": "F",
        "gen": 0
    },
    "C": {
        "father": "A",
        "mother": "B",
        "spouse": None,
        "gender": "M",
        "gen": -1
    }
}
people["D"] = {
    "father": None,
    "mother": None,
    "spouse": None,
    "gender": "F",
    "gen": 0
}
people["E"] = {"father": None, "mother": None, "spouse": "F", "gender": "M", "gen": 1}
people["F"] = {"father": None, "mother": None, "spouse": "E", "gender": "F", "gen": 1}

people["A"]["father"] = "E"
people["A"]["mother"] = "F"
people["G"] = {"father": "E", "mother": "F", "spouse": None, "gender": "M", "gen": 0}
people["H"] = {"father": "E", "mother": "F", "spouse": None, "gender": "F", "gen": 0}
# A là cha của C
# G là anh của A (bác)
# H là em của A (chú)
people["G"]["gen"] = -1  # lớn tuổi hơn A
people["H"]["gen"] = 1   # nhỏ tuổi hơn A

def validate_people(people):
    errors = []

    for pid, p in people.items():
        father = p.get("father")
        mother = p.get("mother")
        spouse = p.get("spouse")

        # 1. Tự làm cha/mẹ chính mình
        if father == pid or mother == pid:
            errors.append(f"{pid} tự là cha/mẹ của chính mình")

        # 2. Cha và mẹ trùng nhau
        if father and mother and father == mother:
            errors.append(f"{pid} có cha và mẹ trùng nhau ({father})")

        # 3. Vợ/chồng không đối xứng
        if spouse:
            if spouse not in people:
                errors.append(f"{pid} có vợ/chồng ({spouse}) không tồn tại")
            else:
                if people[spouse].get("spouse") != pid:
                    errors.append(f"{pid} và {spouse} không khai báo vợ/chồng 2 chiều")

        # 4. Giới tính cha/mẹ sai
        if father and people.get(father, {}).get("gender") != "M":
            errors.append(f"{father} được khai là cha của {pid} nhưng không phải nam")

        if mother and people.get(mother, {}).get("gender") != "F":
            errors.append(f"{mother} được khai là mẹ của {pid} nhưng không phải nữ")

    return errors

def blood_code(A, B):
    a = people[A]
    b = people[B]

    if a.get("father") == b.get("father") and a.get("mother") == b.get("mother"):
        return 3   # cùng cha + mẹ
    if a.get("father") == b.get("father"):
        return 1   # cùng cha
    if a.get("mother") == b.get("mother"):
        return 2   # cùng mẹ
    return 0

def get_relation(A, B):
    # Vợ / chồng
    if people[A].get("spouse") == B:
        return "chồng" if people[A]["gender"] == "M" else "vợ"

    # Cha / mẹ
    if people[A].get("father") == B:
        return "cha"
    if people[A].get("mother") == B:
        return "mẹ"

    # Con
    if people[B].get("father") == A:
        return "con trai" if people[A]["gender"] == "M" else "con gái"
    if people[B].get("mother") == A:
        return "con trai" if people[A]["gender"] == "M" else "con gái"

    # Anh / chị / em ruột
    if blood_code(A, B) == 3 and people[A]["gen"] == people[B]["gen"]:
        if people[A]["gender"] == "M":
            return "anh/em trai"
        else:
            return "chị/em gái"

    # Ông / bà
    father = people[A].get("father")
    mother = people[A].get("mother")

    if father:
        if people[father].get("father") == B:
            return "ông"
        if people[father].get("mother") == B:
            return "bà"

    if mother:
        if people[mother].get("father") == B:
            return "ông"
        if people[mother].get("mother") == B:
            return "bà"

    # Cháu
    if people[B].get("father"):
        fa = people[B]["father"]
        if people.get(fa) and people[fa].get("father") == A:
            return "cháu"
        if people.get(fa) and people[fa].get("mother") == A:
            return "cháu"

    if people[B].get("mother"):
        mo = people[B]["mother"]
        if people.get(mo) and people[mo].get("father") == A:
            return "cháu"
        if people.get(mo) and people[mo].get("mother") == A:
            return "cháu"

    # Bác / chú / cô (anh chị em của cha)
    father = people[A].get("father")
    if father:
        if blood_code(father, B) == 3:
            if people[B]["gender"] == "M":
                if people[B]["gen"] < people[father]["gen"]:
                    return "bác"
                else:
                    return "chú"
            else:
                return "cô"
REVERSE_MAP = {
    "bác": "cháu",
    "chú": "cháu",
    "cô": "cháu",
    "dì": "cháu",
    "cậu": "cháu",
    "ông": "cháu",
    "bà": "cháu",
}

def get_relation_bidirectional(A, B):
    r = get_relation(A, B)
    if r:
        return r

    r_rev = get_relation(B, A)
    if r_rev and r_rev in REVERSE_MAP:
        return REVERSE_MAP[r_rev]

def relation_sentence(A, B):
    r = get_relation_bidirectional(A, B)

    if r is None:
        return f"{A} và {B} không có quan hệ trực tiếp"

    return f"{A} là {r} của {B}"

    
    return None
