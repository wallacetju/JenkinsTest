import unittest
from hello_world import HelloWorld
 
class HelloWorldTest(unittest.TestCase):
 	hello_world = HelloWorld()
	def test_hello_world(self):
		self.assertEqual(self.hello_world.message(), "Hello World!")
		print "Hello World Test Passed!"
 
if __name__ == '__main__':
    unittest.main()