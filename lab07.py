# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from pathlib import Path

AT_SYMBOL = '@'
WHITE_SPACE1 = '//'
WHITE_SPACE2 = '#'
EQUAL = '='
SEMI = ';'
P_OPEN = "("
P_CLOSE = ")"
ZERO_NINE = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
JUMP = 'J'
MEMORY = 'M'
A_REGISTER = 'A'
D_REGISTER = 'D'
ALGEBRAIC = ['+', '-']
NON_ALGEBRA1 = '&'
NON_ALGEBRA2 = '|'
ZERO = '0'
ONE = '1'
# MAX_VALUE is 2^15 -1 (left most bit is excluded)
MAX_VALUE = 32767
WORD_DICT = {}


def txtfile(file_from, file_name):
    pathtxt = Path(file_name)
    if pathtxt.is_file() is False:
        text_write = open(file_name, "w")
        text_write.write("v2.0 raw \n")

        parent = open(file_from, "r")
        with open(file_from, "r") as fp:
            for count, line in enumerate(fp):
                translate_text(parent, text_write)

        text_write.close()
        parent.close()
    else:
        text_read = open(file_from, "r")
        text_read.close()


def binfile(file_from, file_name):
    pathbin = Path(file_name)
    if pathbin.is_file() is False:
        bin_write = open(file_name, "w")

        parent = open(file_from, "r")

        with open(file_from, "r") as fp:
            for count, line in enumerate(fp):
                current = parent.readline()
                if P_OPEN in current and P_CLOSE in current:

                    # count is set to -1 as the index of files begins at 0, meaning the count would be one greater
                    # than the actual position
                    count = 0

                    print(WORD_DICT)
                    with open(file_from, "r") as file_scan2:
                        for lines in file_scan2:
                            count += 1
                            if current in lines:
                                current_new = current.replace('\n', "")
                                current_new2 = current_new.replace("(", "")
                                current_final = current_new2.replace(")", "")
                                WORD_DICT.update({current_final: None})
                                for x in WORD_DICT:
                                    if x != current_final:
                                        count -= 1
                                count -= 1
                                break
                    WORD_DICT.update({current_final: count})
                    print(WORD_DICT)
        parent2 = open(file_from, "r")
        with open(file_from, "r") as fg:
            for count, line in enumerate(fg):
                translate_bin(parent2, bin_write)

        bin_write.close()
        parent.close()
    else:
        bin_read = open(file_name, "r")
        bin_read.close()


def translate_text(file_from, file_to):
    current = file_from.readline()
    if WHITE_SPACE1 not in current or WHITE_SPACE2 not in current:
        first_f = current[12:16]
        sec_f = current[8:12]
        third_f = current[4:8]
        final_f = current[0:4]

        hexdec(final_f, file_to)
        hexdec(third_f, file_to)
        hexdec(sec_f, file_to)
        hexdec(first_f, file_to)

        file_to.write("\n")
    else:
        file_to.write(current)


def translate_bin(file_out, file_to):
    current = file_out.readline()
    if WHITE_SPACE1 not in current or WHITE_SPACE2 not in current:
        if P_OPEN in current and P_CLOSE in current:
            file_to.write("")
        elif AT_SYMBOL in current:
            p_count = 0
            for p in ZERO_NINE:
                if p in current:
                    p_count += 1
            if p_count == 0:
                current = current.replace("@", "")
                current_new = current.replace("\n", "")
                # print(current)
                for x in WORD_DICT:
                    if x == current_new:
                        value = WORD_DICT[current_new]
                        bin_value = bin(value).replace("0b", "")
                        #  print(value)
                        str_bv = str(bin_value)
                        b_vlen = line_size(bin_value)
                        if b_vlen < 16:
                            extender = '0' * (16 - b_vlen)
                            file_to.write(extender)
                        file_to.write(str_bv + "\n")

            else:
                current = current.replace(AT_SYMBOL, "")
                value = bin(int(current)).replace("0b", "")
                # print(value)
                values = str(value)
                lengthnew = line_size(values)
                if lengthnew < 16:
                    extended = '0' * (16 - lengthnew)
                    file_to.write(extended)
                file_to.write(values + "\n")

        # Do not add an else to others as it will a copy of any @ line
        elif AT_SYMBOL not in current and P_OPEN not in current:
            find_last(current, file_to)
            comp(current, file_to)
            dest(current, file_to)
            jumps(current, file_to)
        else:
            file_to.write(current)
    else:
        file_to.write("")


