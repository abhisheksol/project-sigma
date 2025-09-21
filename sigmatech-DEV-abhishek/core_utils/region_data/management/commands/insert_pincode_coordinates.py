import json
from django.core.management.base import BaseCommand
from core_utils.region_data.models import PincodeModel


class Command(BaseCommand):
    help: str = "Insert coordinates into existing pincodes from a GeoJSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "geojson_path",
            nargs="?",
            default="core_utils/region_data/pincode_boundaries.geojson",
            help="Path to the pincode boundaries GeoJSON file",
        )

    def handle(self, *args, **options):
        geojson_path: str = options["geojson_path"]

        try:
            with open(geojson_path) as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {geojson_path}"))
            return

        count: int = 0
        for feature in data.get("features", []):
            pincode = str(feature["properties"].get("Pincode")).strip()
            coords = feature.get("geometry", {}).get("coordinates")

            if not pincode or not coords:
                self.stdout.write(f"⚠️ Skipping feature with missing data: {feature}")
                continue

            try:
                obj = PincodeModel.objects.get(pincode=pincode)
                obj.coordinates = coords
                obj.save()
                count += 1
            except PincodeModel.DoesNotExist:
                self.stdout.write(f"⚠️ Pincode {pincode} not found, skipping.")

        self.stdout.write(
            self.style.SUCCESS(f"✅ Inserted coordinates for {count} pincodes")
        )
