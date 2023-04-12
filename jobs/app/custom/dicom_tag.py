from enum import Enum


class DicomTag(Enum):
    PatientBirthDate = 0x00100030
    PatientSex = 0x00100040
    StudyInstanceUID = 0x0020000D
