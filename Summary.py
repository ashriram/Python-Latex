import glob
import os
import fnmatch
from itertools import zip_longest
import sys, getopt




def main(argv):
    inputfile = ''
    type = ''
    try:
        opts, args = getopt.getopt(argv,"hi:e:n:",["ifolder=","etype="])
    except getopt.GetoptError:
        print("test.py -i <input folder> -e <etype>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("test.py -i <input folder> -e <etype>")
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            inputfile = arg
        elif opt in ("-e", "--etype"):
            type = arg
        elif opt in ("-n", "--name"):
            name = arg


    print('Input file is "' + inputfile)
    print('Type file is "'+  type)


    matches = []

    paths = inputfile+"/**/*."+type
    for filename in glob.iglob(paths, recursive=True):
        matches.append(filename)

    pairs = zip_longest(*[iter(matches)]*2, fillvalue=None)


    tabular = ""
    count = 1
    for a,b in pairs:
        if (b is not None):
            header = "{{\\large \\bf  {0} }} {{ {1} }} & {{\large \\bf {2} }} {{ {3} }} \\\\ ".format(count,os.path.basename(a),count+1,os.path.basename(b))
            # print(header)
            includes = "\\includegraphics[width=3in]{{{0}}} & \\includegraphics[width=3in]{{{1}}} \\\\ \hline ".format(a,b)
            tabular += header + "\n" + includes + "\n"
            # print(includes)
            count += 2
        else:
            header = "{{\\large \\bf  {0} }} {{ {1} }} &  \\\\".format(count,os.path.basename(a))
            # print(header)
            includes = "\\includegraphics[width=3in]{{{0}}} &  \\\\ \hline ".format(a)
            # print(includes)
            tabular += header + "\n" + includes + "\n"
            count += 1

    preambletex = '''\\centering {\\LARGE \\bf ''' + name  + ''' ARTICLES Total articles: ''' + str(count-1) + '''}\n
            \\renewcommand{\\arraystretch}{2}\n
            \\begin{longtable}{p{3.5in}p{3.5in}}\n'''


    Texfile = open(name+"tab.tex","w")
    Txtfile = open(name+"186.txt","w")

    Texfile.write(preambletex)
    Texfile.write(tabular + "\n \end{longtable}")

    count = 1
    for file in matches:
        count+=1
        Txtfile.write(str(count-1) + " " + os.path.splitext(os.path.basename(file))[0] + "\n")


if __name__ == "__main__":
   main(sys.argv[1:])
