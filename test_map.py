
def test_neighborhood():
	from map import Neighborhood as N
	return N(100,100)
if __name__ == "__main__":
	N = test_neighborhood()
	N.start(20)
