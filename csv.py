#!/bin/env python3.2
# -*- coding: utf-8 -*-
#CSV:xpruzi01

import argparse, sys
import _csv as csv_sys
import re
import copy

#main class
class csv2xml:    
    global opts
    global header
    global input_csv
    global output_xml
    
    global pad_lines
    global pad_cols
    
    def __init__(self):
        self.header = '<?xml version="1.0" encoding="UTF-8"?>\n'
        
        #parse commandline
        self.opts = self.parse_cmdline()
        
        # execute conversion
        self.csv2xml(self.opts)

        return
    
    def __del__(self):
        #close(self.opts.output)
        #close(self.opts.input)
        pass

    # main program
    def csv2xml(self, opts):
        nr_lines = 0
        nr_cols = 0
        
    # PREPARSING
        # we are gonna be parsing twice, make a shallow copy of memory backed file
        tmp = copy.copy(self.opts.input)
        
        try:
            tmp_csv = csv_sys.reader(tmp,delimiter=self.opts.separator, quotechar='"')
        
            self.pad_cols = []
            
            for row in tmp_csv:
                if nr_cols == 0:
                    nr_cols = len(row)
                
                #if all columns are defined, take bigger of number of columns on a row and
                # number of columns on first row of CSV
                if opts.all_collumns == True:
                    self.pad_cols.append(self.n_char_padding_required(max(len(row), nr_cols)))
                # otherwise try to get minimal value
                else:
                    self.pad_cols.append(self.n_char_padding_required(min(len(row), nr_cols)))         
                nr_lines += 1
            
            # calculate number of digits required to pad lines (only used if --pading was specified)
            self.pad_lines = self.n_char_padding_required(nr_lines)
        except csv_sys.Error:
            self.error("invalid input file format", 4)
            
        #cleanup
        del tmp_csv
        del tmp
        
    # MAIN PARSING
        input_csv = csv_sys.reader(self.opts.input, delimiter=self.opts.separator, quotechar='"')
        output_xml = ''

        # ic = indent counter
        ic = 0
        
        #XML HEADER
        if opts.n_switch == False:
            output_xml += self.header
        
        #ROOT ELEMENT
        if opts.root_element != None:
            self.validate_xml_root_tag(opts.root_element)
                
            output_xml += '<{:s}>\n'.format(opts.root_element)
            ic += 1
        
        #CSV HEADER HANDLING
        # -h=subst handling  
        if opts.subst != None:
            nr_lines -= 1   #since we ignore first line, decrease this counter
            col_names = next(input_csv)
            
            if len(col_names) == 0:
                self.error("first line cannot be empty if -h was specified!", 31)
            
            col_names = [s.replace(' ', opts.subst) for s in col_names]
            col_names = [s.replace(',', opts.subst) for s in col_names]
            col_names = [s.replace('\n', opts.subst) for s in col_names]
            col_names = [s.replace('\r', opts.subst) for s in col_names]
            
        
        #prepare column names into array so they don't have to be generated inside loop
        if opts.subst == None: 
            col_names = []
            for x in range(1, nr_cols+3):
                col_names.append('{:s}{:d}'.format(opts.column_element, x))
        
        # check for invalid values in prepared column fields
        for x in col_names:
            if None != re.match('[^\w:_.].*$', x):
                self.error("error 31: invalid element <"+x, 31)
        
        # row counter, needed for padding
        rc = 0
        
        # main loop - read line from CSV
        for row in input_csv:
            # print <line element>
            output_xml += '{:s}<{:s}{:s}>\n'.format(
                                          self.indent(ic), 
                                          opts.line_element, 
                                          self.lindex()
                                        )
            # if row contains more/less columns than it should and error_recovery is false
            if len(row) != nr_cols and opts.error_recovery == False:
                self.error('too many columns (neresim)', 32)
            
            # cc = column counter, needed for padding, numbering
            cc = 1
            
            #column loop
            for col in row:
                # don't output more than we have to (in case of recovery, otherwise, we have exited by now)
                if cc <=nr_cols or opts.all_collumns:
                    # format column name according to rules
                    if cc <= nr_cols:
                        if opts.padding == False:
                            col_name = col_names[cc-1]
                        else:
                            col_name = '{:s}{:s}'.format(opts.column_element, self.pad_number(cc, self.pad_cols[rc]))
                    elif opts.all_collumns == True:
                        col_name = '{:s}{:s}'.format(opts.column_element, self.pad_number(cc,self.pad_cols[rc]))
                        
                    #forge string and output
                    output_xml += '{:s}<{:s}>\n'.format(self.indent(ic+1), col_name)
                    output_xml += self.convert_metacharacters('{:s}{:s}\n'.format(self.indent(ic+2), col))
                    output_xml += '{:s}</{:s}>\n'.format(self.indent(ic+1), col_name)
                
                cc += 1
            
            # insert extra empty columns if recovery is enabled
            if opts.all_collumns == True:
                for x in range(cc, nr_cols+1):
                    if cc <= nr_cols:
                        insert_column = col_names[x-1]
                    else:
                        insert_column = '{:s}{:s}'.format(opts.column_element, self.pad_number(x,self.pad_cols[rc]))

                    output_xml += '{:s}<{:s}>\n'.format(self.indent(ic+1), insert_column)
                    output_xml += self.convert_metacharacters('{:s}{:s}\n'.format(self.indent(ic+2), opts.missing_field))
                    output_xml += '{:s}</{:s}>\n'.format(self.indent(ic+1), insert_column)
            
            #print closing </line element>
            output_xml += '{:s}</{:s}>\n'.format(self.indent(ic), opts.line_element)
            
            #increment row counter
            rc += 1
        
        if opts.root_element != None:
            output_xml += '</{:s}>\n'.format(opts.root_element)
            
        print(output_xml, end='', file=opts.output)
        

        return 0
    
    # returns formatted string " indexN"
    def lindex(self):
        if self.opts.index == True:
            s = ' index="{:s}"'.format(self.pad_number(self.opts.start_n, self.pad_lines))
            self.opts.start_n += 1
        else:
            s = ''
        return s

    
    def indent(self, n):
        #str = '\t' * n
        s = '    ' * n
        return s

    def convert_metacharacters(self, s):
        s = s.replace("&", "&amp;")
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
#         s = s.replace("\'", "&apos;")
        s = s.replace('\"', "&quot;")
        s = s.replace('\r', '')
        return s

    def n_char_padding_required(self, number):
        i = 1
        while (number/10) >= 1:
            i = i+1
            number = number / 10
        return i
    
    def pad_number(self, n, pad_to=0):
        s='{:d}'.format(n)
        if self.opts.padding == True:
            s= s.zfill(pad_to)
        return s
        
    
    # command line argument parsing
    def parse_cmdline(self):
        # create parser object
        args = argparse.ArgumentParser(add_help=False)

        # add arguments for all the options
        args.add_argument('--help', action='store_true', default=False, dest='help')
        args.add_argument('--input', dest='input', help='Input file with UTF-8 formatted CSV data')
        args.add_argument('--output', dest='output', help='Output file (XML data)')
        args.add_argument('-n', action='store_true', default=False, dest='n_switch', help='Don\'t generate XML header onto output')
        args.add_argument('-r', action='store', dest='root_element', help='Element encapsulating output')
        args.add_argument('-s', action='store', dest='separator', help='Modify input separator')
        args.add_argument('-h', action='store', dest='subst', nargs='?', const='-', help='First line serves as header')
        args.add_argument('-c', action='store', dest='column_element', help='Modify  column-elementX prefix')
        args.add_argument('-l', action='store', dest='line_element', nargs='?', const='row', help='Modify line element')
        args.add_argument('-i', action='store_true', dest='index', default=False, help='insert attribute index into line-element')
        args.add_argument('--start', action='store', dest='start_n', type=int, help='initial index value')
        args.add_argument('--error-recovery', '-e', action='store_true', default=False, dest='error_recovery')
        args.add_argument('--all-columns', action='store_true', dest='all_collumns', default=False, help='don\'t ignore extra columns in recovery mode')
        args.add_argument('--missing-field', action='store', dest='missing_field', help='missing field filler')
        args.add_argument('--padding', action='store_true', default=False, dest='padding', help='Provide compact output')        
        # execute parsing
        res = args.parse_args()
        
        #fix all interdependencies
        if res.help == True:
            if len(sys.argv) == 2:
                args.print_help()
                sys.exit(0)
            else:
                self.error("--help expects it to be only argument given.", 1)
        
        if res.index == True and res.line_element == None:
            self.error("-i must come with -l", 1)

        if res.start_n != None:
            if res.index == False or res.line_element == None:
                self.error("--start=n requires -i, -l", 1)
        
        #don't allow multiple arguments of same thing
        argcopy = []
        for s in sys.argv:
            argcopy.append(re.sub('--error-recovery', '-e', re.sub('\=.*$','', s)))
        if len(argcopy) != len(set(argcopy)):
            self.error("argument given more than once", 1)
        
        
        # -r=root-element
        if res.root_element != None:
            self.validate_xml_root_tag(res.root_element)

        # -s=separator
        if res.separator == None:
            res.separator = ','
        elif res.separator == 'TAB':
            res.separator='\t'
        elif res.separator.__len__() != 1:
            self.error("separator should consist of single character", 1)
        
        # -h=subst
        if res.subst != None:
            pass    #todo checking
 
        # -c=column-element
        if res.column_element == None:
            res.column_element = 'col'
        else:
            pass
            #self.validate_xml_col_tag(res.column_element)
        
        # -start=n
        if res.start_n == None:
            res.start_n = 1
        else:
            if res.start_n < 0:
                self.error("--start=n expects n >= 0")
            if res.index == None or res.line_element == None:
                self.error("--start=n expects to be run with -i and -l", 1)
        
        # -i=n
        if res.index == True and res.line_element == None:
                self.error("-i requires -l=line-element to be defined", 1)
        
        # -l=line-element
        if res.line_element == None:
            res.line_element = 'row'
        else:
            self.validate_xml_line_tag(res.line_element)
           
        
        if res.missing_field != None:
            if res.error_recovery == False:
                self.error('Missing field only allowed together with --error-recovery!', 1)
            else:
                res.missing_field = self.convert_metacharacters(res.missing_field)
        
        if res.error_recovery == True:
            if res.missing_field == None:
                res.missing_field = ''
        
        if res.all_collumns == True:
            if res.error_recovery == False:
                self.error('--all-columns only allowed together with --eror-recovery!', 1)
                
                
        # open input file & load it into memory
        if res.input == None:
            res.input = sys.stdin
        else:
            try:
                res.input = open(res.input, mode='r', newline='', encoding='utf-8')
            except IOError:
                self.error("couldn't open file for reading", 2)
        
        res.input = res.input.readlines()

        #open output file
        if res.output == None:
            res.output = sys.stdout
        else:
            try:
                res.output = open(res.output, mode='w', newline='', encoding='utf-8')
            except IOError:
                self.error("couldn't open file for writing", 3)
            
        #return parser object with values    
        return res
    
    def validate_xml_root_tag(self,s):
        if  None != re.match('^[^\w:_].*$', s)  or \
            None != re.match('^[0-9].*$', s)    or \
            None != re.match('[^\w:_\.\-]', s)  :
                self.error("error 30: invalid root element <"+s, 30)
        return
        
    def validate_xml_line_tag(self, s):
        if  None != re.match('^[^\w:_].*$',s)   or \
            None != re.match('^[0-9].*$', s)    or \
            None != re.match('[^\w:_\.\-]', s)  :
                self.error("error 30: invalid element <"+opts.root_element, 30)
        return
    
    # todo: implement & rewrite in csv2xml()
    def validate_xml_col_tag(self,s):
        if  None != re.match('^[^\w:_].*$',s)   or \
            None != re.match('^[0-9].*$', s)    or \
            None != re.match('[^\w:_\.\-]', s)  :
                self.error("error 30: invalid element <"+opts.root_element, 30)
        return
    
    def error(self, msg, ret=-1):
        print(msg, file=sys.stderr)
        sys.exit(ret)

if __name__ == "__main__":
    c2x = csv2xml()
    exit(0)
