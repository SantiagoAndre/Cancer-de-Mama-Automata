
def test_neighborhood():
	from logic.map import Neighborhood as N
	return N(80,500,500)
def test_interface():
	from intergace.interface_map import InterfaceNeighborhood
	return InterfaceNeighborhood(80,100,100)
if __name__ == "__main__":
	#N = test_neighborhood()
	N = test_interface()
	N.start(20)
