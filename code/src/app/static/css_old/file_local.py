input_files = []
input_files.append('bootstrap.min.4.1.3.css')
replaces = []
replaces.append({'old':'http://www.w3.org/2000/svg','new':'/svg'})

for input_file in input_files:
    with open(input_file,"r") as fp:
        output_file = input_file+".fix"
        print("%s -> %s"%(input_file,output_file))
        fo = open(output_file,"w")
        line = fp.readline()
        while line:
            for rep in replaces:
                print("  replacing '%s' -> '%s'"%(rep['old'],rep['new']))
                line=line.replace(rep['old'],rep['new'])
            fo.write(line)
            line = fp.readline()
        print("%s fixed."%input_file)
        fo.close()
    fp.close()

