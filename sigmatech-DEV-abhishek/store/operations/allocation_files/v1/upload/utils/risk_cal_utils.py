from datetime import date
from decimal import Decimal
from typing import Dict, Any

from store.operations.case_management.enums import RiskTypesEnum
from store.operations.case_management.models import CaseManagementCaseModel


def calculate_outstanding_ratio_points(case_instance: CaseManagementCaseModel) -> int:
    """
    Calculate risk points based on outstanding ratio (POS_VALUE / TOTAL_LOAN_AMOUNT).

    Args:
        case_instance: CaseManagementCaseModel instance

    Returns:
        int: Points from outstanding ratio (0–8)
    """
    pos_pct: Decimal = Decimal("0")

    if (
        case_instance.total_loan_amount
        and case_instance.total_loan_amount > 0
        and case_instance.pos_value is not None
    ):
        pos_pct: float = case_instance.pos_value / case_instance.total_loan_amount

    if pos_pct >= Decimal("0.90"):
        return 8
    elif pos_pct >= Decimal("0.70"):
        return 6
    elif pos_pct >= Decimal("0.50"):
        return 4
    elif pos_pct >= Decimal("0.30"):
        return 2
    return 0


def calculate_payment_and_tenure_points(case_instance: CaseManagementCaseModel) -> int:
    """
    Calculate risk points based on payment recency and early-tenure stress.

    Args:
        case_instance: CaseManagementCaseModel instance

    Returns:
        int: Sum of points from payment recency (0–6) and early-tenure stress (0–4)
    """
    # Payment recency
    recency_points: int = 0
    recency_days: int = 999
    if case_instance.last_payment_date:
        recency_days = (date.today() - case_instance.last_payment_date).days

    if recency_days == 0:
        recency_points: int = 0
    elif 1 <= recency_days <= 15:
        recency_points: int = 1
    elif 16 <= recency_days <= 30:
        recency_points: int = 3
    elif 31 <= recency_days <= 60:
        recency_points: int = 4
    elif recency_days > 60:
        recency_points: int = 6

    # Early-tenure stress
    tenure_points: int = 0
    paid_pct: Decimal = Decimal("0")
    pos_pct: Decimal = Decimal("0")

    if (
        case_instance.total_loan_amount
        and case_instance.total_loan_amount > 0
        and case_instance.pos_value is not None
    ):
        pos_pct: float = case_instance.pos_value / case_instance.total_loan_amount
    if (
        case_instance.tenure
        and case_instance.tenure > 0
        and case_instance.number_of_emi_paid is not None
    ):
        paid_pct: float = (
            Decimal(case_instance.number_of_emi_paid) / case_instance.tenure
        )

    if paid_pct < Decimal("0.25") and pos_pct >= Decimal("0.70"):
        tenure_points: int = 4
    elif paid_pct < Decimal("0.50") and pos_pct >= Decimal("0.70"):
        tenure_points: int = 3
    elif paid_pct < Decimal("0.25"):
        tenure_points: int = 2
    elif paid_pct < Decimal("0.50"):
        tenure_points: int = 1

    return recency_points + tenure_points


def calculate_penalty_pressure_points(case_instance: CaseManagementCaseModel) -> int:
    """
    Calculate risk points based on penalty and minimum due pressure.

    Args:
        case_instance: CaseManagementCaseModel instance

    Returns:
        int: Points from penalty/min-due pressure (0–2)
    """
    pen_sum: Decimal = Decimal("0")
    if case_instance.penalty_amount:
        pen_sum += case_instance.penalty_amount
    if case_instance.late_payment_fee:
        pen_sum += case_instance.late_payment_fee
    if case_instance.late_payment_charges:
        pen_sum += case_instance.late_payment_charges

    if pen_sum > 0 or (
        case_instance.minimum_due_amount and case_instance.minimum_due_amount > 0
    ):
        return 2
    return 0


def calculate_risk_enum_for_case_instance(
    case_instance: CaseManagementCaseModel,
) -> Dict[str, Any]:
    """
    Calculate risk points and return the corresponding RiskTypesEnum value.
    Returns None if all relevant fields are null.

    Args:
        case_instance: CaseManagementCaseModel instance

    Returns:
        Optional[str]: RiskTypesEnum value (CRITICAL, HIGH, MEDIUM, LOW) or None if all fields are null
    """
    # Check if all relevant fields are null
    all_fields_null: bool = (
        case_instance.pos_value is None
        and case_instance.total_loan_amount is None
        and case_instance.last_payment_date is None
        and case_instance.number_of_emi_paid is None
        and case_instance.tenure is None
        and case_instance.penalty_amount is None
        and case_instance.late_payment_fee is None
        and case_instance.late_payment_charges is None
        and case_instance.minimum_due_amount is None
    )

    if all_fields_null:
        return {"risk": None, "risk_points": 0}

    # Calculate total risk points
    total_points: int = (
        calculate_outstanding_ratio_points(case_instance)
        + calculate_payment_and_tenure_points(case_instance)
        + calculate_penalty_pressure_points(case_instance)
    )

    # Map points to RiskTypesEnum
    if total_points >= 12:
        return {"risk": RiskTypesEnum.CRITICAL.value, "risk_points": total_points}
    elif total_points >= 8:
        return {"risk": RiskTypesEnum.HIGH.value, "risk_points": total_points}
    elif total_points >= 4:
        return {"risk": RiskTypesEnum.MEDIUM.value, "risk_points": total_points}
    else:
        return {"risk": RiskTypesEnum.LOW.value, "risk_points": total_points}
