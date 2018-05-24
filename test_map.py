
def test_neighborhood():
	from map0 import Neighborhood as N
	return N(80,500,500)
def test_interface():
	from interface_map import InterfaceNeighborhood as N
	return N(80,500,500)
if __name__ == "__main__":
	#N = test_neighborhood()
	N = test_interface()
	N.start(20)
