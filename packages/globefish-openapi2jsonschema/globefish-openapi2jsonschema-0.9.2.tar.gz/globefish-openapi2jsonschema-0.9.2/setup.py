from setuptools import setup

setup(
    name='globefish-openapi2jsonschema',
    author='Marshall Ma',
    author_email='mayongcong@gmail.com',
    version='0.9.2',
    license='Apache License 2.0',
    packages=['openapi2jsonschema',],
    install_requires=[
        'jsonref',
        'pyyaml',
        'click',
        'colorama',
    ],
    tests_require=[

    ],
    entry_points={
        'console_scripts': [
            'openapi2jsonschema = openapi2jsonschema.command:default'
       ]
    },
    keywords = 'openapi, jsonschema',
    description = 'A utility to extract JSON Schema from a valid OpenAPI specification.',
    url = "https://github.com/ufonion/openapi2jsonschema",
)
