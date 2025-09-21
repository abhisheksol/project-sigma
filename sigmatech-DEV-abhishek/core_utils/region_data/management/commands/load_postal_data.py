from django.core.management.base import BaseCommand
from core_utils.region_data.models import (
    CityModel,
    CountryModel,
    PincodeModel,
    StateModel,
)
import pandas as pd
import re
from typing import Optional, Tuple


def safe_str(val: object) -> str:
    if pd.isna(val):
        return ""
    return str(val).strip()


def safe_float(val: object) -> Optional[float]:
    if pd.isna(val) or val == "":
        return None
    try:
        return float(val)
    except ValueError:
        dms_pattern: str = r"(\d+)°(\d+)'([\d.]+)\"?"
        match: Optional[re.Match[str]] = re.match(dms_pattern, str(val))
        if match:
            degrees: str
            minutes: str
            seconds: str
            degrees, minutes, seconds = match.groups()
            return float(degrees) + float(minutes) / 60 + float(seconds) / 3600
        return None


class Command(BaseCommand):
    help: str = "Load postal data from CSV file"

    def handle(self, *args: tuple, **options: dict) -> None:
        df: pd.DataFrame = pd.read_csv("core_utils/region_data/citymodel.csv")

        self.stdout.write(f"Loaded {len(df)} rows from CSV")

        # Create or get country
        country: CountryModel
        created: bool
        country, created = CountryModel.objects.get_or_create(
            code="IND", defaults={"name": "India"}
        )

        if created:
            self.stdout.write(f"Created country: {country.name}")
        else:
            self.stdout.write(f"Using existing country: {country.name}")

        processed_count: int = 0

        for _, row in df.iterrows():
            state_name: str = safe_str(row["statename"]).upper()
            district_name: str = safe_str(row["district"]).upper()
            pincode_val: str = safe_str(row["pincode"])
            circle_name: str = safe_str(row["circlename"])
            region_name: str = safe_str(row["regionname"])
            division_name: str = safe_str(row["divisionname"])
            officename: str = safe_str(row["officename"])
            latitude: Optional[float] = safe_float(row["latitude"])
            longitude: Optional[float] = safe_float(row["longitude"])

            state: StateModel
            _state_created: bool
            state, _state_created = StateModel.objects.get_or_create(
                name=state_name, country=country, defaults={"code": state_name[:3]}
            )

            # Try to get existing pincode first
            pincode: PincodeModel
            try:
                pincode: PincodeModel = PincodeModel.objects.get(pincode=pincode_val)
            except PincodeModel.DoesNotExist:
                pincode = PincodeModel.objects.create(
                    pincode=pincode_val,
                    state=state,
                    country=country,
                    district=district_name,
                    circle_name=circle_name,
                    region_name=region_name,
                    division_name=division_name,
                )

            _city_obj: Tuple[CityModel, bool] = CityModel.objects.get_or_create(
                name=officename,
                pincode=pincode,
                state=state,
                country=country,
                defaults={
                    "latitude": latitude,
                    "longitude": longitude,
                    "wiki_data_id": "",
                },
            )

            processed_count += 1
            if processed_count % 10 == 0:
                self.stdout.write(f"Processed {processed_count} records...")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported {processed_count} postal records!"
            )
        )
