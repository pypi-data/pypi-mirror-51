# DInk Python Library

The DInk Python library provides a pythonic interface to the DInk API. It includes an API client class, and a set of resource classes.


## Installation

```
pip install dink
```

## Requirements

- Python 3.7+


# Usage

```Python

import dink
import zipfile


client = dink.Client('your_api_key...')

assets = zipfile.ZipFile()
assets.write('includes/footer.html')
assets.write('css/document.css')
assets.write('images/logo.png')
assets.write('fonts/company-font.otf')

pdfs = dink.resource.PDF.create(
    template_html='''
<html>
    <head>
        <title>{{ title }}</title>
        <link
            rel="stylesheet"
            type="text/css"
            media="print"
            href="file://css/document.css"
        >
    </head>
    <body>
        <img src="images/logo.png" alt="logo">
        <h1>{{ title }}</h1>
        <main>
            {{ name }} you worked {{ hours_worked }} hours this week you
            {% if hours > 40 %}
                star!
            {% else %}
                lazy bum!
            {% endif %}

            <img
                src="chart://hours_chart"
                alt="Hours worked each day this week"
                >
        </main>
        {% include 'includes/footer.html' %}
    </body>
</html>
    ''',
    global_vars={
        'title': 'Weekly sales report'
    },
    document_args={
        'burt': {
            'hours_worked': 10,
            'hours_chart': {
                'chart_type': 'bar',
                'data': [{'data':  [1, 1, 2, 4, 2]}],
                'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'spacing': 0.2
            }
        },
        'harry': {
            'hours_worked': 44,
            'hours_chart': {
                'chart_type': 'bar',
                'data': [{'data':  [8, 8, 10, 8, 10]}],
                'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'spacing': 0.2
            }
        }
    },
    assets=assets
)

print(pds['burt'])

>> {'store_key': 'burt.ue32uw.pdf', 'uid': 'ue32uw'}

```
