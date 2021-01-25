from isomyr.gui.component import GUIComponent


class TailingTextBuffer(object):
    """
    This is a text buffer class that presents only the "most recent" text that
    was pushed to the buffer (i.e., the "tail" text). 
    
    After repeated writes, the amount of text stored in the object at any given
    time is determined by the maximum defined number of lines and the
    configured maximum width of each line.
    """
    def __init__(self, text="", maxWidth=50, maxLines=0):
        self.maxWidth = maxWidth
        self.maxLines = maxLines
        self.lines = []
        if text:
            self.write(text)

    def __len__(self):
        return len("".join(self.lines))

    def justifyText(self, text):
        lastLine = -1
        # Get the last line, if it's there; if not, just append the text.
        #try:
        #    self.lines[lastLine] += text
        #except IndexError:
        #    self.lines.append(text)
        self.lines.append(text)
        totalLength = len(self.lines[lastLine])
        # XXX This can be improved to split lines in such a way that words are
        # not bisected.
        if totalLength > self.maxWidth:
            trimmedLine = self.lines[lastLine][:self.maxWidth]
            remainderIndex = totalLength - self.maxWidth
            remainder = self.lines[lastLine][-remainderIndex:]
            self.lines[lastLine] = trimmedLine
            if remainder:
                self.justifyText(remainder)

    def write(self, text):
        for line in text.splitlines():
            self.justifyText(line)
        if len(self.lines) >= self.maxLines:
            reverseIndex = self.maxLines
            self.lines = self.lines[-reverseIndex:]

    def read(self):
        return "\n".join(self.lines)


class TextAreaView(GUIComponent):

    def __init__(self, default="", rectangle=None, font=None,
                 foreground=(255, 255, 255), background=(0, 0, 0), *args,
                 **kwds):
        super(TextAreaView, self).__init__(*args, **kwds)
        self.default = default
        if not rectangle:
            rectangle = pygame.Rect(
                self.parent.textAreaPosition + self.parent.textAreaSize)
        self.rectangle = rectangle
        if not font:
            font = self.parent.font
        self.font = font
        self.foreground = foreground
        self.background = background
        self.maxWidth, self.maxLines = self.getMaxDimensions()
        self.text = TailingTextBuffer(
            text=default, maxWidth=self.maxWidth, maxLines=self.maxLines)

    def getMaxDimensions(self):
        """
        Get the maximum number of characters wide and tall for the size of the
        provided surface and font.
        """
        # This assumes a monotype font; knowing the size of every letter, we
        # can do these calculations in advance. If we don't use a monotype
        # font, this is going to be trickier.
        self.baseWidth, self.baseHeight = self.font.size("a")
        pixelWidth, pixelHeight = self.rectangle.size
        return (pixelWidth / self.baseWidth, pixelHeight / self.baseHeight)

    def updateDisplay(self, text, antialias=False, color=None,
                      background=None):
        surface = self.parent.getSurface()
        if not color:
            color = self.foreground
        if not background:
            background = self.background
        self.text.write(text)
        X, Y = (0, 1)
        height = self.parent.textAreaPosition[Y]
        for line in self.text.lines:
            if not line:
                line = " "
            data = line.ljust(self.maxWidth)
            rendered = self.font.render(data, antialias, color, background)
            surface.blit(rendered, (10, height))
            #surface.blit(rendered, self.parent.getSurface(), self.rectangle)
            height += self.baseHeight
        super(TextAreaView, self).updateDisplay(self.rectangle)
