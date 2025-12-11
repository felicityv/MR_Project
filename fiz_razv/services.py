from .models import FizicRazvit

def calculate_age_key(age_years, age_months):
    if 1 <= age_months <= 3:
        age_key = age_years + 0.3
    elif 4 <= age_months <= 6:
        age_key = age_years + 0.6
    elif 7 <= age_months <= 9:
        age_key = age_years + 0.9
    elif 10 <= age_months <= 11:
        age_key = age_years + 1.0
    else:
        age_key = float(age_years)
    return age_key

def analyze_centile(parametr, model_class, age_key, gender): 
    centile_row = model_class.objects.filter(gender=gender, age=age_key)
    print(centile_row)
    ME = float(centile_row.ME)
    SD = float(centile_row.SD or 1.0)
    SDS = round((parametr - ME) / SD, 2)

    if parametr < centile_row.p3:
        corridor = "ниже 3"
    elif centile_row.p3 <= parametr < centile_row.p10:
        corridor = "3-10"
    elif centile_row.p10 <= parametr < centile_row.p25:
        corridor = "10-25"
    elif centile_row.p25 <= parametr <= centile_row.p75:
        corridor = "25-75"
    elif centile_row.p75 < parametr <= centile_row.p90:
        corridor = "75-90"
    elif centile_row.p90 < parametr <= centile_row.p97:
        corridor = "90-97"
    else:
        corridor = "выше 97"

    return SDS, corridor


# def analyze_centile(name, parametr, centiles, age_key, gender=None, resultat=True):
#     def calculate_age_key(age_years, age_months):
#         if 1 <= age_months <= 3:
#             age_key = age_years + 0.3
#         elif 4 <= age_months <= 6:
#             age_key = age_years + 0.6
#         elif 7 <= age_months <= 9:
#             age_key = age_years + 0.9
#         elif 10 <= age_months <= 11:
#             age_key = age_years + 1.0
#         else:
#             age_key = float(age_years)
#         return age_key

#     for centile_row in centiles:
#         if float(centile_row['age']) == float(age_key):
#             p3 = float(centile_row['p3'])
#             p10 = float(centile_row['p10'])
#             p25 = float(centile_row['p25'])
#             p75 = float(centile_row['p75'])
#             p90 = float(centile_row['p90'])
#             p97 = float(centile_row['p97'])
#             ME = float(centile_row.get('ME', 0))
#             SD = float(centile_row.get('SD', 1)) or 1.0
#             SDS = round((parametr - ME) / SD, 2)

#             if parametr < p3:
#                 corridor = "ниже 3"
#             elif p3 <= parametr < p10:
#                 corridor = "3-10"
#             elif p10 <= parametr < p25:
#                 corridor = "10-25"
#             elif p25 <= parametr <= p75:
#                 corridor = "25-75"
#             elif p75 < parametr <= p90:
#                 corridor = "75-90"
#             elif p90 < parametr <= p97:
#                 corridor = "90-97"
#             else:
#                 corridor = "выше 97"
#             if resultat:
#                 if corridor in ("ниже 3", "выше 97"):
#                     print(f"{parametr} {name} в центильном коридоре {corridor} перцентиля, SDS = {SDS}.")
#                 else:
#                     print(f"{parametr} {name} в {corridor}-м центильном коридоре, SDS = {SDS}.")
#             return SDS, corridor

fiz_razvitie = {
    ("ниже 3", "ниже 3"):("ОН", "Г"),
    ("ниже 3", "3-10"):("ОН", "ДГ"),
    ("ниже 3", "10-25"):("Н", "РДГ"),
    ("ниже 3", "25-75"):("БОВ", "РДГ"),
    ("ниже 3", "75-90"):("БОВ", "РДГ"),
    ("ниже 3", "90-97"):("БОВ", "РДГ"),
    ("ниже 3", "выше 97"):("БОВ", "РДГ"),
    ("3-10", "ниже 3"):("ОН", "ДГ"),
    ("3-10", "3-10"):("Н", "Г"),
    ("3-10", "10-25"):("Н", "ДГ"),
    ("3-10", "25-75"):("БОВ", "РДГ"),
    ("3-10", "75-90"):("БОВ", "РДГ"),
    ("3-10", "90-97"): ("БОВ", "РДГ"),
    ("3-10", "выше 97"):("БОВ", "РДГ"),

    ("10-25", "ниже 3"):("ОН", "РДГ"),
    ("10-25", "3-10"):("Н", "ДГ"),
    ("10-25", "10-25"):("НС", "Г"),
    ("10-25", "25-75"):("НС", "ДГ"),
    ("10-25", "75-90"):("БОВ", "РДГ"),
    ("10-25", "90-97"):("БОВ", "РДГ"),
    ("10-25", "выше 97"):("БОВ", "РДГ"),

    ("25-75", "ниже 3"):("Н", "РДГ"),
    ("25-75", "3-10"):("Н", "РДГ"),
    ("25-75", "10-25"):("НС", "ДГ"),
    ("25-75", "25-75"):("С", "Г"),
    ("25-75", "75-90"):("ВС", "ДГ"),
    ("25-75", "90-97"):("БОВ", "РДГ"),
    ("25-75", "выше 97"):("БОВ", "РДГ"),

    ("75-90", "ниже 3"):("БОВ", "РДГ"),
    ("75-90", "3-10"):("БОВ", "РДГ"),
    ("75-90", "10-25"):("БОВ", "РДГ"),
    ("75-90", "25-75"):("ВС", "ДГ"),
    ("75-90", "75-90"):("ВС", "Г"),
    ("75-90", "90-97"):("В", "ДГ"),
    ("75-90", "выше 97"):("В", "РДГ"),

    ("90-97", "ниже 3"):("БОВ", "РДГ"),
    ("90-97", "3-10"):("БОВ", "РДГ"),
    ("90-97", "10-25"):("БОВ", "РДГ"),
    ("90-97", "25-75"):("БОВ", "РДГ"),
    ("90-97", "75-90"):("В", "ДГ"),
    ("90-97", "90-97"):("В", "Г"),
    ("90-97", "выше 97"):("ОВ", "ДГ"),

    ("выше 97", "ниже 3"):("БОВ", "РДГ"),
    ("выше 97", "3-10"):("БОВ", "РДГ"),
    ("выше 97", "10-25"):("БОВ", "РДГ"),
    ("выше 97", "25-75"):("БОВ", "РДГ"),
    ("выше 97", "75-90"):("В", "РДГ"),
    ("выше 97", "90-97"):("ОВ", "ДГ"),
    ("выше 97", "выше 97"):("ОВ", "Г")
}


def fizrazvitie(rost_corridor, ves_corridor):
    poiskfizrazvitie = fiz_razvitie.get((rost_corridor, ves_corridor))
    stepen_poiskfizrazvitie, garmon_poiskfizrazvitie = poiskfizrazvitie
    stepen = FizicRazvit.STEPEN_CHOICES[stepen_poiskfizrazvitie]
    garmon = FizicRazvit.GARMON_CHOICES[garmon_poiskfizrazvitie]
    return f"Физическое развитие: {stepen}, {garmon}"



