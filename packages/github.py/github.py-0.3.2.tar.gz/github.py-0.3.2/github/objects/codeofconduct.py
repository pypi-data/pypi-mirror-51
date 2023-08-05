"""
/github/objects/codeofconduct.py

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


class CodeOfConduct(Node, Type):
    """
    Represents a Code of Conduct.

    https://developer.github.com/v4/object/codeofconduct
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
            codes_of_conduct = list()

            for (code_of_conduct) in data:
                codes_of_conduct.append(cls(code_of_conduct))

            return codes_of_conduct

    @property
    def body(self) -> str:
        """
        The body of this Code of Conduct.
        """

        return self.data["body"]

    @property
    def key(self) -> str:
        """
        The key for this Code of Conduct.
        """

        return self.data["key"]

    @property
    def name(self) -> str:
        """
        The name of this Code of Conduct.
        """

        return self.data["name"]

    @property
    def url(self) -> str:
        """
        The url for this Code of Conduct.
        """

        return self.data["url"]
