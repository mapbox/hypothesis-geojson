import sys

from hypothesis_geojson import features
from hypothesis_geojson.scripts.edge_features import main


def test_features():
    for i in range(60):
        features().example()  # TODO what to assert?


def test_cli_main(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['10'])
    main()
