# SF-Data Structural Schema

[![unit tests](https://github.com/SocialFinanceDigitalLabs/sfdata-schema/actions/workflows/tests.yml/badge.svg)](https://github.com/SocialFinanceDigitalLabs/sfdata-schema/actions)
[![codecov](https://codecov.io/gh/SocialFinanceDigitalLabs/sfdata-schema/branch/main/graph/badge.svg?token=Q759W17AIT)](https://codecov.io/gh/SocialFinanceDigitalLabs/sfdata-schema)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a python library for documenting "anticipated" data structures. At Social Finance we often deal with
data that is supposed to have a certain structure, but very frequently the structure is not enforced. Variants
in column names, value formats (such as dates), no common way of indicating 'which' table a representation belongs
to etc.

The purpose of this library is to provide a way to document the expected structure of data, and to provide a way to
conform data to that structure and log any deviations.

Although the structure is primarly for tabular data, it can be used for any data structure, including hierarchical data
such as JSON & XML and provides a way to transform these into a relational datamodel.

The tool also includes the ability to generate documentation for the model, including a relational diagram.

![Entity Relationship Diagram](./docs/images/sample_erd.png)

Schemas can be defined in code, in JSON or in YAML, and can include additional metadata such as descriptions, and, in
the sample above, pretty colours for your documentation.