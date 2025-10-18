from typing import Dict, List
from core_utils.region_data.models import PincodeModel
from store.configurations.region_config.models import (
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationAreaModel,
)
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
import json
from pathlib import Path


def load_region_data_from_file(file_path: str):
    """
    Load region hierarchy data from a JSON file and populate the database.

    This function reads a JSON file containing region hierarchy data (region, city, pincode, subarea)
    and creates or updates corresponding model instances in the database. It handles:
    - Creation of Region, Zone, City, Pincode, and Area records.
    - Validation to prevent duplicate pincode entries that violate the OneToOneField constraint.
    - Logging of any issues encountered during data loading.

    Args:
        file_path (str): Path to the JSON file containing region hierarchy data.

    Raises:
        FileNotFoundError: If the specified JSON file does not exist.
        IntegrityError: If a database integrity constraint (e.g., unique pincode) is violated.
    """
    file: Path = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    with open(file, "r", encoding="utf-8") as f:
        data: List[Dict[str, str]] = json.load(f)

    # Validate JSON for duplicate pincodes with different cities
    pincode_city_map: Dict[str, str] = {}
    for entry in data:
        pincode = entry.get("pincode")
        city = entry.get("city")
        if pincode in pincode_city_map and pincode_city_map[pincode] != city:
            print(
                f"⚠️ Warning: Pincode {pincode} associated with multiple cities: {pincode_city_map[pincode]} and {city}"
            )
        pincode_city_map[pincode] = city

    for entry in data:
        region_name: str = entry.get("region")
        city_name: str = entry.get("city")
        state: str = entry.get("state")
        pincode_value: str = entry.get("pincode")
        subarea: str = entry.get("subarea")

        try:
            # 1. Create or get Region
            region_obj, _ = RegionConfigurationRegionModel.objects.get_or_create(
                title=region_name
            )

            # 2. Create or get Zone
            zone_obj, _ = RegionConfigurationZoneModel.objects.get_or_create(
                region=region_obj,
                title=state,
            )

            # 3. Create or get City
            city_obj, _ = RegionConfigurationCityModel.objects.get_or_create(
                zone=zone_obj,
                city_name=city_name,
            )

            # 4. Create or get Pincode in master table
            pincode_master, _ = PincodeModel.objects.get_or_create(
                pincode=pincode_value
            )

            # 5. Check if pincode is already associated with a different city
            existing_pincode = RegionConfigurationPincodeModel.objects.filter(
                pincode=pincode_master
            ).first()
            if existing_pincode and existing_pincode.city != city_obj:
                print(
                    f"⚠️ Skipping pincode {pincode_value}: already associated with city {existing_pincode.city.city_name}, cannot assign to {city_name}"
                )

            # 6. Create or get RegionConfigurationPincodeModel
            pincode_obj, created = (
                RegionConfigurationPincodeModel.objects.get_or_create(
                    pincode=pincode_master,
                    defaults={"city": city_obj},
                )
            )
            if created:
                print(
                    f"✅ Created RegionConfigurationPincodeModel for pincode {pincode_value}"
                )
            else:
                print(
                    f"ℹ️ Using existing RegionConfigurationPincodeModel for pincode {pincode_value}"
                )

            # 7. Create or get Subarea
            area_obj, created = RegionConfigurationAreaModel.objects.get_or_create(
                title=subarea,
                pincode=pincode_obj,
            )
            if created:
                print(f"✅ Created Area {subarea} for pincode {pincode_value}")
            else:
                print(f"ℹ️ Using existing Area {subarea} for pincode {pincode_value}")

        except IntegrityError as e:
            print(f"❌ Error processing entry {entry}: {str(e)}")

    print("✅ Data loading completed successfully")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """
        Django management command to load region configuration data from a JSON file.

        This command wraps the load_region_data_from_file function in a transaction to ensure
        data consistency. Note: The transaction is set to rollback for testing purposes.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        with transaction.atomic():
            load_region_data_from_file(file_path="test_load_region_data.json")
