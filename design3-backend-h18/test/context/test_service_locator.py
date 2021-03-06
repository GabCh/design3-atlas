import unittest

from atlas.infrastructure.ServiceLocator import ServiceLocator, InstantiationException


class ServiceLocatorTest(unittest.TestCase):
    A_LITERAL_OBJECT = "A Message"

    def setUp(self):
        self.serviceLocator = ServiceLocator()

    def test_givenInexistentComponent_whenGettingComponent_thenThrowInstatiationException(self):
        with self.assertRaises(InstantiationException):
            self.serviceLocator.get(SomeClass)

    def test_givenLiteralComponent_whenGettingComponent_thenReturnsLiteralWithoutInstantiation(self):
        self.serviceLocator.bind(str, self.A_LITERAL_OBJECT)

        component = self.serviceLocator.get(str)

        self.assertEqual(self.A_LITERAL_OBJECT, component)

    def test_givenInstantiatableComponent_whenGettingComponent_thenReturnInstantiatedObject(self):
        self.serviceLocator.bind(SomeClass, SomeClass)

        component = self.serviceLocator.get(SomeClass)

        self.assertIsInstance(component, SomeClass)

    def test_givenBoundAbstraction_whenGettingChildComponent_thenReturnChildComponent(self):
        self.serviceLocator.bind(SomeClass, SomeChildClass)

        component = self.serviceLocator.get(SomeClass)

        self.assertIsInstance(component, SomeChildClass)

    def test_givenConstructorWithParameters_whenGettingComponent_thenRecursivelyInstantiateConstructorParameters(self):
        self.serviceLocator.bind(SomeClassWithParameters, SomeClassWithParameters)
        self.serviceLocator.bind(SomeClass, SomeClass)

        component = self.serviceLocator.get(SomeClassWithParameters)

        self.assertIsInstance(component, SomeClassWithParameters)
        self.assertIsInstance(component.someObject, SomeClass)


class SomeClass(object):
    pass


class SomeChildClass(SomeClass):
    pass


class SomeClassWithParameters(object):
    def __init__(self, some_object: SomeClass):
        self.someObject = some_object


if __name__ == "__main__":
    unittest.main()
