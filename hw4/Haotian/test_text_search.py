import os

from unittest import TestCase

from text_vectors import TextDocument, DocumentCollection, SearchEngine


class DocumentCollectionTest(TestCase):

    def setUp(self):
        test_doc_list = [TextDocument(text_and_id[0], text_and_id[1]) for text_and_id in
                         [("the cat sat on a mat", "doc1"),
                          ("a rose is a rose", "doc2"),
                          ("a summer in New York", "doc3")]]
        self.small_collection = DocumentCollection.from_document_list(test_doc_list)

        # TODO: uncomment in case tests need access to whole document collection.
        # this_dir = os.path.dirname(os.path.abspath(__file__))
        # document_dir = os.path.join(this_dir, os.pardir, '../../Stirnlappenbasilisk/src/data/enron/enron1/ham/')
        # self.large_collection = DocumentCollection.from_dir(document_dir, ".txt")

    def test_unknown_word_cosine(self):
        """ Return 0 if cosine similarity is called for documents with only out-of-vocabulary words. """
        # Document that only contains words that never occurred in the document collection.
        query_doc = TextDocument(text="unknownwords", id=None)
        # Some document from collection.
        collection_doc = self.small_collection.docid_to_doc["doc1"]
        # Similarity should be zero (instead of undefined).
        self.assertEqual(self.small_collection.cosine_similarity(query_doc, collection_doc), 0)

    ### added test ###
    def test_docs_with_all_tokens(self):
        """ Quoted tokens must appear as entire strings """
        collection_doc = self.small_collection.docid_to_doc["doc1"]
        self.assertEqual(self.small_collection.docs_with_all_tokens(["a mat"]), [])

    ### added functional test ###
    def test_from_dir_abspath(self):
        self.collection = DocumentCollection.from_dir("./data", ".txt")
        self.assertEqual(self.collection.term_to_docids["cat"], {"/Users/yehaotian/Studium/SymPro/sympro_privat/hw4/Haotian/data/test_snippets_abspath_doc.txt"})

class TextDocumentTest(TestCase):
    ### added functional test ###
    def setUp(self):
        self.test_file = TextDocument.from_file("test_from_file_doc.txt")


    def test_from_file(self):
        """ Extra blank space after possible non-char will also be stripped """
        self.assertEqual(self.test_file.text, "this is a sentence")

class SearchEngineTest(TestCase):

    def setUp(self):
        test_doc_list = [TextDocument(text_and_id[0], text_and_id[1]) for text_and_id in
                         [("the cat sat on a mat", "doc1"),
                          ("a rose is a rose", "doc2"),
                          ("a summer in New York", "doc3")]]
        self.small_collection = DocumentCollection.from_document_list(test_doc_list)
        self.test_engine = SearchEngine(self.small_collection.docid_to_doc["doc1"])

        self.test_doc = TextDocument("the cat sat on the mat", "doc1")
    ### added functional test ?? ###
    def test_snippets_no_substring(self):
        """ Return only exact matches of query token, not substring matches """
        for snippet in self.test_engine.snippets("at", self.test_doc):
            self.assertIsNone(snippet)

    ### added functional test ?? ###
    def test_snippets_no_dup(self):
        """ If a query contains the same token multiple times, only show one text snippet for it """
        for result1 in self.test_engine.snippets("sat sat", self.test_doc):
            for result2 in self.test_engine.snippets("sat", self.test_doc):
                self.assertEqual(result1, result2)

    ### added test ###
    # def test_snippets_abspath(self):
    #     """"""
    #     self.collection = DocumentCollection.from_dir(".", ".txt")
    #
    #     self.assertEqual(, "test_snippets_abspath_doc.txt")

        # self.assertEqual(self.test_engine.snippets("sat sat", self.test_doc), self.test_engine.snippets("sat", self.test_doc))
