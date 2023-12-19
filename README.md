README LAB 07
The python project uses requires the input of the user for a file, in this example typing "test.asm" will supply two outputs, labeled by the user. 
The job of the binfile method is to open up the input file and add the labels found in the P_OPEN and P_CLOSED (parentheses). 
Once the file is read once it is read again this time editing the .bin file to input the values of 1s and 0s. The input section is 
done in the translate_bin method which takes in the file it is reading from and file it is outputting to and calls multiple functions in the order of 
final_last, comp, dest, and jumps. Once iterated through the length of the input file, meaning it has read every line and produced an output to the .bin file, the 
txtfile method is called. The txtfile method iterates through the course of the .bin file and translates each binary string into a set of hexadecimals for the cpu to read. 
The hexdec() method allows for easy conversion with each 4 digit possibility having a singular output of a hexadecimal. Once the translation to hexadecimals is accomplished, the program terminates but the .txt and .bin file persist. If the user runs the program again, they will not make any changes to the output files, only once the original .txt and .bin files are deleted will the user be able to run the program again with the 
output of two new files. Notably, the fine_12() method is does not run successfully however, all other methods match the outputs of the examples provided in the lab details. 
