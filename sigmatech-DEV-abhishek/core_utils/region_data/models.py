from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel


class CountryMobileCodesModel(CoreGenericModel):
    """CountryMobileCodesModel"""

    title = models.CharField(max_length=50, db_column="COUNTRY_NAME")
    country_code = models.CharField(max_length=20, db_column="COUNTRY_CODE")
    mobile_code = models.CharField(max_length=20, db_column="MOBILE_CODE")
    timezone = models.CharField(max_length=50, db_column="TIMEZONE")
    utc = models.CharField(max_length=50, db_column="UTC")
    currency = models.CharField(
        max_length=50, db_column="CURRENCY", null=True, blank=True
    )

    class Meta:
        db_table = "COUNTRY_MOBILE_CODES"
        indexes = [
            models.Index(fields=["country_code"]),
            models.Index(fields=["mobile_code"]),
        ]


# Country model


class CountryModel(CoreGenericModel):
    id = models.BigAutoField(primary_key=True, db_column="COUNTRY_ID")
    code = models.CharField(max_length=5, db_column="COUNTRY_CODE")
    name = models.CharField(max_length=100, db_column="COUNTRY_NAME")

    class Meta:
        db_table = "PUBLIC_DATA_COUNTRIES_TABLE"
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class StateModel(CoreGenericModel):
    id = models.BigAutoField(primary_key=True, db_column="STATE_ID")
    code = models.CharField(max_length=10, db_column="STATE_CODE")
    name = models.CharField(max_length=100, db_column="STATE_NAME")
    country = models.ForeignKey(
        CountryModel, on_delete=models.CASCADE, related_name="StateModel_country"
    )

    class Meta:
        db_table = "PUBLIC_DATA_STATES_TABLE"
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["country"]),
        ]

    def __str__(self):
        return self.name


class PincodeModel(CoreGenericModel):
    id = models.BigAutoField(primary_key=True, db_column="PINCODE_ID")
    pincode = models.CharField(max_length=10, db_column="PINCODE", unique=True)
    district = models.CharField(max_length=100, db_column="DISTRICT")
    circle_name = models.CharField(max_length=100, db_column="CIRCLE_NAME")
    region_name = models.CharField(max_length=100, db_column="REGION_NAME")
    division_name = models.CharField(max_length=100, db_column="DIVISION_NAME")
    state = models.ForeignKey(
        StateModel, on_delete=models.CASCADE, related_name="pincodes"
    )
    country = models.ForeignKey(
        CountryModel, on_delete=models.CASCADE, related_name="pincodes"
    )

    coordinates = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "PUBLIC_DATA_PINCODES_TABLE"
        unique_together = ["pincode", "state"]
        indexes = [
            models.Index(fields=["pincode"]),
            models.Index(fields=["region_name"]),
            models.Index(fields=["state"]),
            models.Index(fields=["country"]),
        ]

    def __str__(self):
        return self.pincode


class CityModel(CoreGenericModel):
    id = models.BigAutoField(primary_key=True, db_column="CITY_ID")
    name = models.CharField(max_length=200, db_column="CITY_NAME")
    latitude = models.FloatField(null=True, blank=True, db_column="LATITUDE")
    longitude = models.FloatField(null=True, blank=True, db_column="LONGITUDE")
    wiki_data_id = models.CharField(max_length=50)

    pincode = models.ForeignKey(
        PincodeModel,
        on_delete=models.CASCADE,
        related_name="offices",
        null=True,
    )
    state = models.ForeignKey(
        StateModel, on_delete=models.CASCADE, related_name="CityModel_state"
    )
    country = models.ForeignKey(
        CountryModel, on_delete=models.CASCADE, related_name="CityModel_country"
    )

    class Meta:
        db_table = "PUBLIC_DATA_CITIES_TABLE"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["pincode"]),
        ]

    def __str__(self):
        return self.name


class CurrencyModel(CoreGenericModel):
    id = models.BigAutoField(primary_key=True, db_column="ID")
    value_type = models.CharField(null=True, blank=True, db_column="VALUE_TYPE")
    currency_rates = models.JSONField(null=True, blank=True, db_column="CURRENCY_RATES")

    class Meta:
        db_table = "CURRENCY_RATE_TABLE"


# from django.db import models
# from core_utils.utils.generics.generic_models import CoreGenericModel


# class CountryMobileCodesModel(CoreGenericModel):
#     """CountryMobileCodesModel"""

#     title = models.CharField(max_length=50, db_column="COUNTRY_NAME")
#     country_code = models.CharField(max_length=20, db_column="COUNTRY_CODE")
#     mobile_code = models.CharField(max_length=20, db_column="MOBILE_CODE")
#     timezone = models.CharField(max_length=50, db_column="TIMEZONE")
#     utc = models.CharField(max_length=50, db_column="UTC")
#     currency = models.CharField(
#         max_length=50, db_column="CURRENCY", null=True, blank=True
#     )

#     class Meta:
#         db_table = "COUNTRY_MOBILE_CODES"


# # Country model


# class CountryModel(CoreGenericModel):
#     id = models.BigAutoField(primary_key=True, db_column="COUNTRY_ID")
#     code = models.CharField(max_length=5, db_column="COUNTRY_CODE")
#     name = models.CharField(max_length=100, db_column="COUNTRY_NAME")

#     class Meta:
#         db_table = "COUNTRIES_TABLE"


# class StateModel(CoreGenericModel):
#     id = models.BigAutoField(primary_key=True, db_column="STATE_ID")
#     code = models.CharField(max_length=10, db_column="STATE_CODE")
#     name = models.CharField(max_length=100, db_column="STATE_NAME")
#     country = models.ForeignKey(
#         CountryModel, on_delete=models.CASCADE, related_name="StateModel_country"
#     )

#     class Meta:
#         db_table = "STATES_TABLE"


# class CityModel(CoreGenericModel):
#     id = models.BigAutoField(primary_key=True, db_column="CITY_ID")
#     name = models.CharField(max_length=200)
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#     wiki_data_id = models.CharField(max_length=50)
#     state = models.ForeignKey(
#         StateModel, on_delete=models.CASCADE, related_name="CityModel_state"
#     )
#     country = models.ForeignKey(
#         CountryModel, on_delete=models.CASCADE, related_name="CityModel_country"
#     )

#     class Meta:
#         db_table = "CITIES_TABLE"


# class CurrencyModel(CoreGenericModel):
#     id = models.BigAutoField(primary_key=True, db_column="ID")
#     value_type = models.CharField(null=True, blank=True, db_column="VALUE_TYPE")
#     currency_rates = models.JSONField(null=True, blank=True, db_column="CURRENCY_RATES")

#     class Meta:
#         db_table = "CURRENCY_RATE_TABLE"
