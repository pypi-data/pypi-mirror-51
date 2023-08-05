# Copyright 2019 Juan Antonio Sauceda <jasgordo@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""Msa class, Member Services Area object."""

import http.client
from collections import OrderedDict

from bs4 import BeautifulSoup as BS

from .formatifier import Formatify

__license__ = 'GNU General Public License v2.0'


class Msa(object):
    """The Member Services Area class.

    The MSA calls is a very simple way to query the USCF Member Services Area
    api. It's designed to be very lite and bare minimual.

    Args:
        uscf_id (str): A USCF member id.

    Attributes:
        retrieve (func): Initial fetch of member information.

    """

    URL = 'www.uschess.org'
    API = '/msa/thin3.php?'

    def __init__(self, uscf_id):
        self.uscf_id = uscf_id
        self.retrieve(self.URL, self.API, self.uscf_id)

    @staticmethod
    def _get_data(url, api, uscf_id):
        """HTML to Beautiful object parser.

        Args:
            url (str): The url to uschess.org.
            api (str): The MSA api.
            uscf_id (str): A USCF member id.

        Returns:
            A Beautiful Soup parsed object.
        """

        conn = http.client.HTTPConnection(host=url, port=80)
        conn.request('GET', '/msa/thin3.php?' + uscf_id)
        res = conn.getresponse()
        soup = BS(res, 'html.parser')
        return soup

    def _get_profile_item(self, key):
        """Fetch profile item based on attribute.

        Args:
            key (str): A string of a key in a dict

        Returns:
            A str.
        """

        for k, v in self.profile[0].items():
            if key in k:
                return v

    def retrieve(self, url, api, uscf_id):
        """The USCF profile fetcher.

        Once the profile is fetched, it will update the profiles dict.
        Note: The function can also be used to update in real time.

        Args:
            url (str): The url to uschess.org.
            api (str): The MSA api.
            uscf_id (str): A USCF member id.
        """

        data = self._get_data(url=url, api=api, uscf_id=self.uscf_id)
        inputs = data.findAll('input', attrs={'value': True})

        value = []
        for item in inputs:
            value.append(item['value'])

        self.profile = [OrderedDict({
            'uscf_id': value[0],
            'expires': value[1],
            'name': value[2],
            'reg_rating': value[3],
            'quick_rating': value[4],
            'blitz_rating': value[5],
            'state_country': value[6],
            'fide_id': value[7],
            'fide_rating': value[8]
        })]

    def get_profile(self):
        """Gathers the necessary values and fields of the profile.

        Once the values and fields are orgainized, it will return
        a Formatifier object that will allow different styles of
        views of the project.

        Returns:
            A Formatify object.

        Example:
            The following example calls the method 'to_json()' from
            the Formatify class.

            >>> import json
            >>> from pyuscf import Msa
            >>> profile = Msa('12743305')
            >>> data = json.loads(profile.get_profile().to_json()
            >>> print(json.dumps(data), indent=1))
            [
             {
              "uscf_id": "12743305",
              "expires": "2099-12-31",
              "name": "FABIANO CARUANA",
              "reg_rating": "2895* 2019-08-01",
              "quick_rating": "2602* 2019-08-01",
              "blitz_rating": "2816* 2019-08-01",
              "state_country": "NV",
              "fide_id": "2020009 G USA",
              "fide_rating": "2818 2019-08-01"
             }
            ]
        """

        return Formatify(iterable=self.profile)

    def get_uscf_id(self):
        """The USCF id method.

        An 8 digit number represent the USCF id.

        Returns:
            A str.
        """

        return self._get_profile_item('uscf_id')

    def get_expires_date(self):
        """The expires date method.

        The form (YYYY-MM-DD) represent the expiration date.

        Returns:
            A str.
        """

        return self._get_profile_item('expires')

    def get_name(self):
        """The name method.

        The name, at a minimum, has first and last name.

        Returns:
            A str.
        """

        return self._get_profile_item('name')

    def get_regular_rating(self):
        """The USCF id method.

        A regular rating in the format of the following:
        (4 digit number) (YYYY-MM-DD)
        The date represent the current tracked rating.

        Returns:
            A str.
        """

        return self._get_profile_item('reg_rating')

    def get_quick_rating(self):
        """The quick rating method.

        A quick rating in the format of the following:
        (4 digit number) (YYYY-MM-DD)
        The date represent the current tracked rating.

        Returns:
            A str.
        """
        return self._get_profile_item('quick_rating')

    def get_blitz_rating(self):
        """The blitz rating method.

        A quick blitz in the format of the following:
        (4 digit number) (YYYY-MM-DD)
        The date represent the current tracked rating.

        Returns:
            A str.
        """

        return self._get_profile_item('blitz_rating')

    def get_state_country(self):
        """The state country method.

        A State in the abbreviated form.

        Returns:
            A str.
        """
        return self._get_profile_item('state_country')

    def get_fide_id(self):
        """The FIDE id method.

        A format of id and country.

        Returns:
            A str.
        """

        return self._get_profile_item('fide_id')

    def get_fide_rating(self):
        """The FIDE rating method.

        A FIDE rating in the format of the following:
        (4 digit number) (YYYY-MM-DD)
        The date represent the current tracked rating.

        Returns:
            A str.
        """

        return self._get_profile_item('fide_rating')
