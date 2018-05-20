
def test_neighborhood():
	from map import Neighborhood as N
	return N(500,500)
if __name__ == "__main__":
	N = test_neighborhood()
	N.start(20)
