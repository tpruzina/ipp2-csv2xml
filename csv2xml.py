import argparse, sys
import csv
from pyparsing import Empty

class csv2xml:    
    global args
    global header
    
    def __init__(self):
        self.ret = 0
        
        self.header = '<?xml version="1.0" encoding="UTF-8"?>'

        args = self.parse_cmdline()
        
        #print(self.convert_metacharacters("&'<>"))
        #print(self.args.separator)

        return

    def parse_input(self):
        return -1

    def validate(self):
        return -1

    def convert_metacharacters(self, s):
        s = s.replace("&", "&amp")
        s = s.replace("<", "&lt")
        s = s.replace(">", "&gt")
        s = s.replace("\'", "&apos")
        s = s.replace("\"", "&quot")
        return s

    
    # command line argument parsing
    def parse_cmdline(self):
        args = argparse.ArgumentParser(add_help=False)

        args.add_argument('--help', action='help')
        
        args.add_argument('--input', dest='input', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Input file with UTF-8 formatted CSV data')
        args.add_argument('--output', dest='output', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Output file (XML data)')
        
        
        args.add_argument('-n', action='store_true', default=False, dest='n_switch', help='Don\'t generate XML header onto output')
        
        args.add_argument('-r', action='store', dest='root_element', nargs='?', default='not given', help='Element encapsulating output')
        args.add_argument('-s', action='store', dest='separator',  nargs='?', default='not given', help='Modify input separator')
        args.add_argument('-h', action='store', dest='subst', nargs='?', default='not given', help='First line serves as header')
        args.add_argument('-c', action='store', nargs='?', dest='column_element', default='not given', help='Modify  column-elementX prefix')
        args.add_argument('-l', action='store', dest='line_element', default='row', help='Modify line element')
        args.add_argument('-i', action='store', dest='index', default='-1', type=int, help='index atrtibute')
        args.add_argument('--start', action='store', dest='start_n', default=1, type=int, help='initial index value')
        args.add_argument('--error-recovery', '-e', action='store_true', default=False, dest='error_recovery')
        args.add_argument('--missing-field', action='store', default='', help='missing field filler')
        args.add_argument('--padding', action='store_true', default=False, dest='pad', help='Provide compact output')
        args.add_argument('--validate', action='store_true', default=False, dest='validate', help='Validate input CSV')
        
        res = args.parse_args()
        
      
        # -r=root-element
        if res.root_element != None:
            self.validate_xml_tag(res.root_element)

        # -s=separator
        if res.separator == 'not given':
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
        if res.column_element == 'not given':
            res.column_element = 'col'
        
        
        
        # handle columnt element
        if res.column_element != None:
            self.error('todo')
            
        
            

        #print(args.parse_args())
        return res
    
    def validate_xml_tag(self, s):
        
        #self.error("Invalid XML tag", 30)
        return True
    
    def error(self, msg, ret=-1):
        print(msg, file=sys.stderr)
        sys.exit(ret)
    
#     def help(self):
#         #print("ARGUMENT OPTIONS:")
#         #print("--help\t\t\t This message")
#         #print("--input=filename\t Input file with UTF-8 formatted CSV data")
#         # print("--output=filename\t Output file (XML data)")
#         #print("-n\t\t\t Don't generate XML header onto output")
#         # print("-r=root-element\t\t Element encapsulating output")
#         #print("-s=separator\t\t modify input separator")
#         #print("-h=subst\t\t First line serves as header")
#         #print("-c=column-element\t TODO")
#         #print("-l=line-element\t\t TODO")
#         #print("-i\t\t\t TODO")
#         #print("--start=n\t\t TODO")
#         #print("-e, --error-recovery\t TODO")
#         print("--missing-field=val\t TODO")
#         print("--all-coumns\t\t TODO")
#         #print("--padding\t\t Provide compact (minimal) output")
#         #print("--validate\t\t Validate input CSV as defined by RFC4180")


c2x = csv2xml()

exit()
