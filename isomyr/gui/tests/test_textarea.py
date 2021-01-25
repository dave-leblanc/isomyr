from unittest import TestCase

from isomyr.gui.textarea import TailingTextBuffer


class TailingTextBufferTestCase(TestCase):

    def test_creation_defaults(self):
        buffer = TailingTextBuffer()
        self.assertEquals(buffer.maxWidth, 50)
        self.assertEquals(buffer.maxLines, 0)
        self.assertEquals(buffer.lines, [])

    def test_creation(self):
        buffer = TailingTextBuffer("testing ...", maxWidth=4, maxLines=2)
        self.assertEquals(buffer.maxWidth, 4)
        self.assertEquals(buffer.maxLines, 2)
        self.assertEquals(buffer.lines, ['ing ', '...'])

    def test_length(self):
        buffer = TailingTextBuffer("testing ...", maxWidth=80, maxLines=20)
        self.assertEquals(len(buffer), 11)
        buffer = TailingTextBuffer("testing ...", maxWidth=4, maxLines=20)
        self.assertEquals(len(buffer), 11)
        buffer = TailingTextBuffer("testing ...", maxWidth=4, maxLines=2)
        self.assertEquals(len(buffer), 7)

    def test_justifyText(self):
        buffer = TailingTextBuffer("testing ...", maxWidth=9, maxLines=2)
        self.assertEquals(buffer.lines, ['testing .', '..'])
        buffer.justifyText("some more text!")
        self.assertEquals(
            buffer.lines, ['testing .', '..', 'some more', ' text!'])

    def test_write(self):
        buffer = TailingTextBuffer("testing ...", maxWidth=9, maxLines=2)
        self.assertEquals(buffer.lines, ['testing .', '..'])
        buffer.write("some more text!")
        self.assertEquals(buffer.lines, ['some more', ' text!'])

    def test_writeNewLines(self):
        buffer = TailingTextBuffer("testing ...", maxWidth=9, maxLines=20)
        self.assertEquals(buffer.lines, ['testing .', '..'])
        buffer.write("some\nmore\n\ntext!")
        self.assertEquals(
            buffer.lines,
            ['testing .', '..', 'some', 'more', '', 'text!'])

    def test_read(self):
        buffer = TailingTextBuffer("testing ...", maxWidth=9, maxLines=20)
        self.assertEquals(buffer.lines, ['testing .', '..'])
        buffer.write("some\nmore\n\ntext!")
        result = buffer.read()
        self.assertEquals(result, "testing .\n..\nsome\nmore\n\ntext!")
