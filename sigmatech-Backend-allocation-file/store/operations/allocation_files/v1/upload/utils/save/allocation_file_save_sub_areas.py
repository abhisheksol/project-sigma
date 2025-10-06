import re
from typing import List, Optional, Dict
from store.configurations.region_config.models import RegionConfigurationAreaModel
from store.operations.case_management.models import CaseManagementCaseModel


# --------------------------------------------------------------------
#  Address field keys (used to build complete addresses for matching)
# --------------------------------------------------------------------

# Keys used to construct the residential address string
residential_address_key: List[str] = [
    "residential_address_1",
    "residential_address_2",
    "residential_address_3",
    "residential_address_4",
]

# Keys used to construct the customer/employer (office) address string
customer_employer_address_key: List[str] = [
    "customer_employer_address_1",
    "customer_employer_address_2",
    "customer_employer_address_3",
    "customer_employer_address_4",
]


# --------------------------------------------------------------------
#  Utility Functions
# --------------------------------------------------------------------


def get_concat_address_from_case_instance(
    case_instance: CaseManagementCaseModel, is_office_address: bool = False
) -> str:
    """
    Concatenate multiple address fields of a case into a single string.

    Args:
        case_instance (CaseManagementCaseModel): The case instance containing address fields.
        is_office_address (bool, optional): If True, use customer/employer address fields.
                                            Otherwise, use residential address fields.
                                            Defaults to False.

    Returns:
        str: A single concatenated address string (may contain commas).
    """
    # Select appropriate address keys depending on the address type
    address_keys: List[str] = (
        customer_employer_address_key if is_office_address else residential_address_key
    )

    # Concatenate all address components with a space separator, ignoring None values
    concatenated_address: str = " ".join(
        getattr(case_instance, key) or "" for key in address_keys
    )

    return concatenated_address


def normalize_address_part(part: str) -> str:
    """
    Normalize a single address part by:
    - Removing punctuation
    - Stripping leading/trailing spaces
    - Converting to lowercase

    Args:
        part (str): Raw address substring.

    Returns:
        str: Normalized address substring for matching.
    """
    normalized: str = re.sub(r"[^\w\s]", "", part).strip().lower()
    return normalized


def get_address_combinations(address: str) -> List[str]:
    """
    Generate all possible substring combinations from a comma-separated address.
    This helps in matching different levels of granularity (e.g., area, locality, city).

    Example:
        Input:  "Kailash Nagar, Chanda Nagar, Hyderabad"
        Output: ["kailash nagar", "chanda nagar", "hyderabad",
                 "kailash nagar chanda nagar", "chanda nagar hyderabad",
                 "kailash nagar chanda nagar hyderabad"]

    Args:
        address (str): Full address string.

    Returns:
        List[str]: Sorted list of address combinations (longest first).
    """
    # Split address into parts by comma and normalize each part
    parts: List[str] = [
        normalize_address_part(p) for p in address.split(",") if p.strip()
    ]

    # Use a set to avoid duplicate combinations
    combos: set[str] = set()

    # Generate combinations from all possible contiguous parts
    for i in range(len(parts)):
        for j in range(i, len(parts)):
            combo: str = " ".join(parts[i : j + 1]).strip()
            if combo:
                combos.add(combo)

    # Return combinations sorted by length in descending order
    return sorted(combos, key=len, reverse=True)


def find_sub_area_from_address(
    address: str, area_lookup: Dict[str, RegionConfigurationAreaModel]
) -> Optional[RegionConfigurationAreaModel]:
    """
    Attempt to find a matching sub-area (RegionConfigurationAreaModel) from an address string.

    Args:
        address (str): The full address string of the case (residential or office).
        area_lookup (Dict[str, RegionConfigurationAreaModel]):
            A preloaded lookup dictionary mapping normalized area titles to their model instances.

    Returns:
        Optional[RegionConfigurationAreaModel]:
            The matched sub-area instance if found, otherwise None.
    """
    if not address:
        return None

    # Generate combinations and check if any match the preloaded lookup
    for combo in get_address_combinations(address):
        if combo in area_lookup:
            return area_lookup[combo]

    return None


# --------------------------------------------------------------------
#  Main Save Function
# --------------------------------------------------------------------


def save_sub_area_to_allocation_case_instance(
    case_instance: CaseManagementCaseModel,
    area_lookup: Dict[str, RegionConfigurationAreaModel],
) -> bool:
    """
    Match and assign residential and customer sub-area instances to a case.
    This function uses a preloaded area_lookup dictionary to avoid DB hits
    during bulk allocation file processing.

    Args:
        case_instance (CaseManagementCaseModel):
            The case instance to update.
        area_lookup (Dict[str, RegionConfigurationAreaModel]):
            A preloaded lookup dictionary mapping normalized area titles to their model instances.

    Returns:
        bool: True if any sub-area fields were updated and saved, False otherwise.
    """
    # Track whether we made any updates
    updated: bool = False

    # --- Residential Address Sub-area ---
    residential_address: str = get_concat_address_from_case_instance(
        case_instance, is_office_address=False
    )
    residential_sub_area: Optional[RegionConfigurationAreaModel] = (
        find_sub_area_from_address(residential_address, area_lookup)
    )
    if residential_sub_area:
        case_instance.residential_sub_area = residential_sub_area
        updated: bool = True

    # --- Customer/Office Address Sub-area ---
    customer_address: str = get_concat_address_from_case_instance(
        case_instance, is_office_address=True
    )
    customer_sub_area: Optional[RegionConfigurationAreaModel] = (
        find_sub_area_from_address(customer_address, area_lookup)
    )
    if customer_sub_area:
        case_instance.customer_sub_area = customer_sub_area
        updated: bool = True

    # Save only if any sub-area fields were updated
    if updated:
        case_instance.save(update_fields=["residential_sub_area", "customer_sub_area"])
        return True

    return False
