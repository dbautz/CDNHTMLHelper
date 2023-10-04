# cdn_html_helper README

The `CDNHTMLHelper` is a Python utility for generating HTML tags that link to files hosted on the [jsDelivr Content Delivery Network (CDN)](https://www.jsdelivr.com/). This class simplifies the process of including external JavaScript and CSS files in your web application by providing a programmatic way to generate HTML tags for these resources.

## Features

-   Generate HTML tags for including JavaScript and CSS files from jsDelivr CDN.
-   Fetch package information, including available versions and default files.
-   Retrieve Subresource Integrity (SRI) hashes from the jsDelivr API to ensure file integrity and security.
-   Optional integration with Flask applications to easily include resources in your templates.

## Usage

### Initialization

You can create an instance of the `CDNHTMLHelper` class by simply instantiating it:

```python
from CDNHTMLHelper import CDNHTMLHelper

cdn_html_helper = CDNHTMLHelper()
```

Optionally, if you are using the Flask web framework, you can pass your Flask application instance to the constructor. This allows you to easily integrate `CDNHTMLHelper` into your Flask templates:

```python
from CDNHTMLHelper import CDNHTMLHelper
from flask import Flask

app = Flask(__name__)
cdn_html_helper = CDNHTMLHelper(app)
```

### Adding a Package

To add a package to the `CDNHTMLHelper` instance, use the `use` method. This method fetches package information from jsDelivr and adds it to the instance's data dictionary. You can specify the package name, version (default is "latest"), and a dictionary of files you want to include:

```python
cdn_html_helper.use("package-name", version="1.0.0", files={"alias1": "file1.js", "alias2": "file2.css"})
```

### Generating HTML Tags

To generate HTML tags for the added package and its files, use the `get` method. Provide the package name and the alias of the file you want to include in your HTML:

```python
html_tag = cdn_html_helper.get("package-name", "alias1")
```

The `html_tag` variable will contain the HTML tag for the specified file, ready to be inserted into your web page.

### Flask Integration (Optional)

If you are using Flask and passed your Flask application instance to the `CDNHTMLHelper` constructor, you can use the `cdn_html_helper` variable directly in your Flask templates to generate HTML tags. Example usage in a Flask template:

```html
<!DOCTYPE html>
<html>
    <head>
        {{ cdn_html_helper.get("package-name", "alias1") }}
    </head>
    <body>
        <!-- Your web content here -->
    </body>
</html>
```

In this example, `{{ cdn_html_helper.get("package-name", "alias1") }}` generates and safely renders the HTML tag for the specified package file.

## Dependencies

The `CDNHTMLHelper` relies on the following external Python packages:

-   `requests`: Used for making HTTP requests to jsDelivr's API to fetch package information.
-   `markupsafe`: Used for safely rendering HTML tags when integrated with Flask applications.

The required dependencies are included in the `requirements.txt` file, which is shipped with this repository.

## Note

Make sure you have these dependencies installed in your Python environment before using the `CDNHTMLHelper`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contribution

Contributions and bug reports are welcome! Please feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/your/repository).

Enjoy using the `CDNHTMLHelper` class to simplify the process of including external JavaScript and CSS files in your web applications!
