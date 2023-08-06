# RDSR Navigator
[![Downloads](https://pepy.tech/badge/rdsr-navigator)](https://pepy.tech/project/rdsr-navigator)
[![Downloads](https://pepy.tech/badge/rdsr-navigator/week)](https://pepy.tech/project/rdsr-navigator/week)

A package for extracting data from [DICOM](https://www.dicomstandard.org/) RDSR files. The focus of this project is to extract data. It is not possible to modify files. The project is currently in early development and things might not work exactly how you expect. The public API is not yet stable, please keep this in mind.

> The package is intended for **RESEARCH USE ONLY, NOT FOR CLINICAL USE**.

## Getting started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

RDSR Navigator is written in Python 3.6 and uses [pydicom](https://pydicom.github.io/). Therefore make sure you are running Python 3.6 or later and make sure pydicom is installed. If pydicom is not installed, use the command below to install pydicom.

    $ pip install pydicom

### Installation

RDSR Navigator is available on pypi and can be installed using the following command.

    $ pip install rdsr_navigator

Now, you are ready to start using RDSR navigator.

## Usage

### Read file

To open an RDSR file, type the following.

```python
    >>> import rdsr_navigator as nav
    >>> rdsr_obj = nav.read_file(r'C:\rdsr_file.dcm')
```

The input argument to `read_file` is a `str` containing the path to an RDSR file. Other supported data types are `pathlib` and `pydicom` objects.

### Extract data

Data is extracted by first navigating through the RDSR hierarchy using the concept names. All concept names are given in lower case, separated by underscores ("_"). In the example below we are extracting the value from "Procedure Reported".

```python
    >>> rdsr_obj['procedure_reported'].value

    'Projection X-Ray'
```

Data can also be extracted by using the code value and coding scheme designator separated by a colon (":"). This is shown in the example below.

```python
    >>> rdsr_obj['121058:DCM'].value

    'Projection X-Ray'
```

When the square brackets are used, the first matched concept name is returned. This is inappropriate if several entries with the same concept name exist on the same level. To iterate entries with the same concept name, use the `get_all` method.

```python
    >>> for irr_event in sr_obj.get_all('irradiation_event_x-ray_data')):
            print(irr_event['dose_area_product'].value)

    (1.9632189e-7, 'Gy.m2')
    (1.1173212e-5, 'Gy.m2')
    (8.566802e-7, 'Gy.m2')
```

Drill deeper into the hierarchy by adding more concept names in the square brackets.

```python
    >>> rdsr_obj['procedure_reported', 'has_intent'].value

    'Combined Diagnostic and Therapeutic Procedure'
```

## Jupyter notebook integration

The RDSR navigator classes are integrated with [jupyter notebooks](http://jupyter.org/).

+ Data is nicely displayed in tabular form.
+ Tab completion is available when accessing data using square brackets.

## Supported value types

Currently, only a few value types are supported. The supported value types are listed below.

+ Code Meaning
+ Date Time
+ Measured Values
+ Text Value
+ UID

## License

This project is licensed under the MIT License - see the LICENSE file for details.
