# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 21:52:14 2021

@author: 78182
"""

from autocorrect import Speller
spell = Speller
#input: ['I','Love','Yoy']
def spell_check(list_of_tokens):
    do_you_mean = []
    for w in list_of_tokens:
        do_you_mean.append(spell(w))
    final = ' '.join(do_you_mean)
    if do_you_mean != list_of_tokens:
        return f'{final}'