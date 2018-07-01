def asd():
    f = open("resources/files/ranges_file1.txt")
    str_number = ""
    end_line = False
    while True:
        c= f.read(1)
        if not c:
            yield False
            break
        if end_line:
            yield -1
        end_line = c =='\n'
        if (c==" " or c == "\n") and str_number:
        	yield int(str_number)
        	str_number = ""
        else:
            str_number +=c
for numero in asd():
    print("'",numero,"'")
