from django.core.management.base import BaseCommand
from django.db import transaction
from core_utils.region_data.models import PincodeModel
from store.configurations.region_config.models import (
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationAreaModel,
)
from typing import Dict, Any

# Your client_data dictionary can also be loaded from JSON file
client_data: Dict[str, Any] = {
    "UP-UK FE": [
        {"City": "Lucknow", "PIN": 226017},
        {"City": "Kashipur", "PIN": 262405},
        {"City": "Sitarganj", "PIN": 262308},
        {"City": "Nanakmata", "PIN": 262402},
        {"City": "Dehradun", "PIN": 248002},
        {"City": "Haldwani", "PIN": 262311},
        {"City": "Ramnagar", "PIN": 244925},
        {"City": "Muzaffarnagar", "PIN": 251001},
        {"City": "Lucknow", "PIN": 2206004},
        {"City": "Lucknow", "PIN": 226017},
        {"City": "Dehradun", "PIN": 248005},
        {"City": "Saharanpur", "PIN": 247001},
        {"City": "Meerut", "PIN": 250001},
        {"City": "Jaunpur", "PIN": 222131},
        {"City": "Saharanpur", "PIN": 247002},
        {"City": "Lucknow", "PIN": 2260018},
        {"City": "Jaunpur", "PIN": 222001},
        {"City": "Meerut", "PIN": 250003},
        {"City": "Rampur", "PIN": 263160},
        {"City": "Saharanpur", "PIN": 247122},
        {"City": "Meerut", "PIN": 250002},
        {"City": "Lalkuwa", "PIN": 244713},
        {"City": "Varanasi", "PIN": 221104},
        {"City": "Dehradun", "PIN": 248001},
        {"City": "Kanpur", "PIN": 208008},
        {"City": "Kanpur", "PIN": 208001},
        {"City": "Kanpur", "PIN": 208021},
        {"City": "Varanasi", "PIN": 221104},
        {"City": "Lucknow", "PIN": 226016},
        {"City": "Lucknow", "PIN": 226017},
        {"City": "Jaunpur", "PIN": 222149},
        {"City": "Gorakhpur", "PIN": 273007},
        {"City": "Lucknow", "PIN": 226005},
        {"City": "Jaunpur", "PIN": 222180},
        {"City": "Varanasi", "PIN": 221311},
        {"City": "Khateema", "PIN": 263139},
        {"City": "Bazpur", "PIN": 244921},
        {"City": "Meerut", "PIN": 250001},
        {"City": "Meerut", "PIN": 250002},
        {"City": "Meerut", "PIN": 250003},
        {"City": "Meerut", "PIN": 250004},
        {"City": "Meerut", "PIN": 250005},
        {"City": "Meerut", "PIN": 250103},
        {"City": "Meerut", "PIN": 250110},
        {"City": "Muzaffarnagar", "PIN": 251002},
        {"City": "Meerut", "PIN": 250005},
    ],
    "North FE": [
        {"City": "DELHI", "Area": "NORTH", "PIN": 110083},
        {"City": "DELHI", "Area": "NORTH", "PIN": 110085},
        {"City": "DELHI", "Area": "WEST", "PIN": 110041},
        {"City": "DELHI", "Area": "WEST", "PIN": 110058},
        {"City": "NCR", "Area": "GURGAON", "PIN": 122001},
        {"City": "NCR", "Area": "GHAZIABAD", "PIN": 210001},
        {"City": "NCR", "Area": "GURGAON", "PIN": 122001},
        {"City": "DELHI", "Area": "WEST", "PIN": 110045},
        {"City": "DELHI", "Area": "SOUTH", "PIN": 110017},
        {"City": "DELHI", "Area": "NORTH", "PIN": 110033},
        {"City": "DELHI", "Area": "CENTRAL", "PIN": 110005},
        {"City": "DELHI", "Area": "WEST", "PIN": 110015},
        {"City": "DELHI", "Area": "WEST", "PIN": 110043},
        {"City": "DELHI", "Area": "EAST", "PIN": 110092},
        {"City": "NCR", "Area": "GHAZIABAD", "PIN": 210001},
        {"City": "NCR", "Area": "FARIDABAD", "PIN": 121004},
        {"City": "DELHI", "Area": "EAST", "PIN": 110053},
        {"City": "DELHI", "Area": "EAST", "PIN": 110093},
        {"City": "DELHI", "Area": "WEST", "PIN": 110015},
        {"City": "DELHI", "Area": "NORTH", "PIN": 110039},
        {"City": "DELHI", "Area": "SOUTH", "PIN": 110017},
        {"City": "DELHI", "Area": "West", "PIN": 110015},
        {"City": "DELHI", "Area": "EAST", "PIN": 110053},
        {"City": "DELHI", "Area": "North", "PIN": 110086},
        {"City": "DELHI", "Area": "EAST", "PIN": 110031},
        {"City": "DELHI", "Area": "WEST", "PIN": 110045},
        {"City": "DELHI", "Area": "South", "PIN": 110003},
        {"City": "DELHI", "Area": "EAST", "PIN": 110032},
        {"City": "NCR", "Area": "NOIDA", "PIN": 201301},
        {"City": "DELHI", "Area": "EAST", "PIN": 110092},
        {"City": "DELHI", "Area": "NORTH", "PIN": 110007},
        {"City": "DELHI", "Area": "South", "PIN": 110030},
        {"City": "DELHI", "Area": "EAST", "PIN": 110095},
        {"City": "DELHI", "Area": "North", "PIN": 110034},
        {"City": "DELHI", "Area": "NORTH", "PIN": 110034},
        {"City": "DELHI", "Area": "WEST", "PIN": 110059},
        {"City": "DELHI", "Area": "EAST", "PIN": 110093},
        {"City": "DELHI", "Area": "EAST", "PIN": 110091},
        {"City": "DELHI", "Area": "North", "PIN": 110036},
        {"City": "DELHI", "Area": "Central", "PIN": 110001},
        {"City": "DELHI", "Area": "West", "PIN": 110063},
        {"City": "DELHI", "Area": "SOUTH", "PIN": 110062},
        {"City": "DELHI", "Area": "NORTH", "PIN": 110007},
        {"City": "DELHI", "Area": "SOUTH", "PIN": 110062},
        {"City": "DELHI", "Area": "NOIDA", "PIN": 201301},
        {"City": "DELHI", "Area": "NOIDA", "PIN": 201301},
        {"City": "DELHI", "Area": "EAST", "PIN": 110032},
        {"City": "DELHI", "Area": "NOIDA", "PIN": 201301},
        {"City": "DELHI", "Area": "NOIDA", "PIN": 201308},
        {"City": "DELHI", "Area": "NORTH", "PIN": 110007},
        {"City": "DELHI", "Area": "GURGAON", "PIN": 122001},
        {"City": "DELHI", "Area": "G NOIDA", "PIN": 201009},
        {"City": "DELHI", "Area": "West", "PIN": 110059},
    ],
    "West FE": [
        {"City": "Ahmedabad", "PIN": 380052},
        {"City": "CUTTACK/ BBSR", "PIN": 753001},
        {"City": "BHUBANESWAR", "PIN": 751010},
        {"City": "BALASORE", "PIN": 756100},
        {"City": "SURAT", "PIN": 396415},
        {"City": "SURAT", "PIN": 394120},
        {"City": "BHUBANESWAR", "PIN": 752001},
        {"City": "Ahmedabad", "PIN": 380005},
        {"City": "Ahmedabad", "PIN": 380004},
        {"City": "Ahmedabad", "PIN": 382330},
        {"City": "Ahmedabad", "PIN": 380009},
        {"City": "SURAT", "PIN": 394230},
        {"City": "CUTTACK", "PIN": 755003},
        {"City": "Surat", "PIN": 394221},
        {"City": "SURAT", "PIN": 394130},
        {"City": "Ahmedabad", "PIN": 382430},
        {"City": "BHUBANESWAR", "PIN": 751001},
        {"City": "Ahmedabad", "PIN": 382405},
        {"City": "SURAT", "PIN": 394105},
        {"City": "BHUBANESWAR", "PIN": 752002},
        {"City": "CUTTACK", "PIN": 755011},
        {"City": "BHUBANESWAR", "PIN": 754134},
        {"City": "Ahmedabad", "PIN": 380002},
        {"City": "SURAT", "PIN": 394155},
        {"City": "SURAT", "PIN": 394170},
        {"City": "BALASORE", "PIN": 756112},
        {"City": "SURAT", "PIN": 394210},
        {"City": "SURAT", "PIN": 394220},
        {"City": "Ahmedabad", "PIN": 380018},
        {"City": "NAGPUR", "PIN": 440002},
        {"City": "NAGPUR", "PIN": 440013},
        {"City": "MUMBAI", "PIN": 401403},
        {"City": "MUMBAI", "PIN": 401103},
        {"City": "MUMBAI", "PIN": 401402},
        {"City": "MUMBAI", "PIN": 400042},
        {"City": "MUMBAI", "PIN": 401601},
        {"City": "MUMBAI", "PIN": 400068},
        {"City": "SOLAPUR", "PIN": 413002},
        {"City": "MUMBAI", "PIN": 401605},
        {"City": "MUMBAI", "PIN": 401201},
        {"City": "MUMBAI", "PIN": 400053},
        {"City": "MUMBAI", "PIN": 400003},
        {"City": "NAGPUR", "PIN": 440015},
        {"City": "MUMBAI", "PIN": 401607},
        {"City": "MUMBAI", "PIN": 401304},
        {"City": "MUMBAI", "PIN": 400008},
        {"City": "SOLAPUR", "PIN": 413001},
        {"City": "MUMBAI", "PIN": 40097},
        {"City": "KOLHAPUR", "PIN": 416001},
        {"City": "MUMBAI", "PIN": 421303},
        {"City": "MUMBAI", "PIN": 400019},
        {"City": "KOLHAPUR", "PIN": 415302},
        {"City": "VADODARA", "PIN": 390001},
        {"City": "SURAT", "PIN": 393125},
        {"City": "VADODARA", "PIN": 390019},
        {"City": "ANAND", "PIN": 387380},
        {"City": "RAJKOT", "PIN": 360003},
        {"City": "ANAND", "PIN": 388205},
        {"City": "VADODARA", "PIN": 390012},
        {"City": "ANAND", "PIN": 387001},
        {"City": "ANAND", "PIN": 387310},
        {"City": "BHAVNAGAR", "PIN": 364003},
        {"City": "SURAT", "PIN": 393110},
        {"City": "ANAND", "PIN": 387320},
        {"City": "ANAND", "PIN": 387210},
        {"City": "ANAND", "PIN": 388307},
        {"City": "VADODARA", "PIN": 390007},
        {"City": "ANAND", "PIN": 388430},
        {"City": "ANAND", "PIN": 388170},
        {"City": "BHAVNAGAR", "PIN": 364005},
        {"City": "VADODARA", "PIN": 392011},
        {"City": "RAJKOT", "PIN": 360001},
        {"City": "ANAND", "PIN": 388140},
        {"City": "ANAND", "PIN": 388150},
        {"City": "VADODARA", "PIN": 393002},
        {"City": "VADODARA", "PIN": 393001},
        {"City": "VADODARA", "PIN": 392001},
        {"City": "ANAND", "PIN": 388120},
        {"City": "AHMEDABAD", "PIN": 387130},
        {"City": "VADODARA", "PIN": 393145},
        {"City": "VADODARA", "PIN": 393120},
        {"City": "SURAT", "PIN": 393130},
        {"City": "ANAND", "PIN": 387340},
        {"City": "JORHAT", "PIN": 785674},
        {"City": "JORHAT", "PIN": 785661},
        {"City": "JORHAT", "PIN": 785680},
        {"City": "GUWAHATI", "PIN": 781350},
        {"City": "JORHAT", "PIN": 785696},
        {"City": "GUWAHATI", "PIN": 781360},
        {"City": "GUWAHATI", "PIN": 781137},
        {"City": "GUWAHATI", "PIN": 781138},
        {"City": "JORHAT", "PIN": 785672},
        {"City": "GUWAHATI", "PIN": 781102},
        {"City": "JORHAT", "PIN": 785685},
        {"City": "JORHAT", "PIN": 785662},
        {"City": "JORHAT", "PIN": 785663},
        {"City": "JORHAT", "PIN": 785112},
        {"City": "JORHAT", "PIN": 785697},
    ],
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        # client_data = {
        #     "UP-UK FE": [
        #         {"City": "Lucknow", "PIN": 226017},
        #         {"City": "Kashipur", "PIN": 262405},
        #         {"City": "Sitarganj", "PIN": 262308},
        #         {"City": "Nanakmata", "PIN": 262402},
        #         {"City": "Meerut", "PIN": 250005},
        #     ],
        #     "North FE": [
        #         {"City": "DELHI", "Area": "NORTH", "PIN": 110083},
        #         {"City": "DELHI", "Area": "NORTH", "PIN": 110085},
        #         {"City": "DELHI", "Area": "WEST", "PIN": 110041},
        #         {"City": "DELHI", "Area": "West", "PIN": 110059},
        #     ],
        #     "West FE": [
        #         {"City": "Ahmedabad", "PIN": 380052},
        #         {"City": "CUTTACK/ BBSR", "PIN": 753001},
        #         {"City": "BHUBANESWAR", "PIN": 751010},
        #         {"City": "BALASORE", "PIN": 756100},
        #         {"City": "JORHAT", "PIN": 785112},
        #         {"City": "JORHAT", "PIN": 785697},
        #     ],
        # }

        with transaction.atomic():
            for zone_name, cities in client_data.items():
                # Create or get Region
                region, _ = RegionConfigurationRegionModel.objects.get_or_create(
                    title=str(zone_name).capitalize(),
                    defaults={"description": f"Region for {zone_name}"},
                )

                # Process each city/pincode/area
                for city_data in cities:
                    pincode_str = str(city_data["PIN"])
                    try:
                        # Get PincodeModel to extract state
                        pincode_obj = PincodeModel.objects.get(pincode=pincode_str)
                        state: str = pincode_obj.state

                        # Create or get Zone (using state from PincodeModel)
                        zone, _ = RegionConfigurationZoneModel.objects.get_or_create(
                            title=str(state).capitalize(),
                            region=region,
                            defaults={
                                "description": f"Zone for {zone_name} in {state}"
                            },
                        )

                        # Create or get City
                        city, _ = RegionConfigurationCityModel.objects.get_or_create(
                            city_name=str(city_data["City"]).capitalize(),
                            zone=zone,
                            defaults={"description": f'City {city_data["City"]}'},
                        )

                        # Create or get Pincode
                        pincode_config, _ = (
                            RegionConfigurationPincodeModel.objects.get_or_create(
                                pincode=pincode_obj, city=city
                            )
                        )

                        # Create Area if present
                        if "Area" in city_data:
                            RegionConfigurationAreaModel.objects.get_or_create(
                                title=str(city_data["Area"]).capitalize(),
                                pincode=pincode_config,
                            )

                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Processed: {city_data["City"]} - {pincode_str}'
                            )
                        )

                    except PincodeModel.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Pincode {pincode_str} not found in PincodeModel"
                            )
                        )
                        continue
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f'Error processing {city_data["City"]} - {pincode_str}: {str(e)}'
                            )
                        )
                        continue

            self.stdout.write(self.style.SUCCESS("Successfully loaded client data"))