# Converts 4 digits into a hexadecimal for txt file
def hexdec(four_bit, file_to):
    if four_bit == "0000":
        file_to.write("0")
    elif four_bit == "0001":
        file_to.write("1")
    elif four_bit == "0010":
        file_to.write("2")
    elif four_bit == "0011":
        file_to.write("3")
    elif four_bit == "0100":
        file_to.write("4")
    elif four_bit == "0101":
        file_to.write("5")
    elif four_bit == "0110":
        file_to.write("6")
    elif four_bit == "0111":
        file_to.write("7")
    elif four_bit == "1000":
        file_to.write("8")
    elif four_bit == "1001":
        file_to.write("9")
    elif four_bit == "1010":
        file_to.write("A")
    elif four_bit == "1011":
        file_to.write("B")
    elif four_bit == "1100":
        file_to.write("C")
    elif four_bit == "1101":
        file_to.write("D")
    elif four_bit == "1110":
        file_to.write("E")
    elif four_bit == "1111":
        file_to.write("F")


# bits 11 through 6 of the output reliant on if there is an algebraic process done or not ()
def comp(line, file_to):
    find_12(line, file_to)
    # print(line)
    if ALGEBRAIC[0] not in line and ALGEBRAIC[1] not in line and NON_ALGEBRA1 not in line and NON_ALGEBRA2 not in line:
        if SEMI in line:
            value = line.index(SEMI)
            lines = line[:value]
            if EQUAL in line:
                value_e = lines.index(EQUAL)
                lin_l = lines[value_e:]

                if ZERO in lin_l:
                    file_to.write("101010")

                elif ONE in lin_l:
                    if "-" in lin_l:
                        if lin_l.index(ONE) == lin_l.index("-") + 1:
                            file_to.write("111010")
                    else:
                        file_to.write("111111")

                elif D_REGISTER in lin_l:
                    print(line)
                    if "-" in lin_l:
                        if line.index(D_REGISTER) == lin_l.index("-") + 1:
                            file_to.write("001111")
                    elif "!" in lin_l:
                        if lin_l.index(D_REGISTER) == lin_l.index("!") + 1:
                            file_to.write("001101")
                    else:
                        file_to.write('001100')

                elif A_REGISTER in lin_l:
                    if "-" in lin_l:
                        if lin_l.index(A_REGISTER) == lin_l.index("-") + 1:
                            file_to.write("110011")
                    elif "!" in lin_l:
                        if lin_l.index(A_REGISTER) == lin_l.index("!") + 1:
                            file_to.write("110001")
                    else:
                        file_to.write("110000")

                elif MEMORY in lin_l:
                    if "-" in lin_l:
                        if lin_l.index(MEMORY) > lin_l.index("-"):
                            file_to.write("110011")
                    elif "!" in lin_l:
                        if lin_l.index(MEMORY) == lin_l.index("!") + 1:
                            file_to.write("110001")
                    else:
                        file_to.write("110000")
            else:
                if ZERO in lines:
                    file_to.write("101010")

                elif ONE in lines:
                    if "-" in lines:
                        if lines.index(ONE) > lines.index("-"):
                            file_to.write("111010")
                    else:
                        file_to.write("111111")

                elif D_REGISTER in lines:
                    if "-" in line:
                        if lines.index(D_REGISTER) > lines.index("-"):
                            file_to.write("001111")
                    elif "!" in lines:
                        if lines.index(D_REGISTER) > lines.index("!"):
                            file_to.write("001101")
                    else:
                        file_to.write("001100")

                elif A_REGISTER in lines:
                    if "-" in lines:
                        if lines.index(A_REGISTER) > lines.index("-"):
                            file_to.write("110000")
                    elif "!" in lines:
                        if lines.index(A_REGISTER) > lines.index("!"):
                            file_to.write("110001")
                    else:
                        file_to.write("110000")

                elif MEMORY in lines:
                    if "-" in lines:
                        if lines.index(MEMORY) > lines.index("-"):
                            file_to.write("110011")
                    elif "!" in lines:
                        if lines.index(MEMORY) == lines.index("!") + 1:
                            file_to.write("110001")
                    else:
                        file_to.write("110000")

        else:
            if EQUAL in line:
                value_e = line.index(EQUAL)
                lin_l = line[value_e:]
                if ZERO in lin_l:
                    file_to.write("101010")

                elif ONE in lin_l:
                    if "-" in lin_l:
                        if lin_l.index(ONE) > lin_l.index("-"):
                            file_to.write("111010")
                    else:
                        file_to.write("111111")

                elif D_REGISTER in lin_l:
                    if "-" in lin_l:
                        if line.index(D_REGISTER) > lin_l.index("-"):
                            file_to.write("001111")
                    elif "!" in lin_l:
                        if lin_l.index(D_REGISTER) > lin_l.index("!"):
                            file_to.write("001101")
                    else:
                        file_to.write("001100")

                elif A_REGISTER in lin_l:
                    if "-" in lin_l:
                        if lin_l.index(A_REGISTER) > lin_l.index("-"):
                            file_to.write("110011")
                    elif "!" in lin_l:
                        if lin_l.index(A_REGISTER) > lin_l.index("!"):
                            file_to.write("110001")
                    else:
                        file_to.write("110000")

                elif MEMORY in lin_l:
                    if "-" in lin_l:
                        if lin_l.index(MEMORY) > lin_l.index("-"):
                            file_to.write("110011")
                    elif "!" in lin_l:
                        if lin_l.index(MEMORY) == lin_l.index("!") + 1:
                            file_to.write("110001")
                    else:
                        file_to.write("110000")
            else:
                if ZERO in line:
                    file_to.write("101010")

                elif ONE in line:
                    if "-" in line:
                        if line.index(ONE) > line.index("-"):
                            file_to.write("111010")
                    else:
                        file_to.write("111111")

                elif D_REGISTER in line:
                    if "-" in line:
                        if line.index(D_REGISTER) == line.index("-") + 1:
                            file_to.write("001111")
                    elif "!" in line:
                        if line.index(D_REGISTER) == line.index("!") + 1:
                            file_to.write("001101")
                    else:
                        file_to.write("001100")

                elif A_REGISTER in line:
                    if "-" in line:
                        if line.index(A_REGISTER) > line.index("-"):
                            file_to.write("110011")

                    elif "!" in line:
                        if line.index(A_REGISTER) > line.index("!"):
                            file_to.write("110001")
                    else:
                        file_to.write("110000")

                elif MEMORY in line:
                    print(line)
                    if "-" in line:
                        if line.index(MEMORY) > line.index("-"):
                            file_to.write("110011")
                    elif "!" in line:
                        if line.index(MEMORY) == line.index("!") + 1:
                            file_to.write("110001")
                    else:
                        file_to.write("110000")

    elif ALGEBRAIC[0] in line:
        if (D_REGISTER + ALGEBRAIC[0] + '1') in line:
            file_to.write('011111')
        elif (D_REGISTER + ALGEBRAIC[0] + A_REGISTER) in line or (D_REGISTER + ALGEBRAIC[0] + MEMORY) in line:
            file_to.write('000010')
        elif (A_REGISTER + ALGEBRAIC[0] + '1') in line or (MEMORY + ALGEBRAIC[0] + '1') in line:
            file_to.write('110111')
        elif (A_REGISTER + ALGEBRAIC[0] + D_REGISTER) in line or (MEMORY + ALGEBRAIC[0] + D_REGISTER) in line:
            file_to.write('000010')

    elif ALGEBRAIC[1] in line:
        if (D_REGISTER + ALGEBRAIC[1] + '1') in line:
            file_to.write('001110')
        elif (D_REGISTER + ALGEBRAIC[1] + A_REGISTER) in line or (D_REGISTER + ALGEBRAIC[1] + MEMORY) in line:
            file_to.write('010011')
        elif (A_REGISTER + ALGEBRAIC[1] + '1') in line or (MEMORY + ALGEBRAIC[1] + '1') in line:
            file_to.write('110010')
        elif (A_REGISTER + ALGEBRAIC[1] + D_REGISTER) in line or (MEMORY + ALGEBRAIC[1] + D_REGISTER) in line:
            file_to.write('000111')
        elif (ALGEBRAIC[1] + '1') in line:
            file_to.write('111010')
        elif (ALGEBRAIC[1] + D_REGISTER) in line:
            file_to.write('001111')
        elif (ALGEBRAIC[1] + A_REGISTER) in line or (ALGEBRAIC[1] + MEMORY):
            file_to.write('110011')

    elif NON_ALGEBRA1 in line:
        if (D_REGISTER + NON_ALGEBRA1 + A_REGISTER) in line:
            file_to.write('000000')
        if (D_REGISTER + NON_ALGEBRA1 + MEMORY) in line:
            file_to.write('000000')

    elif NON_ALGEBRA2 in line:
        if (D_REGISTER + NON_ALGEBRA2 + A_REGISTER) in line or (D_REGISTER + NON_ALGEBRA2 + MEMORY) in line:
            file_to.write('010101')


