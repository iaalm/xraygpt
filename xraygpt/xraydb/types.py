from enum import IntEnum, StrEnum
from typing import TypedDict


class Language(StrEnum):
    AR = "ar"
    BG = "bg"
    CA = "ca"
    CS = "cs"
    DA = "da"
    DE = "de"
    EL = "el"
    EN = "en"
    EN_AU = "en-AU"
    EN_CA = "en-CA"
    EN_IN = "en-IN"
    EN_US = "en-US"
    ES = "es"
    ES_MX = "es-MX"
    ES_US = "es-US"
    ET = "et"
    FI = "fi"
    FR = "fr"
    FR_CA = "fr-CA"
    HI_IN = "hi-IN"
    HR = "hr"
    HU = "hu"
    IS = "is"
    IT = "it"
    JA = "ja"
    KO = "ko"
    LT = "lt"
    LV = "lv"
    NB_NO = "nb-NO"
    NL = "nl"
    PL = "pl"
    PT_BR = "pt-BR"
    PT_PT = "pt-PT"
    RO = "ro"
    RU = "ru"
    SK = "sk"
    SL = "sl"
    SR = "sr"
    SV = "sv"
    TR = "tr"
    ZH_CN = "zh-CN"
    ZH_HK = "zh-HK"
    ZH_TW = "zh-TW"


class EntityType(IntEnum):
    People = 1
    Terms = 2


class EntitySource(IntEnum):
    KindleStore = 0
    Wikipedia = 1


class Entity(TypedDict):
    name: str
    type: EntityType | int
    source: EntitySource | int
    count: int
    description: str


class Table(StrEnum):
    BOOK_METADATA = "book_metadata"
    ENTITY = "entity"
    STRING = "string"
    ENTITY_DESCRIPTION = "entity_description"
