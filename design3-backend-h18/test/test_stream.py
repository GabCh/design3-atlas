# Jivago Framework, Copyright (c) 2018 Kento A. Lauzon
# https://github.com/keotl/jivago
# Utilisé avec permission.
import unittest

from atlas.infrastructure.stream import Stream


class StreamTest(unittest.TestCase):
    COLLECTION = [5, 3, 1, 10, 51, 42, 7]
    DIVIDES_BY_THREE = lambda x: x % 3 == 0
    BUMPY_COLLECTION = [[5, 3, 1], [10], [51, 42, 7]]

    def setUp(self):
        self.stream = Stream(self.COLLECTION)

    def test_whenMapping_thenReturnFunctionAppliedToAllElements(self):
        expected = [x for x in map(StreamTest.DIVIDES_BY_THREE, self.COLLECTION)]

        result = self.stream.map(StreamTest.DIVIDES_BY_THREE).toList()

        self.assertEqual(expected, result)

    def test_whenFiltering_thenReturnElementsWhichEvaluateToTrue(self):
        expected = [x for x in filter(StreamTest.DIVIDES_BY_THREE, self.COLLECTION)]

        result = self.stream.filter(StreamTest.DIVIDES_BY_THREE).toList()

        self.assertEqual(expected, result)

    def test_givenAnElementThatMatches_whenCheckingAnyMatch_thenReturnTrue(self):
        result = self.stream.anyMatch(StreamTest.DIVIDES_BY_THREE)

        self.assertTrue(result)

    def test_givenNotAllElementsMatch_whenCheckingAllMatch_thenReturnFalse(self):
        result = self.stream.allMatch(StreamTest.DIVIDES_BY_THREE)

        self.assertFalse(result)

    def test_givenAllMatchingElements_whenCheckingAllMatch_thenReturnTrue(self):
        always_true = lambda x: True

        result = self.stream.allMatch(always_true)

        self.assertTrue(result)

    def test_givenNoMatchingElements_whenCheckingAnyMatch_thenReturnFalse(self):
        always_false = lambda x: False

        result = self.stream.anyMatch(always_false)

        self.assertFalse(result)

    def test_whenCollectingToSet_thenReturnASetContainingAllElements(self):
        result_set = self.stream.toSet()

        self.assertEqual(len(self.COLLECTION), len(result_set))
        for item in self.COLLECTION:
            self.assertTrue(item in result_set)

    def test_givenAListOfPairs_whenCollectingToDict_thenExpandPairsToKeyValue(self):
        dictionary = self.stream.map(lambda x: (x, StreamTest.DIVIDES_BY_THREE(x))).toDict()

        self.assertEqual(len(self.COLLECTION), len(dictionary.keys()))
        for i in self.COLLECTION:
            self.assertEqual(dictionary[i], StreamTest.DIVIDES_BY_THREE(i))

    def test_whenForEach_thenCallFunctionOnAllItems(self):
        result = []
        add_to_list = lambda x: result.append(x)

        self.stream.forEach(add_to_list)

        self.assertEqual(self.COLLECTION, result)

    def test_givenCollectionOfTuples_whenForEach_thenExpandTuplesWhenCallingFunction(self):
        result = []
        self.stream = Stream([(1, -1), (2, -2)])
        add_sum_to_list = lambda x, y: result.append(x + y)

        self.stream.forEach(add_sum_to_list)

        self.assertEqual([0, 0], result)

    def test_givenFunctionWithTwoParameters_whenMapping_thenExpandTuplesWhenCallingFunction(self):
        result = self.stream.map(lambda x: (x, x)).map(lambda x, y: x - y).toList()

        self.assertEqual([0 for i in self.COLLECTION], result)

    def test_givenFunctionWithTwoParameters_whenFiltering_thenExpandTuplesWhenCallingFunction(self):
        result = self.stream.map(lambda x: (x, x)).filter(lambda x, y: x == y).toList()

        self.assertEqual([(i, i) for i in self.COLLECTION], result)

    def test_givenFunctionWithTwoParameters_whenFindingFirstMatch_thenExpandTuplesWhenCallingFunction(self):
        result = self.stream.map(lambda x: (x, x)).firstMatch(lambda x, y: x == y)

        self.assertEqual((self.COLLECTION[0], self.COLLECTION[0]), result)

    def test_givenFunctionWithTwoParameters_whenIteratingOverScalars_thenThrowTypeError(self):
        with self.assertRaises(TypeError):
            self.stream.map(lambda x, y: x + y).toList()

    def test_givenStreamOfLists_whenFlattening_thenReturnStreamOfConcatenatedLists(self):
        result = Stream(self.BUMPY_COLLECTION).flat().toList()

        self.assertEqual(self.COLLECTION, result)

    def test_givenNoMatchingElements_whenCheckingNoneMatch_thenReturnTrue(self):
        always_false = lambda x: False

        result = Stream(self.COLLECTION).noneMatch(always_false)

        self.assertTrue(result)

    def test_givenMatchingElements_whenCheckingNoneMatch_thenReturnFalse(self):
        alwasy_true = lambda x: True

        result = Stream(self.COLLECTION).noneMatch(alwasy_true)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
