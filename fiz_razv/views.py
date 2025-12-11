from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .models import Narushenie
from .models import FizicRazvit
from datetime import date

# def normalize_date(date_str: str) -> datetime:
#     cleaned = re.sub(r"\D", ".", date_str)
#     cleaned = re.sub(r"\.+", ".", cleaned).strip(".")
#     return datetime.strptime(cleaned, "%d.%m.%Y")

def calculate_age() -> tuple[int, int]:
    data_ras = models.DateField(default=date.today)
    if days < 0:
        months -= 1
    if months < 0:
        years -= 1
        months += 12
    return years, months


def narushenia(SDSrost, SDSves, SDSimt, age_years):
    if SDSrost <= -2:
        # print(f"Низкорослость или хроническая белково-энергетическая недостаточность, умеренной степени (рост = {SDSrost} SDS)")
        # return
        return Narushenie.objects.get_or_create(type_narushenia="ХБЭН")
    
    elif SDSrost >= 2:
        # print(f"Высокорослость (рост = {SDSrost} SDS).")
        # return
        return Narushenie.objects.get_or_create(type_narushenia="Высокорослость")
    
    if age_years < 5:
        if SDSves >= 3 or SDSimt >= 3:
            # print(f"Ожирение (индекс массы тела = {SDSimt} SDS, вес = {SDSves} SDS).")
            # return
            return Narushenie.objects.get_or_create(type_narushenia="Ожирение")
        
        if SDSves >= 2 or SDSimt >= 2:
            # print(f"Избыток массы тела (индекс массы тела = {SDSimt} SDS, вес = {SDSves} SDS).).")
            # return
            return Narushenie.objects.get_or_create(type_narushenia="Избыток массы тела")
        
    else:
        if SDSimt > 2:
            # print(f"Ожирение (индекс массы тела = {SDSimt} SDS).")
            # return
            return Narushenie.objects.get_or_create(type_narushenia="Ожирение")
        
        if SDSimt > 1:
            # print(f"Избыток массы тела (индекс массы тела = {SDSimt} SDS).")
            # return
            return Narushenie.objects.get_or_create(type_narushenia="Избыток массы тела")
                    
    if age_years < 5:
        if SDSves <= -3 or SDSimt <= -3:
            # print(f"Острая белково-энергетическая недостаточность, тяжёлой степени (индекс массы тела = {SDSimt} SDS, вес = {SDSves} SDS).")
            # return
            return Narushenie.objects.get_or_create(type_narushenia="Острая белково-энергетическая недостаточность, тяжёлой степени")
              
        if SDSves <= -2 or SDSimt <= -2:
            # print(f"Острая белково-энергетическая недостаточность, умеренной степени (индекс массы тела = {SDSimt} SDS, вес = {SDSves} SDS).")
            # return
            return Narushenie.objects.get_or_create(type_narushenia="Острая белково-энергетическая недостаточность, умеренной степени")
          
    else:
        if SDSimt <= -3:
            # print(f"Острая белково-энергетическая недостаточность, тяжёлой степени (индекс массы тела = {SDSimt} SDS).")
            # return
            return Narushenie.objects.get_or_create(type_narushenia="Острая белково-энергетическая недостаточность, тяжёлой степени")
          
        if SDSimt <= -2:
            # print(f"Острая белково-энергетическая недостаточность, умеренной степени (индекс массы тела = {SDSimt} SDS).")
            # return
            return Narushenie.objects.get_or_create(type_narushenia="Острая белково-энергетическая недостаточность, умеренной степени")
          
    print("Нарушений не выявлено")
    return Narushenie.objects.get_or_create(type_narushenia="Нарушений не выявлено")  

def main():
    age_years, age_months = calculate_age()
    age_key = calculate_age_key(age_years, age_months)
    gender = "1"
    rost = 110.0
    ves = 20.0
    # gender = input("Введите пол: 1 - мужской, 2 - женский: ")
    # rost = float(input("Введите рост в см: "))
    # ves = float(input("Введите вес в кг: "))
    imt = round((ves / ((rost / 100) ** 2)), 1)
    if gender == "1":
        centiles_rost = centiles_male_rost
        centiles_ves = centiles_male_ves
        centiles_imt = centiles_male_imt
    elif gender == "2":
        centiles_rost = centiles_female_rost
        centiles_ves = centiles_female_ves
        centiles_imt = centiles_female_imt
    print("Антропометрические данные: ")
    sds_r, corr_r = analyze_centile("см - рост", rost, centiles_rost, age_key, resultat=True)
    sds_v, corr_v = analyze_centile("кг - вес", ves, centiles_ves, age_key, resultat=True)
    sds_i, corr_i = analyze_centile("кг/м2 - ИМТ", imt, centiles_imt, age_key, resultat=True)
    if corr_r is None or corr_v is None:
        print(f"Не удалось определить центильные коридоры для возраста {age_key} и пола {gender}")
        return
    harmony_result = harmony(corr_r, corr_v)
    print(harmony_result)
    narushenia_result = narushenia(sds_r, sds_v, sds_i, age_years)
# main()

# def imt_sozdanie(request):
    # def create_entry(i, gender):
    #     age_value = i.get("age")
    #     if "-" in age_value:
    #         parts = age_value.split("-")
    #         age_int1 = float(parts[0])
    #         age_int2 = float(parts[1])
    #         age = age_int1   # в age сохраняем первое значение интервала
    #     else:
    #             age = float(age_value)
    #             age_int1 = age
    #             age_int2 = age
    # for i in centiles_male_imt:
    #     Imt.objects.create(
    #     gender="M", 
    #     age=i.get("age"),
    #     ME=i.get("ME"),
    #     SD=i.get("SD"),
    #     p3=i.get("p3"),
    #     p10=i.get("p10"),
    #     p25=i.get("p25"),
    #     p50=i.get("p50"),
    #     p75=i.get("p75"),
    #     p90=i.get("p90"),
    #     p97= i.get("p97")
    #     )
    # for i in centiles_female_imt:
    #     Imt.objects.create(
    #     gender="Ж", 
    #     age=i.get("age"),
    #     ME=i.get("ME"),
    #     SD=i.get("SD"),
    #     p3=i.get("p3"),
    #     p10=i.get("p10"),
    #     p25=i.get("p25"),
    #     p50=i.get("p50"),
    #     p75=i.get("p75"),
    #     p90=i.get("p90"),
    #     p97= i.get("p97")
    #     )
    # return HttpResponse("Заполняем таблицу имт девочек и мальчиков")




