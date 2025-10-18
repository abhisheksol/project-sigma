from enum import Enum


class TabNameEnum(str, Enum):
    ELIGIBILITY = "eligibility"
    PRIORITY = "priority"
    VISIT_DOCS = "visit_docs"
