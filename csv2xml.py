import argparse, sys
import _csv as csv_sys
import xml

class csv2xml:    
    global args
    global header
    global ret
    global input_csv
    global output_xml
    
    def __init__(self):
        self.ret = 0
        
        self.header = '<?xml version="1.0" encoding="UTF-8"?>'

        opts = self.parse_cmdline()
        
        input_csv = csv_sys.reader(opts.input, delimiter=opts.separator, quotechar='|')
        
        # paddiig here
#         for row in input_csv:
#             print(', '.join(row))
                
        
        if opts.validate == True:
            ret = self.validate()
        else:
            ret = self.csv2xml(opts, input_csv)

        return

    def csv2xml(self, opts, input_csv):
        
        i = 0
        
        if opts.n_switch == False:
            print(self.header, file=opts.output)
            
        if opts.root_element != None:
            print('<{:s}>'.format(opts.root_element), file=opts.output)
            i += 1
            
        # main loop    
        for row in input_csv:
            #print(row)
            print('{:s}<{:s}>'.format(self.indent(i), opts.line_element), file=opts.output)
            
            j = 1
            for col in row:
                print('{:s}<{:s}{:d}>'.format(self.indent(i+1), opts.column_element, j), file=opts.output)
                
                print('{:s}{:s}'.format(self.indent(i+2), col), file=opts.output)
                
                print('{:s}</{:s}{:d}>'.format(self.indent(i+1), opts.column_element, j), file=opts.output)
                j += 1
                
            
            print('{:s}</{:s}>'.format(self.indent(i), opts.line_element), file=opts.output)
        
        if opts.root_element != None:
            print('</{:s}>'.format(opts.root_element), file=opts.output)
        
        
        
        
        return 0

    def validate(self):
        return 0
    
    def indent(self, n):
        str = '\t' * n
        return str

    def convert_metacharacters(self, s):
        s = s.replace("&", "&amp")
        s = s.replace("<", "&lt")
        s = s.replace(">", "&gt")
        s = s.replace("\'", "&apos")
        s = s.replace("\"", "&quot")
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
        args.add_argument('-h', action='store', dest='subst', nargs='?', default='not given', help='First line serves as header')
        args.add_argument('-c', action='store', dest='column_element', help='Modify  column-elementX prefix')
        args.add_argument('-l', action='store', dest='line_element', help='Modify line element')
        args.add_argument('-i', action='store_true', dest='index', default=False, help='insert attribute index into line-element')
        args.add_argument('--start', action='store', dest='start_n', type=int, help='initial index value')
        args.add_argument('--error-recovery', '-e', action='store_true', default=False, dest='error_recovery')
        args.add_argument('--missing-field=', action='store', dest='missing_field', help='missing field filler')
        args.add_argument('--all-columns', action='store_true', default=False, help='don\'t ignore extra columns in recovery mode')
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
            self.error("separator should consist of single character", -1)
        
        # -h=subst
        if res.subst == None:
            res.subst = '-'
        # -h argument not present
        if res.subst == 'not given':
            res.subst = None
            
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
                self.error("--start=n expects to be run with -i and -l")
        
        # -i=n
        if res.index == True and res.line_element == None:
                self.error("-i requires -l=line-element to be defined")
        
        # -l=line-element
        if res.line_element == None:
            res.line_element = 'row'
        else:
            self.validate_xml_tag(res.line_element)
           
        
        if res.missing_field != None:
            if res.error_recovery == False:
                self.error('Missing field only allowed together with --error-recovery!')
            else:
                res.missing_field = self.convert_metacharacters(res.missing_field)
        
        if res.error_recovery == True:
            if res.missing_field == None:
                res.missing_field = ''
        
        if res.all_columns == True:
            if res.error_recovery == False:
                self.error('--all-columns only allowed together with --eror-recovery!')
                
        if res.input == None:
            res.input = sys.stdin
        else:
            res.input = open(res.input, mode='r', encoding='utf-8')
            #todo handilng
            
        if res.output == None:
            res.output = sys.stdin
        else:
            res.output = open(res.output, mode='w', encoding='utf-8')
            #todo: handling
        return res
    
    def validate_xml_tag(self, s):
        
        #self.error("Invalid XML tag", 30)
        return True
    
    def error(self, msg, ret=-1):
        print(msg, file=sys.stderr)
        sys.exit(ret)


c2x = csv2xml()
exit(c2x.ret)
