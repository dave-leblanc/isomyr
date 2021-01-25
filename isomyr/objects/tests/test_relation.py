from unittest import TestCase

from isomyr.objects.relation import RelationshipMixin


class RelationshipMixinTestCase(TestCase):

    def test_setParent(self):
        t1 = RelationshipMixin("parent")
        t2 = RelationshipMixin("child")
        t2.setParent(t1)
        self.assertEquals(t2.parent, t1)
        self.assertEquals(t1.children, [t2])
