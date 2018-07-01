#calcula el rgb de un color en hexadecimal sin el # al principio
def hex_to_rgb(hex):
	#hex = hex.lstrip('#')
	hlen = len(hex)
	return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))
def read_colors_file():
	colors = []
	for color in open("resources/files/colors_file.txt"):
		if color[-1] is "\n":
			color = color[:-1]
		if color[0] is "#":
			if color[1] is  "!":
				continue
			color = hex_to_rgb(color[1:])
		else:
			color = eval(color)
		colors.append(color)
	return colors
def read_ranges_file():
	f = open("resources/files/ranges_file.txt")
	end_line = True
	str_number = ""
	while True:
		c = f.read(1)
		if c == "#":
			f.readline()
			
			#print("ignorado: ",f.readline())#lee toda la linea, y la ignora
			if  end_line:
				while f.read(1)=="#":
					f.readline()
				end_line = False
				continue
			c = '\n'
		if not c:
			yield -1
			break
		if end_line:
			yield -1

		end_line = c =='\n'
		if (c==" " or c == "\n"):
			if str_number:
				yield int(str_number)
			str_number = ""
		else:
			str_number +=c
