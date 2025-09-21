from rest_framework import serializers
from core_utils.region_data.models import (
    CountryModel,
    StateModel,
    CityModel,
    CountryMobileCodesModel,
)


class CountryModelSerializer(serializers.ModelSerializer):
    """
    Serializer for the CountryModel.

    Serializes the following fields:
    - id: Unique identifier of the country.
    - name: Name of the country.
    """

    class Meta:
        model = CountryModel
        fields = ["id", "name"]  # ? Minimal data for country representation


class StateModelSerializer(serializers.ModelSerializer):
    """
    Serializer for the StateModel.

    Serializes the following fields:
    - id: Unique identifier of the state.
    - name: Name of the state.
    """

    class Meta:
        model = StateModel
        fields = ["id", "name"]  # ? Basic state-level info


class CityModelSerializer(serializers.ModelSerializer):
    """
    Serializer for the CityModel.

    Serializes the following fields:
    - id: Unique identifier of the city.
    - name: Name of the city.
    """

    class Meta:
        model = CityModel
        fields = ["id", "name"]  # ? City name and ID only


class CountryMobileCodesModelSerializer(serializers.ModelSerializer):
    """
    Serializer for the CountryMobileCodesModel.

    Serializes the following fields:
    - id: Unique identifier.
    - title: Display title for the mobile code entry (e.g., country name).
    - country_code: Country dialing code (e.g., 'US').
    - mobile_code: Mobile prefix code (e.g., '+1').
    - timezone: Associated time zone for the country.
    """

    class Meta:
        model = CountryMobileCodesModel
        fields = ["id", "title", "country_code", "mobile_code", "timezone"]
        # ? Provides detailed mobile dialing info and timezone context
