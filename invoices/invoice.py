#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import codecs
import sys
import xml.etree.ElementTree as ET
import argparse
import subprocess

one_to_twenty_n = [
    'ένα',
    'δύο',
    'τρία',
    'τέσσερα',
    'πέντε',
    'έξι',
    'επτά',
    'οκτώ',
    'εννέα',
    'δέκα',
    'έντεκα',
    'δώδεκα',
    'δεκατρία',
    'δεκατέσσερα',
    'δεκαπέντε',
    'δεκαέξι',
    'δεκαεπτά',
    'δεκαοκτώ',
    'δεκαεννέα'
    ]

one_to_twenty_f = [
    'μία',
    'δύο',
    'τρεις',
    'τέσσερεις',
    'πέντε',
    'έξι',
    'επτά',
    'οκτώ',
    'εννέα',
    'δέκα',
    'έντεκα',
    'δώδεκα',
    'δεκατρείς',
    'δεκατέσσερεις',
    'δεκαπέντε',
    'δεκαέξι',
    'δεκαεπτά',
    'δεκαοκτώ',
    'δεκαεννέα'
    ]

one_to_twenty_en = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
    'ten',
    'eleven',
    'twelve',
    'thirteen',
    'fourteen',
    'fifteen',
    'sixteen',
    'seventeen',
    'eighteen',
    'nineteen'
    ]

tens = [
    'δέκα',
    'είκοσι',
    'τριάντα',
    'σαράντα',
    'πενήντα',
    'εξήντα',
    'εβδομήντα',
    'ογδόντα',
    'ενενήντα'
    ]

tens_en = [
    'ten',
    'twenty',
    'thirty',
    'forty',
    'fifty',
    'sixty',
    'seventy',
    'eighty',
    'ninety'
    ]

hundreds_n = [
    'εκατό',
    'διακόσια',
    'τριακόσια',
    'τετρακόσια',
    'πεντακόσια',
    'εξακόσια',
    'επτακόσια',
    'οκτακόσια',
    'εννιακόσια'
    ]

hundreds_f = [
    'εκατό',
    'διακόσιες',
    'τριακόσιες',
    'τετρακόσιες',
    'πεντακόσιες',
    'εξακόσιες',
    'επτακόσιες',
    'οκτακόσιες',
    'εννιακόσιες'
    ]

hundreds_en = [ x + ' hundred' for x in one_to_twenty_en[0:10]]

thousands = [
    'χίλια',
    'χιλιάδες'
    ]

thousands_en = [
    'one thousand',
    'thousand'
]

millions = [
    'εκατομμύριο',
    'εκατομμύρια'
    ]

millions_en = [
    'one million',
    'million'
]

billions = [
    'δισεκατομμύριο',
    'δισεκατομμύρια'
    ]

billions_en = [
    'one billion',
    'billion'
]

def num_to_text_hundreds(number, f, english=False):
    parts = []
    h, mod100 = divmod(number, 100)
    t, mod10 = divmod(mod100, 10)
    if english:
        one_to_twenty_arr_f = one_to_twenty_en
        one_to_twenty_arr_n = one_to_twenty_en
        hundreds_arr_f = hundreds_en
        hundreds_arr_n = hundreds_en
        tens_arr = tens_en
    else:
        one_to_twenty_arr_f = one_to_twenty_f
        one_to_twenty_arr_n = one_to_twenty_n
        hundreds_arr_f = hundreds_f
        hundreds_arr_n = hundreds_n
        tens_arr = tens
    if h > 0:
        if h == 1 and mod100 > 0 and english:
            parts.append(hundreds_arr_n[h - 1] + 'ν')
        else:
            if f == True:
                parts.append(hundreds_arr_f[h - 1])
            else:
                parts.append(hundreds_arr_n[h - 1])
    if t > 1:
        parts.append(tens_arr[t - 1])
        if mod10 > 0:
            if english:
                parts[-1] = parts[-1] + '-' + one_to_twenty_arr_f[mod10 - 1]
            elif f == True:
                parts.append(one_to_twenty_arr_f[mod10 - 1])
            else:
                parts.append(one_to_twenty_arr_n[mod10 - 1])
    elif t == 1:
        parts.append(one_to_twenty_arr_n[10 + mod10 - 1])
    elif mod10 > 0:
        if f == True:
            parts.append(one_to_twenty_arr_f[mod10 - 1])
        else:
            parts.append(one_to_twenty_arr_n[mod10 - 1])
    return ' '.join(parts)

def num_to_text_thousands(number, english=False):
    th, r = divmod(number, 1000)
    if english:
        thousands_arr = thousands_en
    else:
        thousands_arr = thousands        
    if th > 1:
        return "{0} {1} {2}".format(num_to_text_hundreds(th, True, english),
                                    thousands_arr[1],
                                    num_to_text_hundreds(r, False, english))
    elif th == 1:
        return "{0} {1}".format(thousands_arr[0],
                                num_to_text_hundreds(r, False, english))
    else:
        return num_to_text_hundreds(r, False, english)

def num_to_text_millions(number, english=False):
    m, r = divmod(number, 1000000)
    if english:
        millions_arr = millions_en
    else:
        millions_arr = millions    
    if m > 1:
        return "{0} {1} {2}".format(num_to_text_hundreds(m, False),
                                    millions_arr[1],
                                    num_to_text_thousands(r, english))
    elif m == 1:
        return "{0} {1} {2}".format(one_to_twenty_n[0],
                                    millions_arr[0],
                                    num_to_text_thousands(r, english))
    else:
        return num_to_text_thousands(number, english)

