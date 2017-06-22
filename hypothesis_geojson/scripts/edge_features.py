#!/usr/bin/env python
import sys
import json
from hypothesis_geojson import features


def main():
    try:
        n = int(sys.argv[1])
    except IndexError:
        n = 10

    for i in range(n):
        print(json.dumps(features().example()))


if __name__ == "__main__":
    main()
