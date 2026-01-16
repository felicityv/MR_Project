import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from mkb10.models import MKB10


def klass_by_code(code: str) -> str:
    code = code.strip().upper()
    first = code[0]

    if first in "AB":
        return "A"
    if first == "C" or (first == "D" and code[1] in "01234"):
        return "C"
    if first == "D" and code[1] in "56789":
        return "D"
    if first in "EFGHIJKLMNOPQRZU":
        return first
    if first == "H":
        return "H0" if code[1] in "012345" else "H6"
    if first in "ST":
        return "T"
    if first == "V":
        return "V"
    return "Z"


class Command(BaseCommand):
    help = "Загружает МКБ-10 из Excel (код и название)"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Путь к Excel-файлу")

    def handle(self, *args, **opts):
        file_path = opts["file"]

        try:
            df = pd.read_excel(
                file_path,
                usecols="A:B",
                header=None,
                names=["code_mkb", "diagnoz_mkb"],
                dtype=str,
            )
        except Exception as e:
            raise CommandError(f"Ошибка чтения Excel: {e}")

        df.dropna(subset=["code_mkb"], inplace=True)
        df["code_mkb"] = df["code_mkb"].str.strip()
        df["diagnoz_mkb"] = df["diagnoz_mkb"].fillna("").str.strip()
        df.drop_duplicates(subset=["code_mkb"], inplace=True)

        objs = [
            MKB10(
                code_mkb=row.code_mkb,
                diagnoz_mkb=row.diagnoz_mkb,
                mkb_klass=klass_by_code(row.code_mkb),
            )
            for _, row in df.iterrows()
        ]

        MKB10.objects.bulk_create(objs, ignore_conflicts=True, batch_size=5000)
        self.stdout.write(self.style.SUCCESS(f"Загружено {len(objs)} записей МКБ-10"))