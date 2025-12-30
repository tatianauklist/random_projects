import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description="Simple tool to test project readiness.")
    parser.add_argument("-i","--interactive", action="store_true")
    parser.add_argument("-p","--project", type=str, help="Project Name")
    return parser.parse_args()