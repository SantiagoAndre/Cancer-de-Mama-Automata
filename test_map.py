
def test_neighborhood():
	from map import Neighborhood as N
	return N(50,8,8)
if __name__ == "__main__":
	N = test_neighborhood()
	N.start(20)