def num_to_text_billions(number, english=False):
    m, r = divmod(number, 1000000000)
    if english:
        billions_arr = billions_en
    else:
        billions_arr = billions
    if m > 1:
        return "{0} {1} {2}".format(num_to_text_hundreds(m, False),
                                    billions_arr[1],
                                    num_to_text_millions(r, english))
    elif m == 1:
        return "{0} {1} {2}".format(one_to_twenty_n[0],
                                    billions_arr[0],
                                    num_to_text_millions(r, english))
    else:
        return num_to_text_millions(number, english)
    
def num_to_text(number, english=False):
    return num_to_text_billions(number, english)

def make_percentage(number):
    percentage = "{:.2f}".format(number * 100)
    if percentage.endswith('.00'):
        percentage = percentage.replace('.00', '')
    return percentage
    
CURPATH = os.path.dirname(os.path.realpath(__file__))
default_template = os.path.join(CURPATH, 'invoice.tex')

parser = argparse.ArgumentParser(description='Invoice generator')
parser.add_argument('invoice_data')
parser.add_argument('-t', '--template', dest='template',
                    default=default_template,
                    help='use TEMPLATE as LaTeX template')
parser.add_argument('-e', '--english', dest='english',
                    action='store_true',
                    default=False,
                    help='include English output')
parser.add_argument('-b', '--build', dest='build',
                    action='store_true', default=False,
                    help='build pdf from TeX file')

def main():
    args = parser.parse_args()

    tree = ET.parse(args.invoice_data)
    root = tree.getroot()

    num = root.find('num').text
    date = root.find('date').text
    stamp = root.find('stamp').text
    client = root.find('client').text
    occupation = root.find('occupation').text
    taxoffice = root.find('taxoffice').text
    address = root.find('address').text
    taxnumber = root.find('taxnumber').text
    description = root.find('description').text
    comment = root.find('comment').text
    withholding = root.find('withholding').text
    value_f = float(root.find('value').text)
    uni_rate_el = root.find('uni_rate')
    vat_rate_el = root.find('vat_rate')
    if vat_rate_el is not None:
        vat_rate = vat_rate_el.text
    else:
        vat_rate = "0.24" # default value
    vat_rate_f = float(vat_rate)
    vat_rate_prc = make_percentage(vat_rate_f)
    if uni_rate_el is not None:
        uni_rate = uni_rate_el.text
    else:
        uni_rate = '0.07'
    uni_rate_f = float(uni_rate)
    uni_rate_prc = make_percentage(uni_rate_f)

    value = "{:.2f}".format(value_f)
    vat_element = root.find('vat')
    if vat_element is not None:
        vat_f = float(vat_element.text)
    else:
        vat_f = value_f * vat_rate_f
    total_f = value_f + vat_f
    vat = "{:.2f}".format(vat_f)
    total = "{:.2f}".format(total_f) 
    (intpart, floatpart) = total.split('.')

    numbertext = "{0} ευρώ".format(num_to_text(int(intpart)))

    uni_f = value_f * uni_rate_f
    uni = "{:.2f}".format(uni_f) 

    if args.english:
        numbertext_en = "{0} euros".format(num_to_text(int(intpart), True))
    else:
        numbertext_en = ""

    if floatpart != '' :
        floatpart_i = int(floatpart)
        if floatpart_i > 0:
            if floatpart_i > 1:
                dec_desc = 'λεπτά'
            else:
                dec_desc = 'λεπτό'
            numbertext = "{0} και {1} {2}".format(numbertext,
                                                  num_to_text(int(floatpart)),
                                                  dec_desc)
            if args.english:
                if floatpart_i > 1:
                    dec_desc = 'cents'
                else:
                    dec_desc = 'cent'            
                numbertext_en = "{0} and {1} {2}".format(numbertext_en,
                                                         num_to_text(
                                                             int(floatpart),
                                                             True),
                                                         dec_desc)

    outfn_prefix = 'invoice_%03d' % int(num)
    outfn_dir = outfn_prefix + '_build'
    os.makedirs(outfn_dir)
    outfn = outfn_prefix + '.tex'
    outfn_path = os.path.join(outfn_dir, outfn)

    with codecs.open(args.template, mode='r', encoding='utf-8') as inf:
        with codecs.open(outfn_path, mode='w', encoding='utf-8') as outf:
            for line in inf:
                line = line.replace("{{NUM}}", num)
                line = line.replace("{{DATE}}", date)
                line = line.replace("{{STAMP}}", stamp)
                line = line.replace("{{CLIENT}}", client)
                line = line.replace("{{OCCUPATION}}", occupation)
                line = line.replace("{{TAXOFFICE}}", taxoffice)
                line = line.replace("{{ADDRESS}}", address)
                line = line.replace("{{TAXNUMBER}}", taxnumber)
                line = line.replace("{{DESCRIPTION}}", description)
                line = line.replace("{{VALUE}}", value)
                line = line.replace("{{COMMENT}}", comment)
                line = line.replace("{{WITHHOLDING}}", withholding)
                line = line.replace("{{VATRATE}}", vat_rate_prc)
                line = line.replace("{{VAT}}", vat)
                line = line.replace("{{TOTAL}}", total)
                line = line.replace("{{NUMBERTEXT}}",
                                    numbertext.decode('utf-8').capitalize())
                line = line.replace("{{NUMBERTEXTEN}}",
                                    numbertext_en.decode('utf-8').capitalize())
                line = line.replace("{{UNIRATE}}", uni_rate_prc)
                line = line.replace("{{UNI}}", uni)

                outf.write(line)

    print "Wrote %s" % outfn

    if args.build:
        subprocess.call(["xelatex", outfn], cwd=outfn_dir)
        pdffn = outfn_prefix + ".pdf"
        print "Wrote pdf file %s" % os.path.join(outfn_dir, pdffn)

if __name__ == "__main__":
    main()