def not_digit(file_from):
    chosen = file_from.readline()
    print(chosen)
    with open("test.asm", 'r') as file_new:
        count = 0
        for line in file_new:
            count += 1
            if chosen in line:
                break
    WORD_DICT.update({chosen: count})
    print(WORD_DICT)


def count_num_char(line, char):
    count = 0
    for x in line:
        if x == char:
            count += 1
    return count


# finds the 12th bit
def find_12(line, file_to):
    if SEMI in line:
        value_sem = line.index(SEMI)
        lines = line[0:value_sem]
        if EQUAL in lines:
            value_e = lines.index(EQUAL)
            split_l = lines[:value_e]
            if MEMORY not in split_l or "!M" in split_l:
                file_to.write("0")
            elif MEMORY in split_l and "!" not in split_l:
                file_to.write("1")
        else:
            if MEMORY not in lines or "!M" in lines:
                file_to.write("0")
            elif MEMORY in lines and "!" not in lines:
                file_to.write("1")
    else:
        if MEMORY not in line or "!M" in line:
            file_to.write("0")
        elif MEMORY in line:
            file_to.write("1")
            if "!M" in line:
                file_to.write("0")


# finds the last digits [15:13], if @ in line print all 0s, if not all 1s
def find_last(line, file_to):
    if AT_SYMBOL not in line:
        file_to.write('111')
    else:
        file_to.write('000')


