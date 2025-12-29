import yaml

def loadChecklist(fileType):
    if "software" in fileType:
        filePath = '/Users/tatianauklist/plotholes/PreFlightCheck/configs/softwaresample.yaml'
        with open(filePath, 'r') as f:
            data = yaml.safe_load(f)
    elif "event" in fileType:
        filePath = '/Users/tatianauklist/plotholes/PreFlightCheck/configs/eventssample.yaml'
        with open(filePath, 'r') as f:
            data = yaml.safe_load(f)
    return data, filePath

def saveChecklist(data, filePath):
    with open(filePath, 'w') as f:
        yaml.dump(data,f, sort_keys=False)







