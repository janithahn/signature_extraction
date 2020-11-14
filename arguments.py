import getopt, sys

argumentList = sys.argv[1:]
short_options = "hi:o:"
long_options = ["Input=", "Output="]
inputFile = ''
outputFile = ''

try:
    opts, args = getopt.getopt(argumentList, short_options, long_options)
    for opt, arg in opts:
        if opt in ('-h', '--Help'):
            print('signature.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ('-i', '--Input'):
            inputFile = arg
        elif opt in ('-o', '--Output'):
            outputFile = arg
except getopt.error as err:
    print (str(err))
    sys.exit(2)

print(inputFile, outputFile)
