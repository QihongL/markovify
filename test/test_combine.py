import unittest
import markovify
import sys, os
import operator

def get_sorted(chain_json):
    return sorted(chain_json, key=operator.itemgetter(0))

class MarkovifyTest(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(os.path.dirname(__file__), "texts/sherlock.txt")) as f:
            self.sherlock = f.read()

    def test_simple(self):
        text_model = markovify.Text(self.sherlock)
        combo = markovify.combine([ text_model, text_model ], [ 0.5, 0.5 ])
        assert(combo.chain.model == text_model.chain.model)

    def test_double_weighted(self):
        text_model = markovify.Text(self.sherlock)
        combo = markovify.combine([ text_model, text_model ])
        assert(combo.chain.model != text_model.chain.model)

    def test_combine_chains(self):
        chain = markovify.Text(self.sherlock).chain
        combo = markovify.combine([ chain, chain ])

    def test_combine_dicts(self):
        _dict = markovify.Text(self.sherlock).chain.model
        combo = markovify.combine([ _dict, _dict ])

    def test_combine_lists(self):
        _list = list(markovify.Text(self.sherlock).chain.model.items())
        combo = markovify.combine([ _list, _list ])

    def test_bad_types(self):
        with self.assertRaises(Exception) as context:
            combo = markovify.combine([ "testing", "testing" ])

    def test_bad_weights(self):
        with self.assertRaises(Exception) as context:
            text_model = markovify.Text(self.sherlock)
            combo = markovify.combine([ text_model, text_model ], [ 0.5  ])

    def test_mismatched_state_sizes(self):
        with self.assertRaises(Exception) as context:
            text_model_a = markovify.Text(self.sherlock, state_size=2)
            text_model_b = markovify.Text(self.sherlock, state_size=3)
            combo = markovify.combine([ text_model_a, text_model_b ])

    def test_mismatched_model_types(self):
        with self.assertRaises(Exception) as context:
            text_model_a = markovify.Text(self.sherlock)
            text_model_b = markovify.NewlineText(self.sherlock)
            combo = markovify.combine([ text_model_a, text_model_b ])

if __name__ == '__main__':
    unittest.main()

