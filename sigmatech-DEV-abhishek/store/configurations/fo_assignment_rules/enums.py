from core_utils.utils.enums import EnumChoices


class PerformanceMetricsFactorEnumChoices(EnumChoices):
    RECOVERY_RATE = "RECOVERY_RATE"
    SUCCESS_RATE = "SUCCESS_RATE"


class PerformanceOptionalRuleTypeEnumChoices(EnumChoices):
    OPTIONAL_MEDIA_UPLOAD = "OPTIONAL_MEDIA_UPLOAD"
    OPTIONAL_GPS_TRACKING = "OPTIONAL_GPS_TRACKING"
    # OPTIONAL_MEDIA_LOCATION = "OPTIONAL_MEDIA_LOCATION"   # Location mapping
    # OPTIONAL_GPS_LOCATION = "OPTIONAL_GPS_LOCATION"       # Location mapping
