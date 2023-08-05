"""
/github/objects/license.py

    Copyright (c) 2019 ShineyDev
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import typing

from github.abc import Node
from github.abc import Type
from .licenserule import LicenseRule


class License(Node, Type):
    """
    A repository's source license.

    https://developer.github.com/v4/object/license/
    """

    __slots__ = ("data",)

    def __init__(self, data):
        self.data = data

    def __repr__(self) -> str:
        return "<{0.__class__.__name__} key='{0.key}'>".format(self)

    @classmethod
    def from_data(cls, data):
        if isinstance(data, dict):
            return cls(data)
        elif isinstance(data, list):
            licenses = list()

            for (license) in data:
                licenses.append(cls(license))

            return licenses

    @property
    def body(self) -> str:
        """
        The full text of the license.
        """

        return self.data["body"]

    @property
    def conditions(self) -> typing.List[LicenseRule]:
        """
        The conditions set by the license.
        """

        conditions = self.data["conditions"]
        return LicenseRule.from_data(conditions)

    @property
    def description(self) -> str:
        """
        A human-readable description of the license.
        """

        return self.data["description"]

    @property
    def implementation(self) -> str:
        """
        Instructions on how to implement the license.
        """

        return self.data["implementation"]

    @property
    def is_featured(self) -> bool:
        """
        Whether the license is featured.
        """

        return self.data["featured"]

    @property
    def is_hidden(self) -> bool:
        """
        Whether the license is not displayed in license pickers.
        """

        return self.data["hidden"]

    @property
    def is_pseudo(self) -> bool:
        """
        Whether the license is a pseudo-license placeholder.
        """

        return self.data["pseudoLicense"]

    @property
    def key(self) -> str:
        """
        The lowercased SPDX ID of the license.
        """

        return self.data["key"]

    @property
    def limitations(self) -> typing.List[LicenseRule]:
        """
        The limitations set by the license.
        """

        limitations = self.data["limitations"]
        return LicenseRule.from_data(limitations)

    @property
    def name(self) -> str:
        """
        The license' full name specified by https://spdx.org/licenses.
        """

        return self.data["name"]

    @property
    def nickname(self) -> typing.Optional[str]:
        """
        The license' customary short name.
        """

        return self.data["nickname"]

    @property
    def permissions(self) -> typing.List[LicenseRule]:
        """
        The permissions set by the license.
        """

        permissions = self.data["permissions"]
        return LicenseRule.from_data(permissions)

    @property
    def spdx_id(self) -> str:
        """
        The license' short identifier specified by https://spdx.org/licenses.
        """

        return self.data["spdxId"]

    @property
    def url(self) -> str:
        """
        The url to the license on https://choosealicense.com.
        """

        return self.data["url"]
