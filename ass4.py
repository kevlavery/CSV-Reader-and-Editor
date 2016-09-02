#!/opt/bin/python3

# Assignment 4
# Author: Kevin Lavery, V00242982

import sys
import os
import os.path
import re
import csv

def dependants(file, sources):
    temp = []
    try:
        with open(file) as fp:
            for line in fp:
                if re.search(r"^#include\s+\"(.*\.h)\"", line) != None:
                    temp.append(re.findall(r"^#include\s+\"(.*\.h)\"", line))
    except:
        print("Error occured while reading file", file)
        reason = sys.exc_info()
        print("Reason: ", reason[1])

    for item in temp:
        item = str(item)[2:-2]
        if item not in sources:
            sources.add(item)
            if os.path.isfile(os.path.join(os.getcwd(),item)) == False:
                print("{0}: contains #include for missing file {1}".format(file, item))
            else:
                if(dependants(item, sources) != None):
                    blarg = dependants(item, sources)
                    for header in blarg:
                        sources.add(header)
    if len(sources) < 1:
        return None

    return sources

if __name__ == '__main__':

    if(len(sys.argv) < 2):
        print ("Directory not specified.")
        sys.exit()

    folderpath = sys.argv[1]
    if(os.path.isdir(os.path.join(os.getcwd(),folderpath))):
        os.chdir(folderpath)
    else:
        print("Specified directory doesn't exist.")
        sys.exit()

    fcontents = []
    names = []
    newnames = []
    ctype = []
    for file in os.listdir():
        if file[-2:] == '.c':
            ctype.append('CC')
            fcontents.append(file)
            names.append(os.path.splitext(file)[0])
            
        if file[-2:] == '.C' or file[-4:] == '.cpp' or file[-3:] == '.cc':
            ctype.append('CXX')
            fcontents.append(file)
            names.append(os.path.splitext(file)[0])
    names = [s+'.o' for s in names]

    if len(fcontents) < 1:
        print('There are no files to make in this folder.')
        sys.exit()

    try:
        filewrite = open('Makefile', 'w')
        filewrite.write("SRCS = "+" ".join(fcontents)+\
                   "\nOBJS = "+" ".join(names)+\
                   "\nPROG = prog.exe"+\
                   "\n\n$(PROG): $(OBJS)"+\
                   "\n\t$(CC) $(LDFLAGS) $(OBJS) $(LDLIBS) -o $(PROG)")
        
        filewrite.close()
    except:
        print("Error occured while creating file", 'Makefile')
        reason = sys.exc_info()
        print("Reason: ", reason[1])
    
    for create, cfile, compiler in zip(names, fcontents, ctype):
        sources = set()
        dependants(cfile, sources)

        if compiler == 'CC' and sources!=None:
            try:
                filewrite = open('Makefile', 'a')
                filewrite.write("\n\n{0}: {1} {2}\n\t$(CC) $(CPPFLAGS) $(CFLAGS) -c {0}".format(create, cfile, " ".join(sources)))
                filewrite.close()
            except:
                print("Error occured while creating file", 'Makefile')
                reason = sys.exc_info()
                print("Reason: ", reason[1])
                
        elif compiler == 'CXX' and sources!=None:
            try:
                filewrite = open('Makefile', 'a')
                filewrite.write("\n\n{0}: {1} {2}\n\t$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c {0}".format(create, cfile, " ".join(sources)))
                filewrite.close()
            except:
                print("Error occured while creating file", 'Makefile')
                reason = sys.exc_info()
                print("Reason: ", reason[1])
        else:
            print("There are no source or header files in this directory to make.")

    try:
        filewrite = open('Makefile', 'a')
        filewrite.write("\n\nclean:"\
                        "\n\trm -f $(OBJS)")
        
        filewrite.close()
    except:
        print("Error occured while creating file", 'Makefile')
        reason = sys.exc_info()
        print("Reason: ", reason[1])
            
        
        
        
        
    
