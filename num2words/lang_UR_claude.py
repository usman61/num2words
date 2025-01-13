# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

from .base import Num2Word_Base

CURRENCY_PKR = [("روپیہ", "روپے", "روپے", "روپے"),
                ("پیسہ", "پیسے", "پیسے", "پیسے")]

URDU_ONES = [
    "", "ایک", "دو", "تین", "چار", "پانچ", "چھ", "سات", "آٹھ",
    "نو", "دس", "گیارہ", "بارہ", "تیرہ", "چودہ", "پندرہ",
    "سولہ", "سترہ", "اٹھارہ", "انیس"
]

class Num2Word_UR(Num2Word_Base):
    CURRENCY_FORMS = {
        'PKR': (('روپیہ', 'روپے'), ('پیسہ', 'پیسے'))
    }

    def __init__(self):
        super().__init__()
        
        self.number = 0
        self.urdu_prefix_text = ""
        self.urdu_suffix_text = ""
        self.integer_value = 0
        self._decimal_value = 0
        self.part_precision = 2
        self.currency_unit = CURRENCY_PKR[0]
        self.currency_subunit = CURRENCY_PKR[1]
        self.is_currency_feminine = False
        self.separator = 'اور'

        self.urdu_ones = URDU_ONES
        
        self.urdu_tens = [
            "بیس", "تیس", "چالیس", "پچاس", "ساٹھ", "ستر", "اسی",
            "نوے"
        ]
        
        self.urdu_hundreds = [
            "", "سو", "دو سو", "تین سو", "چار سو", "پانچ سو", "چھ سو",
            "سات سو", "آٹھ سو", "نو سو"
        ]

        self.urdu_groups = [
            "سو", "ہزار", "لاکھ", "کروڑ", "ارب", "کھرب"
        ]

        self.urdu_plural_groups = [
            "", "ہزار", "لاکھ", "کروڑ", "ارب", "کھرب"
        ]

    def to_cardinal(self, number):
        if number == 0:
            return "صفر"
            
        if number < 0:
            return "منفی " + self._to_cardinal_positive(-number)
            
        return self._to_cardinal_positive(number)

    def _to_cardinal_positive(self, number):
        if number < 20:
            return self.urdu_ones[number]
            
        if number < 100:
            tens = number // 10 - 2
            unit = number % 10
            if unit == 0:
                return self.urdu_tens[tens]
            return self.urdu_ones[unit] + " " + self.urdu_tens[tens]

        if number < 1000:
            hundreds = number // 100
            remainder = number % 100
            if remainder == 0:
                return self.urdu_hundreds[hundreds]
            return self.urdu_hundreds[hundreds] + " " + self._to_cardinal_positive(remainder)

        for group_index, group_value in enumerate([1000, 100000, 10000000, 1000000000, 100000000000], 1):
            if number < group_value * 100:
                quotient = number // group_value
                remainder = number % group_value
                cardinal = self._to_cardinal_positive(quotient)
                group_name = self.urdu_groups[group_index]
                
                if remainder == 0:
                    return cardinal + " " + group_name
                return cardinal + " " + group_name + " " + self._to_cardinal_positive(remainder)

        raise OverflowError("Number too large for conversion to Urdu words")

    def to_currency(self, value, currency='PKR', prefix='', suffix=''):
        number = int(value)
        decimal = int(round((value - number) * 100))
        
        result = self.to_cardinal(number)
        
        if currency == 'PKR':
            if number == 1:
                result += " روپیہ"
            else:
                result += " روپے"
                
            if decimal > 0:
                result += " " + self.separator + " "
                result += self.to_cardinal(decimal)
                if decimal == 1:
                    result += " پیسہ"
                else:
                    result += " پیسے"
                    
        if prefix:
            result = prefix + " " + result
        if suffix:
            result = result + " " + suffix
            
        return result

    def to_ordinal(self, number):
        if number == 1:
            return "پہلا"
        if number == 2:
            return "دوسرا"
        if number == 3:
            return "تیسرا"
        
        cardinal = self.to_cardinal(number)
        if cardinal.endswith("یک"):
            return cardinal[:-2] + "کواں"
        return cardinal + "واں"

    def to_ordinal_num(self, number):
        return str(number) + "واں"

    def to_year(self, number):
        return self.to_cardinal(number)
