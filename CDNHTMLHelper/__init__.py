from functools import lru_cache

import requests
from markupsafe import Markup


class CDNHTMLHelper:
    """
    A class for generating HTML tags for files hosted on jsDelivr CDN.
    """

    CDN_URL = "https://cdn.jsdelivr.net"
    DATA_URL = "https://data.jsdelivr.com"
    API_RESOLVED_VERSION = "/v1/packages/npm/{package}/resolved"
    API_VERSION_METADATA = "/v1/packages/npm/{package}@{version}"
    API_ENTRYPOINTS = "/v1/packages/npm/{package}@{version}/entrypoints"
    TEMPLATE_STRINGS = {
        ".css": (
            '<link rel="stylesheet"'
            ' href="{cdn_url}/{repo}/{package}@{version}{name}"'
            ' integrity="sha256-{hash}" crossorigin="anonymous"/>'
        ),
        ".js": (
            '<script src="{cdn_url}/{repo}/{package}@{version}{name}"'
            ' integrity="sha256-{hash}"'
            ' crossorigin="anonymous"></script>'
        ),
        # Add more template strings for other file types if needed
    }

    def __init__(self, app=None):
        """
        Initializes a new instance of the CDNHTMLHelper class.

        Args:
            app: An optional Flask application instance.
        """
        self.data = {}
        self.app_name = type(app).__name__

        if self.app_name == "Flask":

            @app.context_processor
            def _():
                return dict(cdn_html_helper=self)

    def _get_hash_and_name(self, package, version, filename):
        """
        Gets the hash and name of a file in a package.

        Args:
            package: The name of the package.
            version: The version of the package.
            filename: The name of the file.

        Returns:
            A tuple containing the name and hash of the file.
        """
        r = requests.get(
            self.DATA_URL + self.API_VERSION_METADATA.format(package=package, version=version),
            params={"structure": "flat"},
        )

        for file in r.json().get("files", []):
            if file["name"].endswith(filename):
                return file["name"], file["hash"]

    def _get_default_files(self, package, version):
        """
        Gets the default files for a package version.

        Args:
            package: The name of the package.
            version: The version of the package.

        Returns:
            A dictionary containing the default files for the package version.
        """
        files = {}
        r = requests.get(
            self.DATA_URL + self.API_ENTRYPOINTS.format(package=package, version=version)
        )
        entrypoints = r.json().get("entrypoints", {})
        for key, value in entrypoints.items():
            if "file" in value:
                files[key] = value["file"]
        return files

    def use(self, package, version="latest", files={}):
        """
        Adds a package to the data dictionary.

        Args:
            package: The name of the package.
            version: The version of the package.
            files: A dictionary containing the files to be added to the package.

        Raises:
            Exception: If the package is not found.
        """
        self.data[package] = {"requested_version": version, "files": {}}

        r = requests.get(
            self.DATA_URL + self.API_RESOLVED_VERSION.format(package=package),
            params={"specifier": version},
        )
        data = r.json()
        if not data.get("version"):
            raise Exception(f"Package {package} not found")
        if not files:
            files = self._get_default_files(package, data["version"])
        for alias, filename in files.items():
            name, hash = self._get_hash_and_name(package, data["version"], filename)
            self.data[package]["files"][alias] = {
                "name": name,
                "package": package,
                "version": data["version"],
                "repo": "npm",
                "hash": hash,
            }

    def _find_matching_extension(self, filename):
        """
        Finds the matching extension for a filename.

        Args:
            filename: The name of the file.

        Returns:
            The matching extension for the file.
        """
        matching_extension = None
        for extension in self.TEMPLATE_STRINGS.keys():
            if filename.endswith(extension) and (
                matching_extension is None or len(extension) > len(matching_extension)
            ):
                matching_extension = extension
        return matching_extension

    @lru_cache(maxsize=None)
    def _get_string(self, package, alias):
        """
        Gets the HTML tag string for a file in a package.

        Args:
            package: The name of the package.
            alias: The alias of the file.

        Returns:
            The HTML tag string for the file.
        """
        file = self.data.get(package, {}).get("files", {}).get(alias)
        if not file:
            return f"<!-- File not found -->"

        filetype = self._find_matching_extension(file.get("name"))

        if filetype:
            template_string = self.TEMPLATE_STRINGS[filetype]
        else:
            return f"<!-- Template string not found for file type [{file['name']}] -->"

        return template_string.format(
            cdn_url=self.CDN_URL,
            repo=file.get("repo"),
            package=file.get("package"),
            version=file.get("version"),
            name=file.get("name"),
            hash=file.get("hash"),
        )

    def get(self, package, alias):
        """
        Gets the HTML tag for a file in a package.

        Args:
            package: The name of the package.
            alias: The alias of the file.

        Returns:
            The HTML tag for the file.
        """
        html = self._get_string(package, alias)
        if self.app_name == "Flask":
            return Markup(html)
        return html
