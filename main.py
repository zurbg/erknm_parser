import json
from pprint import pprint
from erknm_parser import ErknmParser



if __name__=='__main__':
    knm_filename = '21995037.xml'

    parser = ErknmParser(knm_filename)
    result = parser.parse()
    pprint(result)