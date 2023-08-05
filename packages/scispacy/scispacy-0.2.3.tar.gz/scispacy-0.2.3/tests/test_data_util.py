# pylint: disable=no-self-use,invalid-name
import os
import unittest
import shutil


from scispacy.data_util import read_med_mentions, med_mentions_example_iterator
from scispacy.data_util import read_ner_from_tsv

class TestDataUtil(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.TEST_DIR = "/tmp/scispacy"
        os.makedirs(self.TEST_DIR, exist_ok=True)

        self.med_mentions = "tests/fixtures/med_mentions.txt"
        self.ner_tsv = "tests/fixtures/ner_test.tsv"

    def tearDown(self):
        shutil.rmtree(self.TEST_DIR)

    def test_example_iterator(self):
        iterator = med_mentions_example_iterator(self.med_mentions)
        for example in iterator:
            assert example.text == example.title + " " + example.abstract

            for entity in example.entities:
                assert entity.start < entity.end
                assert entity.start < len(example.text)
                assert entity.end < len(example.text)
                assert entity.mention_text == example.text[entity.start: entity.end]

    def test_read_med_mentions(self):
        examples = read_med_mentions(self.med_mentions)
        assert len(examples) == 3


    def test_read_ner_from_tsv(self):

        data = read_ner_from_tsv(self.ner_tsv)
        assert len(data) == 4       
        example = data[0]
        assert example[0] == 'Intraocular pressure in genetically distinct mice : an update and strain survey'
        assert example[1] ==  {'entities': [(24, 35, 'SO'), (45, 49, 'TAXON')]}
        example = data[1]
        assert example[0] == 'Abstract'
        assert example[1] ==  {'entities': []}
        example = data[2]
        assert example[0] == 'Background'
        assert example[1] ==  {'entities': []}
        example = data[3]
        assert example[0] == 'Little is known about genetic factors affecting intraocular pressure ( IOP ) in mice and other mammals .'
        assert example[1] ==  {'entities': [(22, 29, 'SO'), (80, 84, 'TAXON'), (95, 102, 'TAXON')]}
