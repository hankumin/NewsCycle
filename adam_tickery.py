#/usr/bin/python
#/Testing some stuff
from fabric.api import *
import sys
#edi_path = "/nwsys/tickergen-EDI/"
met_sun= "/nwsys/metabot_sungard/"
edi_path = met_sun
list_of_files = [
                  'xwalk_in.txt',
                  'dnbInput.txt',
                  'sungardDomestic.txt',
                  'sungardIntl.txt',
                  'xwalkOverride.txt',
                  'mapper/ticker_secid_name.map',
                  'mapper/mapper_override',
                  'mapper/NaicsToIc.txt',
                  'mapper/sungardPreferredTickers.txt',
                  'noah/sungard_name_overrides',
                  'noah/sungard_symbols_override',
                  'noah/sungard_ticker_overrides',
                  'noah/location_variants',
                  'noah/lastAcorn',
                  'noah/dict.amc',
                  'noah/company_variants',
                  'noah/peoplenames',
                  'noah/locations',
                  'noah/symbols',
                  'compustat/domestic.txt',
                  'compustat/foreign.txt',
                  'working/NewConcordance',
                  'working/concordance'
                ]
# removed mapper/exchanges.csv
def copy_from_cameo2():

    with settings(host_string="cameo2.mmu.acquiremedia.com", user = "nadmin", password="nadmin"):
         for file in list_of_files :
             try:
                   path = edi_path+file
                   path = path[:path.rfind('/')]
                   local('mkdir -p ' + path)
                   get(met_sun+file, edi_path+file)
             except Exception as e:
                 print e

if __name__ == "__main__":
   copy_from_cameo2()
