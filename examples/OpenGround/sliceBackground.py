import os

from PIL import Image, ImageDraw


# where to look for files
dirname = os.path.dirname(__file__)
# define proportions for individual slice
sliceSizeX, sliceSizeY = (348, 176)


def getMask(sliceSize):
    """
    Create a diamond in the right proportions that will mask a slice, showing
    just the traversable areas
    """
    black = 0
    white = 255
    mask = Image.new("RGBA", sliceSize, (black, black, black))

    topPoint = (mask.size[0] / 2, 0)
    bottomPoint = (mask.size[0] / 2, mask.size[1])
    leftPoint = (0, mask.size[1] / 2)
    rightPoint = (mask.size[0], mask.size[1] /2)

    diamond = Image.new("L", sliceSize, white)
    shape = ImageDraw.Draw(diamond)
    shape.polygon([leftPoint, topPoint, rightPoint, bottomPoint], fill=black)
    mask.putalpha(diamond)
    return mask


def paintDiamond(original):
    im = original.copy()

    topLeftCorner = (0, 0)
    topRightCorner = (im.size[0], 0)
    bottomRightCorner = (im.size[0], im.size[1])
    bottomLeftCorner = (0, im.size[1])

    topPoint = (im.size[0] / 2, 0)
    bottomPoint = (im.size[0] / 2, im.size[1])
    leftPoint = (0, im.size[1] / 2)
    rightPoint = (im.size[0], im.size[1] /2)

    black = 0
    shape = ImageDraw.Draw(im)
    shape.polygon([leftPoint, topPoint, topLeftCorner], black)
    shape.polygon([topPoint, rightPoint, topRightCorner], black)
    shape.polygon([rightPoint, bottomPoint, bottomRightCorner], black)
    shape.polygon([bottomPoint, leftPoint, bottomLeftCorner], black)

    return im


def createImageSlice(fullImage, outFile, startingPointX, startingPointY):
    # get the mask for diamond shape
    mask = getMask((sliceSizeX, sliceSizeY))
    # calculate all slice points based on starting point and slice proportions
    maxX, maxY = fullImage.size
    box = (startingPointX - sliceSizeX / 2,
           startingPointY - sliceSizeY / 2,
           startingPointX + sliceSizeX / 2,
           startingPointY + sliceSizeY / 2)
    slice = paintDiamond(fullImage.crop(box))
    # XXX Pad the image with 184 pixels of black space above and 26 pixels of
    # black space on either side for use in Isomyr.
    padded = Image.new(slice.mode, (400, 360), (0, 0, 0))
    padded.paste(slice, (26, 184))
    padded.save(os.path.join(dirname, outFile))


def createImageSlices(fullImage, startingPoints):
    for startingPointX, startingPointY in startingPoints:
        outFile = "backgrounds/%sx%s.png" % (startingPointX, startingPointY)
        createImageSlice(fullImage, outFile, startingPointX, startingPointY)
        


if __name__ == "__main__":

    # load image
    fullImage = Image.open(
        os.path.join(dirname, "background.png")).convert("RGB")
    # define center starting point
    originX, originY = (1084, 302)
    tiles = [
        # column 1
        (originX - 5 * (sliceSizeX / 2), originY - sliceSizeY / 2),
        (originX - 5 * (sliceSizeX / 2), originY + sliceSizeY / 2),
        # column 2
        (originX - 2 * sliceSizeX, originY - sliceSizeY),
        (originX - 2 * sliceSizeX, originY),
        # column 3
        (originX - 3 * (sliceSizeX / 2), originY - sliceSizeY / 2),
        (originX - 3 * (sliceSizeX / 2), originY + sliceSizeY / 2),
        # column 4
        (originX - sliceSizeX, originY - sliceSizeY),
        (originX - sliceSizeX, originY),
        # column 5
        (originX - sliceSizeX / 2, originY - sliceSizeY / 2),
        (originX - sliceSizeX / 2, originY + sliceSizeY / 2),
        # column 6
        (originX, originY - sliceSizeY),
        (originX, originY),
        # column 7
        (originX + sliceSizeX / 2, originY - sliceSizeY / 2),
        (originX + sliceSizeX / 2, originY + sliceSizeY / 2),
        ]
    createImageSlices(fullImage, tiles)
