from setuptools import setup, find_packages


long_description = """Generate GeoJSON data for testing,
designed to expose edge cases in your code.
Implemented as a custom extension of hypothesis.

Documentation: https://github.com/mapbox/hypothesis_geojson

Hypothesis home: https://github.com/HypothesisWorks/hypothesis-python
"""


with open('hypothesis_geojson/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split('=')[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            break


setup(
    author=u"Matthew Perry",
    author_email='mperry@mapbox.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: GIS'],
    description=u"Hypothesis extension for testing with GeoJSON",
    entry_points="""
        [rasterio.rio_plugins]
        edge-features=hypothesis_geojson.scripts.edge_features:main""",
    extras_require={
        'test': ['pytest', 'pytest-cov']},
    include_package_date=True,
    install_requires=['hypothesis'],
    keywords='',
    license='BSD',
    long_description=long_description,
    name='hypothesis_geojson',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    url='https://github.com/mapbox/hypothesis-geojson',
    version=version,
    zip_safe=False,
)
