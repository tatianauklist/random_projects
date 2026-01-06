import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description="Simple tool to test project readiness.")
    parser.add_argument("-i","--interactive", action="store_true")
    parser.add_argument("-p","--project", type=str, help="Project Name")
    parser.add_argument("-c","--create", action="store_true")
    return parser.parse_args()