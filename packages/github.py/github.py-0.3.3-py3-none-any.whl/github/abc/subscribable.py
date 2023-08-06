"""
/github/abc/subscribable.py

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

from github.enums import RepositorySubscription as SubscriptionState


class Subscribable():
    """
    Represents an object which can be subscribed to.
    """

    __slots__ = ()

    @property
    def viewer_can_subscribe(self) -> bool:
        """
        Whether or not the authenticated user can subscribe to the subscribable.
        """

        return self.data["viewerCanSubscribe"]

    @property
    def viewer_subscription(self) -> SubscriptionState:
        """
        The authenticated user's subscription state to the subscribable.
        """

        subscription = self.data["viewerSubscription"]
        return SubscriptionState.from_data(subscription)

    async def ignore(self):
        """
        |coro|

        Updates the authenticated user's subscription state to "IGNORED".
        """

        await self.http.update_subscription(self.id, "IGNORED")
        
    async def subscribe(self):
        """
        |coro|

        Updates the authenticated user's subscription state to "SUBSCRIBED".
        """

        await self.http.update_subscription(self.id, "SUBSCRIBED")

    async def unsubscribe(self):
        """
        |coro|

        Updates the authenticated user's subscription state to "UNSUBSCRIBED".
        """

        await self.http.update_subscription(self.id, "UNSUBSCRIBED")
