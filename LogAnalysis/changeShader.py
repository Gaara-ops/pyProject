import os

filenames = ["D:/finalshelldown/compute.cs", "D:/finalshelldown/sum.cs"]
for filename in filenames:
    fr = open(filename, 'r')
    fw = open(filename + '.bak', 'w')
    for line in fr:
        fw.write("\"")
        fw.write(line.replace('\n', ''))
        fw.write("\\n\"")
        fw.write("\n")
    fr.close()
    fw.close()

print("end!")
