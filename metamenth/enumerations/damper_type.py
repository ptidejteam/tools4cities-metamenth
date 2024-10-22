from metamenth.enumerations.abstract_enum import AbstractEnum


class DamperType(AbstractEnum):
    """
    Types of dampers

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    BASIC_MANUAL_VOLUME = "BasicManualVolume"
    MANUAL_VOLUME = "ManualVolume"
    BACK_DRAFT = "BackDraft"
    BIOMETRIC_BYPASS = "BiometricBypass"
    OTHER = "Other"

