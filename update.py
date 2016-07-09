from ScrapeTarget import ScrapeTarget
import json
import glob

scrapeTargets = []

for filename in glob.iglob('sites/*.json'):
    with open(filename,'r') as file:
        newsDef = json.load(file)
        scrapeTargets.append(ScrapeTarget(newsDef))

for i in scrapeTargets:
    i.load(cached=False)
    i.runXpaths()
    i.updateText()