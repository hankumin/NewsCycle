#!usr/bin/python
import csv

def main():
    with open('../ticker_secid_name.map' , newline = '', encoding ='utf-8') as csvfile:
        firstTwo = csv.DictReader(csvfile, delimiter = '|')

        theExchanges = dict([])

        for row in firstTwo:
            if row['Exchange'] != 'Private':
                if row['Exchange'] in theExchanges:
                    theExchanges[row['Exchange']].append(row['Symbol'])
                else:
                    theExchanges[row['Exchange']] = [row['Symbol']]

        for eachExchange in theExchanges:
            print eachExchange + ": "
            print theExchanges[eachExchange]

        csvfile.close()

if __name__ == '__main__':
    main()
