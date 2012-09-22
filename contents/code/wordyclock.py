'''
The MIT License

Copyright (c) 2011 Ken Lim - http://kenlim.github.com/pyWordyClock/
2012 - Adapted by Biel Frontera <biel.fb@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

'''

import re
from time import localtime

clockFace = {}

clockFace ['en'] = """\
ITLISXABOUT
ACQUARTERDC
TWENTYRFIVE
HALFBTENFTO
PASTEKSNINE
ONESIXTHREE
FOURFIVETWO
EIGHTELEVEN
TENMIDNIGHT
SEVENTYNOON"""

clockFace ['ca_ma'] = """\
ESONELAULES
DUESTRESUNA
QUATRECINCF
SISOASETJEN
VUITANOUYOB
LADEUDSONZE
DOTZEIMENOS
IOVINTEDEUP
VINT-I-CINC
MITJAAQUART"""

clockFace ['es'] = """\
ESONELASUNA
DOSITRESORE
CUATROCINCO
SEISASIETEN
OCHONUEVEYO
LADIEZSONCE
DOCELYMENOS
OVEINTEDIEZ
VEINTICINCO
MEDIACUARTO"""

hourNames = {}

hourNames['en'] = {   0 : 'midnight',
                1 : 'one',
                2 : 'two',
                3 : 'three',
                4: 'four',
                5: 'five',
                6: 'six',
                7 : 'seven',
                8: 'eight',
                9: 'nine',
                10: 'ten',
                11: 'eleven',
                12: 'noon',
                13 : 'one',
                14 : 'two',
                15 : 'three',
                16: 'four',
                17: 'five',
                18: 'six',
                19 : 'seven',
                20: 'eight',
                21: 'nine',
                22: 'ten',
                23: 'eleven',
                24: 'midnight'
            }
            
hourNames['ca_ma'] = {   0 : 'les dotze',
                1 : 'la una',
                2 : 'les dues',
                3 : 'les tres',
                4: 'les quatre',
                5: 'les cinc',
                6: 'les sis',
                7 : 'les set',
                8: 'les vuit',
                9: 'les nou',
                10: 'les deu',
                11: 'les onze',
                12: 'les dotze',
                13 : 'la una',
                14 : 'les dues',
                15 : 'les tres',
                16: 'les quatre',
                17: 'les cinc',
                18: 'les sis',
                19 : 'les set',
                20: 'les vuit',
                21: 'les nou',
                22: 'les deu',
                23: 'les onze',
                24: 'les dotze'
            }
            
hourNames['es'] = {   0 : 'las doce',
                1 : 'la una',
                2 : 'las dos',
                3 : 'las tres',
                4: 'las cuatro',
                5: 'las cinco',
                6: 'las seis',
                7 : 'las siete',
                8: 'las ocho',
                9: 'las nueve',
                10: 'las diez',
                11: 'las once',
                12: 'las doce',
                13 : 'la una',
                14 : 'las dos',
                15 : 'las tres',
                16: 'las cuatro',
                17: 'las cinco',
                18: 'las seis',
                19 : 'las siete',
                20: 'las ocho',
                21: 'las nueve',
                22: 'las diez',
                23: 'las once',
                24: 'las doce'
            }
            
            
minuteNames = {}            

minuteNames['en'] = { 0: None,
                5: 'five past',
                10: 'ten past',
                15:'a quarter past',
                20:'twenty past',
                25: 'twenty five past',
                30: 'half past',
                35: 'twenty five to',
                40:'twenty to',
                45: 'a quarter to',
                50: 'ten to',
                55: 'five to'
            }
            
minuteNames['ca_ma'] = { 0: None,
                5: 'i cinc',
                10: 'i deu',
                15:'i quart',
                20:'i vint',
                25: 'i vint-i-cinc',
                30: 'i mitja',
                35: 'menos vint-i-cinc',
                40:'menos vint',
                45: 'menos quart',
                50: 'menos deu',
                55: 'menos cinc'
            }            
            
minuteNames['es'] = { 0: None,
                5: 'y cinco',
                10: 'y diez',
                15:'y cuarto',
                20:'y veinte',
                25: 'y veinticinco',
                30: 'y media',
                35: 'menos veinticinco',
                40:'menos veinte',
                45: 'menos cuarto',
                50: 'menos diez',
                55: 'menos cinco'
            }    
            
def roundToClosest5Minutes(hour, minutes):
    minutes = round(minutes / 5.0) * 5
    if minutes == 60:
        return (hour +1, 0)
    else:
        return (hour, minutes)

def constructString(minutesRelativeTo, hour, lang='en'):
    if lang=='ca_ma' or lang=='es':
        components = ["son", hourNames[lang][hour],minuteNames[lang][minutesRelativeTo]]
    else:   
        components = ["it is", minuteNames[lang][minutesRelativeTo], hourNames[lang][hour]]
    return " ".join([x for x in components if x != None])

def convertToWords(hour, minutes, lang='en'):
    if minutes > 30:
        return constructString(minutes, hour + 1,lang)
    else:
        return constructString(minutes, hour,lang)

def convertToRegex(string):
    return ".*" + ".*".join(["(" + x + ")" for x in string.split(" ")]) + ".*"


def blankOutTargetFromBase(target, baseString):
    targetRegex = convertToRegex(target)
    blankedString = re.sub(".", " ", baseString)

    matcher = re.match(targetRegex, baseString, re.DOTALL)
    outputArray = list(blankedString)

    for x in range(1, len(matcher.groups()) +1):
        outputArray[matcher.start(x) : matcher.end(x)] = [y for y in matcher.group(x)]

    return "".join(outputArray)



def main():
    clock = localtime()
    hour, minutes = roundToClosest5Minutes(clock.tm_hour, clock.tm_min)

    wordyTime = convertToWords(hour, minutes)
    print blankOutTargetFromBase(wordyTime.upper(), clockFace['en'])
    return 0

def otherMain():
    print clockFace['en']
    return 0

