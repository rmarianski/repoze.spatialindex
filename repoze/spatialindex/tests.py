import unittest

class SpatialIndexTest(unittest.TestCase):

    def _getTargetClass(self):
        from repoze.spatialindex import SpatialIndex
        return SpatialIndex

    def _makeOne(self, *args):
        return self._getTargetClass()(*args)

    def test_index(self):
        instance = self._makeOne()
        instance.index_doc(1, (1, 2, 3, 4))
        instance.index_doc(2, (2, 2, 3, 4))
        docids = instance.apply((0, 0, 5, 5))
        self.assertEqual([1, 2], docids)

    def test_count(self):
        instance = self._makeOne()
        instance.index_doc(1, (1, 2, 3, 4))
        self.assertEqual(1, instance.count((0, 0, 5, 5)))

    def test_index_negative_docid(self):
        instance = self._makeOne()
        instance.index_doc(-1234, (1, 2, 3, 4))
        docids = instance.apply((0, 0, 5, 5))
        self.assertEqual([-1234], docids)

    def test_unindex(self):
        instance = self._makeOne()
        instance.index_doc(1, (1, 2, 3, 4))
        instance.unindex_doc(1)
        self.assertEqual(0, instance.count((0, 0, 5, 5)))

    def test_clear_memory(self):
        instance = self._makeOne()
        instance.index_doc(1, (1, 2, 3, 4))
        instance.clear()
        self.assertEqual(0, instance.count((0, 0, 5, 5)))

    def test_clear_disk(self):
        import tempfile
        basename = tempfile.gettempprefix()
        instance = self._makeOne(basename)
        instance.index_doc(1, (1, 2, 3, 4))
        instance.clear()
        self.assertEqual(0, instance.count((0, 0, 5, 5)))
        import os
        os.unlink('%s.%s' % (basename, 'dat'))
        os.unlink('%s.%s' % (basename, 'idx'))

    def test_index_out_of_bounds(self):
        instance = self._makeOne()
        instance.index_doc(1, (1, 2, 3, 4))
        docids = instance.apply((4, 4, 5, 5))
        self.assertEqual([], docids)
        self.assertEqual(0, instance.count((4, 4, 5, 5)))

class DummyModel(object):
    """create a dummy model to return bounds"""

    def __init__(self, bounds):
        self.bounds = bounds

class CatalogSpatialIndexTest(unittest.TestCase):

    def _getTargetClass(self):
        from repoze.spatialindex import CatalogSpatialIndex
        return CatalogSpatialIndex

    def _makeOne(self, fn=None):
        if fn is None:
            fn = lambda x,marker:x.bounds
        return self._getTargetClass()(fn)

    def test_index(self):
        instance = self._makeOne()
        instance.index_doc(1, DummyModel((1, 2, 3, 4)))
        docids = instance.apply((1, 1, 5, 5))
        self.assertEqual([1], docids)
        self.assertEqual(1, instance.count((1, 1, 5, 5)))

    def test_reindex(self):
        instance = self._makeOne()
        dummy_model = DummyModel((1, 2, 3, 4))
        instance.index_doc(1, dummy_model)
        instance.reindex_doc(1, dummy_model)
        docids = instance.apply((1, 1, 5, 5))
        self.assertEqual([1], docids)

    def test_unindex(self):
        instance = self._makeOne()
        instance.index_doc(1, DummyModel((1, 2, 3, 4)))
        instance.unindex_doc(1)
        docids = instance.apply((1, 1, 5, 5))
        self.assertEqual([], docids)
        self.assertEqual(0, instance.count((1, 1, 5, 5)))

class CatalogTest(unittest.TestCase):

    def test_catalog_index(self):
        from repoze.catalog.catalog import Catalog
        from repoze.spatialindex import CatalogSpatialIndex
        cat = Catalog()
        cat['bbox'] = CatalogSpatialIndex(lambda x,default:x.bounds)
        dummyobject = DummyObject((1, 2, 3, 4))
        cat.index_doc(1, dummyobject)
        docids = cat.search(bbox=(1, 1, 5, 5))
        self.assertEqual((1, [1]), docids)

class DummyObject(object):
    def __init__(self, bounds):
        self.bounds = bounds
