# -*- coding: utf-8 -*-
import decimal
import math
import re
from decimal import Decimal
from math import floor

from .base import Num2Word_Base

CURRENCY_PK = [("روپیہ", "دو روپے", "روپے", "روپے"),
               ("پیسہ", "دو پیسے", "پیسے", "پیسے")]

URDU_ONES = [
    "", "ایک", "دو", "تین", "چار", "پانچ", "چھے", "سات", "آٹھ",
    "نو", "دس", "گیارہ", "بارہ", "تیرہ", "چودہ", "پندرہ", "سولہ",
    "سترہ", "اٹھارہ", "انیس"
]

URDU_FEMININE_ONES = [
    "", "ایک", "دو", "تین", "چار", "پانچ", "چھے", "سات", "آٹھ",
    "نو", "دس", "گیارہ", "بارہ", "تیرہ", "چودہ", "پندرہ", "سولہ",
    "سترہ", "اٹھارہ", "انیس"
]

URDU_TENS = [
    "بیس", "تیس", "چالیس", "پچاس", "ساٹھ", "ستر", "اسی", "نوے"
]

URDU_HUNDREDS = [
    "", "ایک سو", "دو سو", "تین سو", "چار سو", "پانچ سو", "چھے سو",
    "سات سو", "آٹھ سو", "نو سو"
]

URDU_GROUP = [
    "", "ہزار", "لاکھ", "کروڑ", "ارب", "کھرب", "نیل", "دس کھرب",
    "سو کھرب", "نیل"
]

class Num2Word_UR(Num2Word_Base):
    errmsg_toobig = "abs(%s) must be less than %s."
    MAXVAL = 10**51

    def __init__(self):
        super().__init__()

        self.number = 0
        self.urduPrefixText = ""
        self.urduSuffixText = ""
        self.integer_value = 0
        self._decimalValue = ""
        self.partPrecision = 2
        self.currency_unit = CURRENCY_PK[0]
        self.currency_subunit = CURRENCY_PK[1]
        self.isCurrencyPartNameFeminine = False
        self.isCurrencyNameFeminine = False
        self.separator = 'اور'

        self.urduOnes = URDU_ONES
        self.urduFeminineOnes = URDU_FEMININE_ONES
        self.urduTens = URDU_TENS
        self.urduHundreds = URDU_HUNDREDS
        self.urduGroup = URDU_GROUP

    def process_urdu_group(self, group_number, group_level):
        tens = group_number % 100
        hundreds = group_number // 100
        ret_val = ""

        if hundreds > 0:
            ret_val = self.urduHundreds[hundreds]
            if tens > 0:
                ret_val += f" {self.separator} "

        if tens > 0:
            if tens < 20:
                ret_val += self.urduOnes[tens]
            else:
                ones = tens % 10
                tens = (tens // 10) - 2
                ret_val += self.urduTens[tens]
                if ones > 0:
                    ret_val += f" {self.urduOnes[ones]}"

        # Generic fix for correcting common character issues
        ret_val = ret_val.replace("ٹھ", "اٹھ")
        return ret_val.strip()

    def convert(self, value):
        self.number = str(value)
        integer_part, _, decimal_part = self.number.partition('.')

        self.integer_value = int(integer_part)
        self._decimalValue = int(decimal_part) if decimal_part else 0

        if self.integer_value == 0:
            return "صفر"

        result = ""
        group = 0

        while self.integer_value > 0:
            group_value = self.integer_value % 1000
            self.integer_value //= 1000

            if group_value > 0:
                group_suffix = self.urduGroup[group] if group > 0 else ""
                processed_group = self.process_urdu_group(group_value, group)
                if result:
                    result = f"{processed_group} {group_suffix} {self.separator} {result}"
                else:
                    result = f"{processed_group} {group_suffix}"

            group += 1

        return result.strip(self.separator).strip()

    def to_currency(self, value, prefix='', suffix=''):
        self.urduPrefixText = prefix
        self.urduSuffixText = suffix

        result = self.convert(value)

        if self.urduPrefixText:
            result = f"{self.urduPrefixText} {result}"
        if self._decimalValue:
            result += f" {self.separator} {self._decimalValue} {self.currency_subunit[2]}"
        if self.urduSuffixText:
            result += f" {self.urduSuffixText}"

        return result.strip()

    def to_cardinal(self, value):
        self.isCurrencyNameFeminine = False
        return self.convert(value)

    def to_ordinal(self, number):
        if number <= 10:
            return self.urduFeminineOnes[number]
        return self.convert(number)
