from time import sleep


class TailingTextBuffer(object):

    def __init__(self, maxWidth=50, maxLines=0):
        self.maxWidth = maxWidth
        self.maxLines = maxLines
        self.lines = []

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


text = TailingTextBuffer(maxLines=5)
while True:
    text.write("This is some text. ")
    print len(text)
    print text.read()
    print
    sleep(2)
