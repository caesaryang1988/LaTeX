#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 13:23:06 2020

@author: HUANG YANG (caesaryang1988@gmail.com)

The python script is for cleaning notations in latex file (.tex) by usage of 
trackchanges.sty. After the cleaning, the latex file is good and clean for the
next round of review and revision process.

Following changes are made to the latex file through cleaning.

(a) \add[(editor)]{(text)} -> (text)
(b) \remove[(editor)]{(text)} -> 
(c) \change[(editor)]{(text1)}{(text2)} -> (text2)

Notices as of the version by 07-30-2020 (v1.0)
v1.0 only works on .tex file in which every line is a full paragraph
v1.0 has not addressed excessive '\n' after cleaning the '\remove' paragraphs

Updates as of the version by 07-31-2020 (v1.1)
v1.1 fixes the bug when transformations are identical for multiple places in one
line. For example, \add[]{the}, the str.replace() function will replace all matching
substrings all at once, and therefore the counts of operation before looping 
isn't right.

"""


import re

def mapping_brackets(start_point,end_point,string):
# =============================================================================
# This function pairs brackets in the given string (as the third input), and
# returns the index of the right bracket ('}', as the second input) corresponding
# to the left bracket ('{', index given as the first input). Additional brackets
# within the mapping brackets will be skipped. 
#
# EXAMPLE:
# string = '{who}'
# ep = mapping_brackets(0,0,string)
# print(ep)
# ep = 4
# =============================================================================
    lbracket_counts = 0
    rbracket_counts = 0
    for c_i in range(start_point,len(string)):
        c = string[c_i]
        if lbracket_counts > 0 and rbracket_counts > 0 and \
        lbracket_counts == rbracket_counts:
            break
        if c=='{':
            lbracket_counts += 1
        if c=='}':
            rbracket_counts += 1
            end_point = c_i
    return end_point
    
# Here read the input latex file, change the directory of input file to fit
# your need.
with open('/Users/hy337/Study/AGU-LaTeX/2018_IHT_GRL/ywcp_grl_IHT_2018_revision_marked.tex','r+') as fin:
    lines = fin.readlines()
    lines_new = []
    for line in lines:
# Address '\add'
        query = '\\\\add\[\S*?\]'
        m = re.search(query,line)
        while m is not None:
            add_flag_len = m.end()-m.start()
            sp = m.end()
            ep = 0
            ep = mapping_brackets(sp,ep,line)
# 'str_old' is the old substring as '\add[(editor)]{(text)}'
# 'str_new' is the new substring as '(text)'
            str_old = line[sp-add_flag_len:ep+1]
            str_new = line[sp+1:ep]
            line = line.replace(str_old,str_new)
            m = re.search(query,line)
        query = '\\\\remove\[\S*?\]'
        m = re.search(query,line)
        while m is not None:
            remove_flag_len = m.end()-m.start()
            sp = m.end()
            ep = 0
            ep = mapping_brackets(sp,ep,line)
# 'str_old' is the old substring as '\remove[(editor)]{(text)}'
# 'str_new' is the new substring as nothing
            str_old = line[sp-remove_flag_len:ep+1]
            str_new = ''
            line = line.replace(str_old,str_new)
            m = re.search(query,line)
        query = '\\\\change\[\S*?\]'
        m = re.search(query,line)
        while m is not None:
            m = re.search(query,line)
            change_flag_len = m.end()-m.start()
            sp = m.end()
            ep = 0
# mapping the first pairs of '{}' after '\change[(editor)]'
            ep = mapping_brackets(sp,ep,line)
            sp2 = ep + 1
            ep2 = 0
# mapping the second pairs of '{}' after locating the end of first pairs of '{}'
            ep2 = mapping_brackets(sp2,ep2,line)
# 'str_old' is the old substring as '\change[(editor)]{(text1)}{(text2)}'
# 'str_new' is the new substring as '(text2)'
            str_old = line[sp-change_flag_len:ep2+1]
            str_new = line[sp2+1:ep2]
            line = line.replace(str_old,str_new)
            m = re.search(query,line)
        lines_new.append(line)
fin.close()

# Here write the new and clean latex file. Change the directory of output file
# to fit your need.
with open('/Users/hy337/Study/AGU-LaTeX/2018_IHT_GRL/ywcp_grl_IHT_2018_revision_clean.tex','w+') as fout:
    for line in lines_new:
        fout.write(line)
fout.close()