# handles the dest bits [5:3] in an array. Since there is a one-to-one relationship between the three bits and A, D
# and M each changes the bit for their repective spot.
def dest(line, file_to):
    dest_rules = [0, 0, 0]
    if EQUAL in line:
        value = line.index(EQUAL)
        lines = line[0:value]
        if MEMORY in lines:
            dest_rules[2] = 1
        if A_REGISTER in lines:
            dest_rules[0] = 1
        if D_REGISTER in lines:
            dest_rules[1] = 1

    string_dest = str(dest_rules)
    dest1 = string_dest.replace("[", "")
    dest2 = dest1.replace("]", "")
    dest3 = dest2.replace(" ", "")
    final_dest = dest3.replace(",", "")
    file_to.write(final_dest)


#handles the first three bits (jump bits) based on the letter after ";"
def jumps(line, file_to):
    if 'JGT' in line:
        file_to.write('001\n')
    elif 'JEQ' in line:
        file_to.write('010\n')
    elif 'JGE' in line:
        file_to.write('011\n')
    elif 'JLT' in line:
        file_to.write('100\n')
    elif 'JNE' in line:
        file_to.write('101\n')
    elif 'JLE' in line:
        file_to.write('110\n')
    elif 'JMP' in line:
        file_to.write('111\n')
    elif JUMP not in line:
        file_to.write('000\n')


def line_size(line):
    counter = 0
    for x in line:
        counter += 1
    return counter


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file = input("What file would you like to translate? ")
    bin_file = input("What would you like to name the bin file? ")
    txt_file = input("What would you like to name the txt file? ")
    binfile(file, bin_file)
    txtfile(bin_file, txt_file)
