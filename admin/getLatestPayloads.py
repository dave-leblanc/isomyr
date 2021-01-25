#!/usr/bin/python
from cStringIO import StringIO

from twisted.internet import reactor
from twisted.internet.defer import DeferredList

from txspore import client
from txspore.url import atom, rest, static


sampleCreatureID = "500327625969"
sampleUserName = "oubiwann"
sampleSporecastID = "500320272789"
samplePartFilename = "ce_grasper_radial_02"
samplePaintFilename = "BE_zany_37"

resources = [
    (rest, "dailyStatsURL", (), {}),
    (rest, "creatureStatsURL", (sampleCreatureID,), {}),
    (rest, "profileInfoURL", (sampleUserName,), {}),
    (rest, "assetsForUserURL", (sampleUserName, 0, 4), {}),
    (rest, "sporeCastsForUserURL", (sampleUserName,), {}),
    (rest, "assetsForSporeCastURL", (sampleSporecastID, 0, 3), {}),
    (rest, "achievementsForUserURL", (sampleUserName, 0, 2), {}),
    (rest, "infoForAssetURL", (sampleCreatureID,), {}),
    (rest, "commentsForAssetURL", (sampleCreatureID, 0, 2), {}),
    (rest, "buddiesForUserURL", (sampleUserName, 0, 2), {}),
    (rest, "assetSearchURL", ("MAXIS_MADE", 0, 4, "CREATURE"), {}),
    (data, "largeCardURL", (sampleCreatureID,), {}),
    (data, "assetDataXMLURL", (sampleCreatureID,), {}),
    (data, "assetDataLargePNGURL", (sampleCreatureID,), {}),
    (data, "assetDataSmallPNGURL", (sampleCreatureID,), {}),
    (data, "achievementDataXMLURL", (), {}),
    (data, "achievementIconURL", (achievementID,), {}),
    (data, "partInfoURL", ("creatureblockmap",), {}),
    (data, "partInfoURL", ("limbblockmap",), {}),
    (data, "partInfoURL", ("buildingblockmap",), {}),
    (data, "partInfoURL", ("vehicleblockmap",), {}),
    (data, "partInfoURL", ("blockmap",), {}),
    (data, "partIconURL", (samplePartFilename,), {}),
    (data, "paintInfoURL", (), {}),
    (data, "paintIconURL", (samplePaintFilename,), {}),
    (atom, "assetsForUserURL", (sampleUserName,), {}),
    (atom, "eventsForUserURL", (sampleUserName,), {}),
    (atom, "eventsForAssetURL", (sampleCreatureID,), {}),
    (atom, "sporeCastFeedURL", (sampleSporecastID,), {}),
    (atom, "assetSearchURL", ("MAXIS_MADE",0, 5), {}),

]


def correlateData(result, functionName, type, args):
    functionName = functionName[0].upper() + functionName[1:]
    if functionName == "PartInfoURL":
        prepend = args[0][0].upper() + args[0][1:]
        functionName = prepend.replace("blockmap", "BlockMap") + functionName
    variableName = "sample%s%s" % (
        type, functionName.replace("URL", "Response"))
    return (variableName, result)


def getTypeForModule(module):
    if module == rest:
        type = "REST"
    elif module == static:
        type = "StaticData"
    elif module == atom:
        type = "Atom"
    return type


def getPayloads():
    deferreds = []
    asyncClient = client.AsyncClient()
    for module, functionName, args, kwds in resources:
        resource_url = getattr(module, functionName)(*args, **kwds)
        d = asyncClient.openURL(resource_url)
        d.addCallback(correlateData, functionName, getTypeForModule(module),
                      args)
        deferreds.append(d)
    return DeferredList(deferreds)


def processData(results):
    output = StringIO()
    output.write("# -*- coding: utf-8 -*-\n\n")
    for success, result in results:
        variableName, data = result
        if not data.startswith("<"):
            data = variableName + " BINARY DATA"
        output.write('%s = """\n%s"""\n\n\n' % (variableName, data))
    fh = open("txspore/testing/payload.py", "w+")
    fh.write(output.getvalue())
    fh.close()


def printError(error):
    print error.getErrorMessage()


def finish(ignored):
    reactor.stop()


if __name__ == "__main__":
    d = getPayloads()
    d.addCallback(processData)
    d.addErrback(printError)
    d.addCallback(finish)
    reactor.run()
