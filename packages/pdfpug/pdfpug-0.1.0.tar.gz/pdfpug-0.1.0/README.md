# Python PDF Generator

**PdfPug** is a simple Python PDF creator using easy to use APIs. It provides a variety
of components and the ability to customise these components to suit different use cases.

**Note: PdfPug is still very new and as such the APIs are not stable. It can be
considered to be in pre-alpha stage!**

## Installation

``` {.sourceCode .bash}
$ pip install pdfpug
```

## Usage

``` {.sourceCode .python}
>>> from pdfpug import Header, Paragraph, PdfReport
>>> intro_header = Header('Introduction to PdfPug')
>>> para = Paragraph(
...     "Lorem Ipsum is <b>simply</b> <u>dummy</u> text of the printing and typesetting "
...     "industry. Lorem Ipsum has been the industry's standard dummy text "
...     "ever since the 1500s, when an unknown printer took a galley of type"
...     " and scrambled it to make a type specimen book. It has survived not "
...     "only five centuries, but also the leap into electronic typesetting, "
...     "remaining essentially unchanged. It was popularised in the 1960s with "
...     "the release of Letraset sheets containing Lorem Ipsum passages, and "
...     "more recently with desktop publishing software like Aldus PageMaker "
...     "including versions of Lorem Ipsum."
... )
>>> report = PdfReport()
>>> report.add_element(intro_header)
>>> report.add_element(para)
>>> report.generate_pdf('pdfpug-report.pdf')
```

## Documentation

Documentation is available at <https://pdfpug.readthedocs.io/en/latest/>