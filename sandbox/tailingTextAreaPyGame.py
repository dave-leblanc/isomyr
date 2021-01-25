import pygame


class TailingTextBuffer(object):

    def __init__(self, text="", maxWidth=50, maxLines=0):
        self.maxWidth = maxWidth
        self.maxLines = maxLines
        self.lines = []
        if text:
            self.lines.append(text)

    def __len__(self):
        return len("".join(self.lines))

    def justifyText(self, text):
        accumulator = ""
        # Get the last line, if it's there; if not, just append the text.
        lastLine = -1
        try:
            self.lines[lastLine] += text
        except IndexError:
            self.lines.append(text)
        totalLength = len(self.lines[lastLine])
        if totalLength > self.maxWidth:
            trimmedLine = self.lines[lastLine][:self.maxWidth]
            remainderIndex = totalLength - self.maxWidth
            remainder = self.lines[lastLine][-remainderIndex:]
            self.lines[lastLine] = trimmedLine
            self.lines.append(remainder.lstrip())

    def write(self, text):
        self.justifyText(text)
        if len(self.lines) >= self.maxLines:
            reverseIndex = self.maxLines
            self.lines = self.lines[-reverseIndex:]

    def read(self):
        return "\n".join(self.lines)


class TextAreaWidget(object):

    def __init__(self, surface, default="", rectangle=None, font=None,
                 foreground=(255, 255, 255), background=(0, 0, 0)):
        self.surface = surface
        self.default = default

        if not rectangle:
            rectangle = pygame.Rect((40, 40, 300, 300))
        self.rectangle = rectangle
        if not font:
            font = pygame.font.SysFont(
                "bitstreamverasansmono", 11, bold=False, italic=False)
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
        return (pixelWidth/self.baseWidth, pixelHeight/self.baseHeight)

    def update(self, text, antialias=False, color=None, background=None):
        if not color:
            color = self.foreground
        if not background:
            background = self.background
        self.text.write(text)
        height = 0
        for line in self.text.lines:
            data = line.ljust(self.maxWidth)
            rendered = self.font.render(data, antialias, color, background)
            self.surface.blit(rendered, (0, height))
            height += self.baseHeight
        pygame.display.update()


pygame.init()
display = pygame.display.set_mode((400, 400))

widget = TextAreaWidget(
    display, default="This is some default text area widget text.")
text = TailingTextBuffer(maxLines=5)
quit = False
while not quit:
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            quit = True
    widget.update("This is some text. ")
    pygame.time.wait(1000)

