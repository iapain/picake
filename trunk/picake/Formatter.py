"""
PI string formatter (dynamic)
PI cake PI computation project
Author: Deepak Thukral
MiNI 2008 Politehcnika Warsaw
"""

import sys

class TextFormatter:
    ''' Formats file in readable order '''
    def __init__(self, text, blocks_per_line=10, digits_per_block=6, rows_per_block=20, row_tabs=2, col_tabs=1, show_count=True):
        self.text = text[2:]
        self.blocks_per_line = blocks_per_line
        self.digits_per_block = digits_per_block
        self.rows_per_block = rows_per_block
        self.row_tabs = row_tabs
        self.col_tabs = col_tabs
        self.show_count = show_count
        self.format_text = ['3.\n']
        
    def format(self):
        b = 0
        r = 0
        cnt = 0
        buff = ''
        prev = 0
        for i in self.text:
            buff += i
            cnt += 1
            if cnt*2 == self.digits_per_block:
                buff+=' '
            if cnt == self.digits_per_block:
                if b < self.blocks_per_line - 1:
                    for j in range(self.col_tabs):
                        buff+='\t'
                    b += 1
                    cnt = 0
                else:
                    if self.show_count:
                        prev += len(buff) - (self.blocks_per_line - 1)*2*self.col_tabs - 1
                        self.format_text.append(buff + ' : ' + str(prev))
                    else:
                        self.format_text.append(buff)
                    self.format_text.append('\n')
                    buff = ''
                    b = 0
                    r += 1
                    cnt = 0
                    
            if r == self.rows_per_block - 1:
                for j in range(self.row_tabs):
                    if sys.platform == 'linux2':
                        self.format_text.append('\n')
                    else:
                        self.format_text.append('\n') 
                r = 0
        self.format_text.append(buff)   
        return self.format_text 

"""
a = TextFormatter('122323123123712387821763781263876218736126531213211111131712532135875875765765765765765765765765765765555555555555555555555555555567666666666666')
print a.format()
"""
