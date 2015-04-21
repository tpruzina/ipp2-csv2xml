#!/bin/env python3.2
# -*- coding: utf-8 -*-

import argparse, sys
import _csv as csv_sys
import re
import copy

class csv2xml:    
    global opts
    global header
    global ret
    global input_csv
    global output_xml
    
    def __init__(self):
        self.ret = 0
        self.header = '<?xml version="1.0" encoding="UTF-8"?>\n'
        self.opts = self.parse_cmdline()
                        
        
        if self.opts.validate == True:
            ret = self.validate()
        else:
            ret = self.csv2xml(self.opts)

        return
    
    def __del__(self):
        #close(self.opts.output)
        #close(self.opts.input)
        pass

    def csv2xml(self, opts):
        nr_lines = 0
        nr_cols = 0
        
    # PREPARSING
        # we are gonna be parsing twice, make a shallow copy of memory backed file
        tmp = copy.copy(self.opts.input)
        tmp_csv = csv_sys.reader(tmp,delimiter=self.opts.separator, quotechar='"')
        for row in tmp_csv:
            if nr_cols == 0:
                nr_cols = len(row)
            nr_lines += 1
        
        del tmp_csv
        del tmp
        
    # MAIN PARSING
        input_csv = csv_sys.reader(self.opts.input, delimiter=self.opts.separator, quotechar='"')
        output_xml = ''

        # ic = indent counter
        ic = 0
        
        if opts.n_switch == False:
            output_xml += self.header
            
        if opts.root_element != None:
            if (None != re.match('[^\w:_.].*$', opts.root_element)) or (None != re.match('^[0-9].*$', opts.root_element)) or (None != re.match('[^\w:_.].*$', opts.root_element)):
                self.error("error 30: invalid root element <"+opts.root_element, 30)
                
            output_xml += '<{:s}>\n'.format(opts.root_element)
            ic += 1
        
        # -h=subst handling  
        if opts.subst != None:
            nr_lines -= 1   #since we ignore first line, decrease this counter
            col_names = next(input_csv)
            
            col_names = [s.replace(' ', opts.subst) for s in col_names]
            col_names = [s.replace(',', opts.subst) for s in col_names]
            col_names = [s.replace('\n', opts.subst) for s in col_names]
            col_names = [s.replace('\r', opts.subst) for s in col_names]
            
        
        if opts.subst == None: 
            col_names = []
            for x in range(1, nr_cols+3):
                col_names.append('{:s}{:d}'.format(opts.column_element, x))
        
        # check for invalid values
        for x in col_names:
            if None != re.match('[^\w:_.].*$', x):
                self.error("error 31: invalid element <"+x, 31)
        
        # main loop    
        for row in input_csv:
            output_xml += '{:s}<{:s}{:s}>\n'.format(
                                          self.indent(ic), 
                                          opts.line_element, 
                                          self.lindex()
                                        )
            # if row contains more/less columns than it should and error_recovery is false
            if len(row) != nr_cols and opts.error_recovery == False:
                self.error('too many columns (neresim)', 32)
            
            # cc = column counter
            cc = 1
            
            #column loop
            for col in row:
#                 print(row)
                # don't output more than we have to (in case of recovery, otherwise, we have exited by now)
                if cc <=nr_cols or opts.all_collumns:
                    if cc <= nr_cols:
                        col_name = col_names[cc-1]
                    elif opts.all_collumns == True:
                        col_name = '{:s}{:d}'.format(opts.column_element, cc)
                        
                    output_xml += '{:s}<{:s}>\n'.format(self.indent(ic+1), col_name)
                    output_xml += self.convert_metacharacters('{:s}{:s}\n'.format(self.indent(ic+2), col))
                    output_xml += '{:s}</{:s}>\n'.format(self.indent(ic+1), col_name)
                
                cc += 1
            
            # insert extra empty columns if recovery is enabled
            if opts.all_collumns == True:
                for x in range(cc, nr_cols+1):
                    output_xml += '{:s}<{:s}{:d}>\n'.format(self.indent(ic+1), opts.column_element, x)
                    output_xml += self.convert_metacharacters('{:s}{:s}\n'.format(self.indent(ic+2), opts.missing_field))
                    output_xml += '{:s}</{:s}{:d}>\n'.format(self.indent(ic+1), opts.column_element, x)
            
            
            output_xml += '{:s}</{:s}>\n'.format(self.indent(ic), opts.line_element)
        
        if opts.root_element != None:
            output_xml += '</{:s}>\n'.format(opts.root_element)
            
        print(output_xml, end='', file=opts.output)
        
        
        
        
        return 0
    
    # returns formatted string " indexN"
    def lindex(self):
        if self.opts.index == True:
            s = ' index="{:d}"'.format(self.opts.start_n)
            self.opts.start_n += 1
        else:
            s = ''
        return s

    def validate(self):
        return 0
    
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
        return s

    def n_char_padding_required(self, number):
        i = 1
        while (number/10) >= 1:
            i = i+1
            number = number / 10
        return i
    
    # command line argument parsing
    def parse_cmdline(self):
        args = argparse.ArgumentParser(add_help=False)

        args.add_argument('--help', action='help')
        args.add_argument('--input', dest='input', help='Input file with UTF-8 formatted CSV data')
        args.add_argument('--output', dest='output', help='Output file (XML data)')
        args.add_argument('-n', action='store_true', default=False, dest='n_switch', help='Don\'t generate XML header onto output')
        args.add_argument('-r', action='store', dest='root_element', help='Element encapsulating output')
        args.add_argument('-s', action='store', dest='separator', help='Modify input separator')
        
        args.add_argument('-h', action='store', dest='subst', nargs='?', const='-', help='First line serves as header')
        
        args.add_argument('-c', action='store', dest='column_element', help='Modify  column-elementX prefix')
        args.add_argument('-l', action='store', dest='line_element', help='Modify line element')
        args.add_argument('-i', action='store_true', dest='index', default=False, help='insert attribute index into line-element')
        args.add_argument('--start', action='store', dest='start_n', type=int, help='initial index value')
        args.add_argument('--error-recovery', '-e', action='store_true', default=False, dest='error_recovery')
        args.add_argument('--all-columns', action='store_true', dest='all_collumns', default=False, help='don\'t ignore extra columns in recovery mode')
        args.add_argument('--missing-field', action='store', dest='missing_field', help='missing field filler')
        args.add_argument('--padding', action='store_true', default=False, dest='pad', help='Provide compact output')
        args.add_argument('--validate', action='store_true', default=False, dest='validate', help='Validate input CSV')
        
        res = args.parse_args()
        
        # -r=root-element
        if res.root_element != None:
            self.validate_xml_tag(res.root_element)

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
            self.validate_xml_tag(res.column_element)
        
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
            self.validate_xml_tag(res.line_element)
           
        
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
                
        if res.input == None:
            res.input = sys.stdin
        else:
            try:
                res.input = open(res.input, mode='r', newline='', encoding='utf-8')
            except IOError:
                self.error("couldn't open file for reading", 2)
            
        if res.output == None:
            res.output = sys.stdout
        else:
            try:
                res.output = open(res.output, mode='w', newline='', encoding='utf-8')
            except IOError:
                self.error("couldn't open file for writing", 3)
            
        res.input = res.input.readlines()
            
        return res
    
    def validate_xml_tag(self, s):
        
        #self.error("Invalid XML tag", 30)
        return True
    
    def error(self, msg, ret=-1):
        print(msg, file=sys.stderr)
        sys.exit(ret)

c2x = csv2xml()
exit(c2x.ret)
