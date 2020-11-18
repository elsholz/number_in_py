#!/usr/bin/python3
import sys
import math
import colorama
import zipfile

colorama.init()
number = sys.argv[1]
pn = bytearray(number, 'utf-8')
print(f'Searching for the following number: {number}')
print('Progress'.ljust(15), 'Digits'.ljust(25), '10^x'.ljust(15))
zfile = zipfile.ZipFile('./pi.zip')
finfo = zfile.infolist()[0]
with zfile.open(finfo) as pi:
    o = len(number) - 1
    overhang = b''
    previous_content = b''
    base_index = 0
    byte_count = 8192
    # remove the first digit and the decimal point
    pi.read(2)
    while True:
        try:
            content = pi.read(byte_count*64)
            if not content:
                print()
                print(colorama.asni.Fore.RED, 'Reached end of file, number was not found.',
                        colorama.ansi.Fore.RESET, sep='')
                quit()
            if pn in overhang + content:
                # index of the start of the phoine number in the current content
                res = (overhang+content).index(pn)
                #print(res)
                # 50 neighboring digits
                # TODO: Edge case that the phone number is directly at the beginning
                # center_ind: the index of the center of the phone number within the string
                # of previous_content and content concatinated
                center_ind = len(previous_content) - len(overhang) + res + len(number)//2

                #print(center_ind)
                neighbors = (previous_content + content)[center_ind-25:center_ind+25+len(number)]
                res = base_index - len(overhang) + res
                l = colorama.ansi.Back.GREEN + ' '*(50+len(number)) + colorama.ansi.Back.RESET
                print('\n')
                print(l)
                print(colorama.ansi.Fore.GREEN,f'Your Number was found in Pi! The probability for that to\nhappen is roughly {round((1 - (1 - 0.1 ** len(str(number))) ** (res+1))*100, 4)}%!', 
                        colorama.ansi.Fore.RESET, sep='')
                print(f'The index that {number} starts at is: {res:,}.\nThat is the decimal digits {res+1:,} to {res+len(number)+1:,}.')
                starting_point = 25 - len(number) // 2
                ending_point = starting_point+len(number)
                print(colorama.ansi.Fore.YELLOW, neighbors[:starting_point].decode('utf-8'), 
                        colorama.ansi.Fore.MAGENTA, neighbors[starting_point:ending_point].decode('utf-8'),  
                    colorama.ansi.Fore.RESET, colorama.ansi.Fore.YELLOW, neighbors[ending_point:].decode('utf-8'), colorama.ansi.Fore.RESET, sep='')
                print(colorama.ansi.Fore.GREEN, ' '*starting_point, '^', ' '*(len(number)-2), '^', sep='')
                print(l)
                print()
                quit()
            
            if (base_index // 8192) % (128  ) == 0:
                print('\r',' '*15 + f'{base_index}'.ljust(25) + str(math.log10(base_index+1))[:5].ljust(15), end='')

            base_index += byte_count 
            overhang = content[:o]
            previous_content = content
        except Exception as e:
            print()
            print(e)
            quit()

