import yaml

def loadChecklist(fileType):
    if fileType == "software":
        with open('softwaresample.yaml', 'r') as f:
            data = yaml.safe_load(f)
    else:
        with open('eventssample.yaml', 'r') as f:
            data = yaml.safe_load(f)
    return data







