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

	for piv in open("resources/files/ranges_file.txt"):
		if piv[-1] is "\n":
			piv = piv[:-1]
		if not (piv[0]  is "#"):
			yield float(piv)
