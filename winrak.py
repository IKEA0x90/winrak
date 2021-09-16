from sys import argv
from os import path
from typing import Type
import numpy

def pack(Bits: list):
    '''
    Packs bits using winrak (c) packing.
    @param:
        Bits: list
    @return:
        Packed: list 
    '''
    counter = 0
    packed = []
    bitm = Bits[0]
    try:
        for j in range(0, len(Bits)):
            if Bits[j] == bitm:
                counter += 1
            else:
                packed.append([bitm, counter])
                counter = 1
                bitm = Bits[j]
            if counter == 9:
                packed.append([bitm, counter])
                counter = 0
        if j == len(Bits) - 1:
            packed.append([bitm, counter])
            return packed
    except:
        return packed

def create_rak(packed: list, name, filetype):
    '''
    Creates a .rak file
    @param:
        packed: list - packed bits
        name: string - name of the file
        filetype: string - filetype
    '''
    file = open(name + '.rak', 'w')
    data = ''
    for list in packed:
        data += str(list[0])
        data += str(list[1])
    file.write(filetype + "\n" + data)
    file.close()

def unpack(packed):
    '''
    Unpacks a winrak (c) archive
    @param:
        packed: string - packed bits
    @return:
        unpacked: list
    '''
    unpacked = []
    for i in range(0, len(packed) - 1, 2):
        bitm = int(packed[i])
        for j in range(int(packed[i + 1])):
            unpacked.append(bitm)
    return unpacked

    
def create_unpacked(unpacked: list, name, filetype):
    '''
    Creates an unpacked file using unpacked bits
    @param:
        unpacked: list - unpacked bits
        name: string - name
        filetype: string - filetype
    '''
    Bytes = numpy.packbits(numpy.asarray(unpacked))
    Bytes = numpy.asarray(Bytes)
    filename = (name + filetype).strip()
    file = open(filename, "wb")
    Bytes.tofile(file)
    file.close()

def help():
    '''
    Displays a help message, stating how to use winrak (c) and arguments
    '''
    print("Usage: ", argv[0], " <filename> [OPTIONS]", sep='')
    print("Options:\n\
            \t-n, --name\t [name of the winrak (c) archive that will be created]\n\
            \t-u, --unpack\t[tells ", argv[0], " to unpack the archive]\n\
            \t-a\t\t[name of the unpacked file that will be created]", sep='')

def getArgs():
    '''
    Gets all the arguments that the user specified using argv and validates them
    @return:
        args: dict - dictionary of the arguments.

    '''
    args = {'script':None, 'name':None, '-n':'', '-u':False, '-a':''}

    if len(argv) == 1:
        print("Usage: ", argv[0], " <filename> [OPTIONS]. Use --help to see options", sep='')
        exit(0)
    
    args['script'] = argv[0]
    args['name'] = argv[1]
    
    try:
        if argv.count('-n') or argv.count('--name'):
            if argv.count('-n'):
                i = argv.index('-n')
            if argv.count('--name'):
                i = argv.index('--name')
            args['-n'] = argv[i + 1]
        
        if argv.count('-a'):
            i = argv.index('-a')
            args['-a'] = argv[i + 1]

        if argv.count('-u') or argv.count('--unpack'):
            args['-u'] = True
    except IndexError:
        print(argv[0], ': option requires an argument -- ', argv[i])
    
    return args

def main():
    '''
    If pack is used: 
        Reads bits from a file and calls pack() to pack them \n
        Creates a packed .rak file via create_rak()\n
    If unpack is used:
        Reads a packed file
        Unpacks it via unpack()
        Creates a file from unpacked bits via create_uncpacked()
    '''
    try:
        args = getArgs()
        if args['name'] == '--help':
            help()
            exit(0)
        if not args['-u']:
            file = open(args['name'], 'rb')
            filepath = path.splitext(args['name'])
            filetype = filepath[1].strip()
            
            if args['-n'] == '':
                filename = filepath[0].strip()
            else:
                filename = args['-n']

            Bytes = numpy.fromfile(file, dtype = "uint8")
            Bits = numpy.unpackbits(Bytes)

            
            #for bit in Bits:
            #    print(bit, sep='', end='')
            #print()
            

            packed = pack(Bits)

            #print(packed)
            create_rak(packed, filename, filetype)
            file.close()
        else:
            file = open(args['name'])
            filepath = path.splitext(args['name'])
            filetype = file.readline()

            if args['-a'] == '':
                filename = filepath[0].strip()
            else:
                filename = args['-a']

            packed = file.readline()

            unpacked = unpack(packed)
            #print(unpacked)

            create_unpacked(unpacked, filename, filetype)
            file.close()

    except FileNotFoundError:
        print("File not found: ", args['name'], sep='')
    except IndexError:
        print("Usage: ", args['script'], " <filename> [OPTIONS]. Use --help for full description", sep='')
    except UnicodeDecodeError:
        print("Cannot decode file: ",args['name'], sep='')
    except TypeError:
        print("Something went wrong")

if __name__ == "__main__":
    main()