# ----------------------------------------------------------------------------
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml
#
# ----------------------------------------------------------------------------

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code using: baml-cli generate
# baml-cli is available with the baml package.

import typing
import typing_extensions
from enum import Enum


from pydantic import BaseModel, ConfigDict


import baml_py

CheckT = typing_extensions.TypeVar("CheckT")
CheckName = typing_extensions.TypeVar("CheckName", bound=str)


class Check(BaseModel):
    name: str
    expression: str
    status: str


class Checked(BaseModel, typing.Generic[CheckT, CheckName]):
    value: CheckT
    checks: typing.Dict[CheckName, Check]


def get_checks(checks: typing.Dict[CheckName, Check]) -> typing.List[Check]:
    return list(checks.values())


def all_succeeded(checks: typing.Dict[CheckName, Check]) -> bool:
    return all(check.status == "succeeded" for check in get_checks(checks))


# #########################################################################
# Generated enums (1)
# #########################################################################


class FaithfulnessErrorType(str, Enum):
    CONTRADICTORY_FACTS = "CONTRADICTORY_FACTS"
    NUMERIC_STATISTICAL_DISTORTION = "NUMERIC_STATISTICAL_DISTORTION"
    WRONG_DATES_TIMELINE = "WRONG_DATES_TIMELINE"
    INCORRECT_ATTRIBUTION_IDENTIFIER = "INCORRECT_ATTRIBUTION_IDENTIFIER"
    CONTEXTUAL_OMISSION = "CONTEXTUAL_OMISSION"
    BAD_OR_NONEXISTENT_SOURCE = "BAD_OR_NONEXISTENT_SOURCE"
    SPECULATION_AS_FACT = "SPECULATION_AS_FACT"
    OUTDATED_INFORMATION = "OUTDATED_INFORMATION"
    FALSE_CAUSATION = "FALSE_CAUSATION"
    OVERGENERALIZATION = "OVERGENERALIZATION"


# #########################################################################
# Generated classes (2)
# #########################################################################


class FaithfulnessError(BaseModel):
    reasoning: str
    error_type: FaithfulnessErrorType


class PublicationTime(BaseModel):
    reasoning: str
    is_in_the_text: bool
    year: int
    month: int
    day: int


# #########################################################################
# Generated type aliases (0)
# #########################################################################
