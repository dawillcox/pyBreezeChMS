"""Python wrapper for Breeze ChMS API: http://www.breezechms.com/api

This API wrapper allows churches to build custom functionality integrated with
Breeze Church Management System.

Usage:
  from breeze import breeze

  breeze_api = breeze.BreezeApi(
      breeze_url='https://demo.breezechms.com',
      api_key='5c2d2cbacg3...')
  people = breeze_api.get_people();

  for person in people:
    print '%s %s' % (person['first_name'], person['last_name'])
"""

__author__ = 'alexortizrosado@gmail.com (Alex Ortiz-Rosado)'

import logging
import requests
from enum import Enum
from typing import Union, List


class ENDPOINTS(Enum):
    PEOPLE = 'people'
    EVENTS = 'events'
    PROFILE_FIELDS = 'profile'
    CONTRIBUTIONS = 'giving'
    FUNDS = 'funds'
    PLEDGES = 'pledges'
    TAGS = 'tags'
    ACCOUNT_SUMMARY = 'account/summary'
    FORMS = 'forms'


class BreezeError(Exception):
    """Exception for BreezeApi."""
    pass


class BreezeApi(object):
    """A wrapper for the Breeze REST API."""

    def __init__(self, breeze_url, api_key,
                 dry_run=False,
                 connection=requests.Session()):
        """Instantiates the BreezeApi with your Breeze account information.

        Args:
          breeze_url: Fully qualified domain for your organizations Breeze
                      service.
          api_key: Unique Breeze API key. For instructions on finding your
                   organizations API key, see:
                   http://breezechms.com/docs#extensions_api
          dry_run: Enable no-op mode, which disables requests from being made.
                   When combined with debug, this allows debugging requests
                   without affecting data in your Breeze account."""

        self.breeze_url = breeze_url
        self.api_key = api_key
        self.dry_run = dry_run
        self.connection = connection

        # TODO(alex): use urlparse to check url format.
        if not (self.breeze_url and self.breeze_url.startswith('https://') and
                self.breeze_url.find('.breezechms.')):
            raise BreezeError('You must provide your breeze_url as ',
                              'subdomain.breezechms.com')

        if not self.api_key:
            raise BreezeError('You must provide an API key.')

    def _request(self,
                 endpoint: ENDPOINTS,
                 args: List[str] = [],
                 command: str = '',
                 params=None,
                 headers=None,
                 timeout=60):
        """Makes an HTTP request to a given url.

        Args:
          endpoint: URL where the service can be accessed.
          params: Query parameters to append to endpoint url.
          headers: HTTP headers; used for authenication parameters.
          timeout: Timeout in seconds for HTTP request.

        Returns:
          HTTP response

        Throws:
          BreezeError if connection or request fails."""
        if headers is None:
            headers = {}
        headers.update({
          'Content-Type': 'application/json',
          'Api-Key': self.api_key}
          )

        if params is None:
            params = {}
        keywords = dict(params=params, headers=headers, timeout=timeout)
        url = f"{self.breeze_url}/api/{endpoint.value}/{command}?{'&'.join(args)}"

        logging.debug('Making request to %s', url)
        if self.dry_run:
            return      # NOT TESTED

        response = self.connection.get(url, verify=True, **keywords)
        try:
            response = response.json()
        except requests.ConnectionError as error:
            raise BreezeError(error)
        else:
            if not self._request_succeeded(response):
                raise BreezeError(response)
            logging.debug('JSON Response: %s', response)
            return response

    def _request_succeeded(self, response) -> bool:
        """Predicate to ensure that the HTTP request succeeded."""
        if isinstance(response, bool):
            return response
        else:
            return not (('errors' in response) or ('errorCode' in response))

    def get_account_summary(self):
        """Retrieve the details for a specific account using the API key 
          and URL. It can also work to see if the key and URL are valid.

        Returns:
          JSON response. For example:
          {
            "id":"1234",
            "name":"Grace Church",
            "subdomain":"gracechurchdemo",
            "status":"1",
            "created_on":"2018-09-10 09:19:35",
            "details":{
                "timezone":"America\/New_York",
                "country":{
                    "id":"2",
                    "name":"United States of America",
                    "abbreviation":"USA",
                    "abbreviation_2":"US",
                    "currency":"USD",
                    "currency_symbol":"$",
                    "date_format":"MDY",
                    "sms_prefix":"1"
                }
            }
          }
          """
        return self._request(ENDPOINTS.ACCOUNT_SUMMARY) # NOT TESTED

    def get_people(self, limit=None, offset=None, details=False):
        """List people from your database.

        Args:
          limit: Number of people to return. If None, will return all people.
          offset: Number of people to skip before beginning to return results.
                  Can be used in conjunction with limit for pagination.
          details: Option to return all information (slower) or just names.

        returns:
          JSON response. For example:
          {
            "id":"157857",
            "first_name":"Thomas",
            "last_name":"Anderson",
            "path":"img\/profiles\/generic\/blue.jpg"
          },
          {
            "id":"157859",
            "first_name":"Kate",
            "last_name":"Austen",
            "path":"img\/profiles\/upload\/2498d7f78s.jpg"
          },
          {
            ...
          }"""

        params = []
        if limit:
            params.append('limit=%s' % limit)
        if offset:
            params.append('offset=%s' % offset)
        if details:
            params.append('details=1')
        return self._request(ENDPOINTS.PEOPLE, args=params)
        # return self._request('%s/?%s' % (ENDPOINTS.PEOPLE, '&'.join(params)))

    def get_profile_fields(self):
        """List profile fields from your database.

        Returns:
          JSON response."""
        return self._request(ENDPOINTS.PROFILE_FIELDS)

    def get_person_details(self, person_id):
        """Retrieve the details for a specific person by their ID.

        Args:
          person_id: Unique id for a person in Breeze database.

        Returns:
          JSON response."""
        return self._request(ENDPOINTS.PEOPLE, command=str(person_id))
        # return self._request('%s/%s' % (ENDPOINTS.PEOPLE, str(person_id)))

    def add_person(self, first_name, last_name, fields_json=None):
        """Adds a new person into the database.

        Args:
          first_name: The first name of the person.
          last_name: The first name of the person.
          fields_json: JSON string representing an array of fields to update.
                       Each array element must contain field id, field type, response,
                       and in some cases, more information.
                       ie. [ {
                               "field_id":"929778337",
                               "field_type":"email",
                               "response":"true",
                               "details":{
                                    "address": "tony@starkindustries.com",
                                    "is_private":1}
                             }
                           ].
                       Obtain such field information from get_profile_fields() or
                       use get_person_details() to see fields that already exist for a specific person.

        Returns:
          JSON response equivalent to get_person_details()."""

        params = []
        params.append(f'first={first_name}')
        params.append(f'last={last_name}')
        if fields_json:
            params.append(f'fields_json={fields_json}')  # NOT TESTSED

        return self._request(ENDPOINTS.PEOPLE, command='add', args=params)

        # return self._request('%s/add?%s' % (ENDPOINTS.PEOPLE, '&'.join(params)))

    def update_person(self, person_id, fields_json=[]):
        """Updates the details for a specific person in the database.

        Args:
          person_id: Unique id for a person in Breeze database.
          fields_json: JSON string representing an array of fields to update.
                       Each array element must contain field id, field type, response,
                       and in some cases, more information.
                       ie. [ {
                               "field_id":"929778337",
                               "field_type":"email",
                               "response":"true",
                               "details":{
                                    "address": "tony@starkindustries.com",
                                    "is_private":1}
                             }
                           ].
                       Obtain such field information from get_profile_fields() or
                       use get_person_details() to see fields that already exist for a specific person.


        Returns:
          JSON response equivalent to get_person_details(person_id)."""
        params = [f'person_id={person_id}', f'fields_json={fields_json}']
        return self._request(ENDPOINTS.PEOPLE, command='update', args=params)

        # return self._request(
        #     '%s/update?person_id=%s&fields_json=%s' % (
        #         ENDPOINTS.PEOPLE.value, person_id, fields_json
        #     ))

    def get_events(self, start_date=None, end_date=None):
        """Retrieve all events for a given date range.

        Args:
          start_date: Start date; defaults to first day of the current month.
          end_date: End date; defaults to last day of the current month

        Returns:
          JSON response."""
        args = []
        if start_date:
            args.append(f'start={start_date}')
        if end_date:
            args.append(f'end={end_date}')
        return self._request(ENDPOINTS.EVENTS, args=args)
        # return self._request('%s/?%s' % (ENDPOINTS.EVENTS, '&'.join(params)))

    def add_event(self,
                  name,
                  start_date,
                  end_date=None,
                  all_day=None,
                  description=None,
                  category_id=None,
                  event_id=None):
        """Add event for a given date range.

        Args:
          name: Name of event
          start_date: Start datetimestamp (epoch time)
          end_date: End datetimestamp (epoch time)
          all_day: boolean
          description: description of event (default none)
          category id: which calendar your event is on (defaults to primary)
          event id: series id

        Returns:
          JSON response."""
          
        args = []
        if name:
            args.append(f'name={name}')
        if start_date:
            args.append(f'starts_on={start_date}')
        if end_date:
            args.append(f'ends_on={end_date}')
        if all_day is not None:
            args.append(f'all_day={1 if all_day else 0}')
        if description:
            args.append(f'description={description}')
        if category_id:
            args.append(f'category_id={category_id}')
        if event_id:
            args.append(f'event_id={event_id}')
        return self._request(ENDPOINTS.EVENTS, command='add', args=args)
        # return self._request('%s/add?%s' % (ENDPOINTS.EVENTS, '&'.join(params)))

    def event_check_in(self, person_id, event_instance_id):
        """Checks in a person into an event.

        Args:
          person_id: id for a person in Breeze database.
          event_instance_id: id for event instance to check into.."""
        args = [f'person_id={person_id}', f'instance_id={event_instance_id}']

        return self._request(ENDPOINTS.EVENTS, command='add', args=args)
        # return self._request(
        #     '%s/attendance/add?person_id=%s&instance_id=%s' % (
        #         ENDPOINTS.EVENTS, str(person_id), str(event_instance_id)
        #     ))

    def event_check_out(self, person_id, event_instance_id):
        """Remove the attendance for a person checked into an event.

        Args:
          person_id: Breeze ID for a person in Breeze database.
          event_instance_id: id for event instance to check out (delete).

        Returns:
          True if check-out succeeds; False if check-out fails."""

        args = [f'person_id={person_id}', f'instance_id={event_instance_id}']
        return self._request(ENDPOINTS.EVENTS, command='delete', args=args)
        # return self._request(
        #     '%s/attendance/delete?person_id=%s&instance_id=%s' % (
        #         ENDPOINTS.EVENTS, str(person_id), str(event_instance_id)
        #     ))

    def add_contribution(self, **kwargs):
                         # date=None,
                         # name=None,
                         # person_id=None,
                         # uid=None,
                         # processor=None,
                         # method=None,
                         # funds_json=None,
                         # amount=None,
                         # group=None,
                         # batch_number=None,
                         # batch_name=None):
        """Add a contribution to Breeze.

        Args:
          date: Date of transaction in DD-MM-YYYY format (ie. 24-5-2015)
          name: Name of person that made the transaction. Used to help match up
                contribution to correct profile within Breeze.  (ie. John Doe)
          person_id: The Breeze ID of the donor. If unknown, use UID instead of
                     person id  (ie. 1234567)
          uid: The unique id of the person sent from the giving platform. This
               should be used when the Breeze ID is unknown. Within Breeze a
               user will be able to associate this ID with a given Breeze ID.
               (ie. 9876543)
          email: Email address of donor. If no person_id is provided, used to
                 help automatically match the person to the correct profile.
                 (ie. sample@breezechms.com)
          street_address: Donor's street address. If person_id is not provided,
                          street_address will be used to help automatically
                          match the person to the correct profile.
                          (ie. 123 Sample St)
          processor: The name of the processor used to send the payment. Used
                     in conjunction with uid. Not needed if using Breeze ID.
                     (ie. SimpleGive, BluePay, Stripe)
          method: The payment method. (ie. Check, Cash, Credit/Debit Online,
                  Credit/Debit Offline, Donated Goods (FMV), Stocks (FMV),
                  Direct Deposit)
          funds_json: JSON string containing fund names and amounts. This
                      allows splitting fund giving. The ID is optional. If
                      present, it must match an existing fund ID and it will
                      override the fund name.
                      ie. [ {
                              'id':'12345',
                              'name':'General Fund',
                              'amount':'100.00'
                            },
                            {
                              'name':'Missions Fund',
                              'amount':'150.00'
                            }
                          ]
          amount: Total amount given. Must match sum of amount in funds_json.
          group: This will create a new batch and enter all contributions with
                 the same group into the new batch. Previous groups will be
                 remembered and so they should be unique for every new batch.
                 Use this if wanting to import into the next batch number in a
                 series.
          batch_number: The batch number to import contributions into. Use
                        group instead if you want to import into the next batch
                        number.
          batch_name: The name of the batch. Can be used with batch number or
                      group.

        Returns:
          Payment Id.

        Throws:
          BreezeError on failure to add contribution."""

        args = [f'{k}={v}' for k, v in kwargs.items()]
        # if date:
        #     params.append('date=%s' % date)
        # if name:
        #     params.append('name=%s' % name)
        # if person_id:
        #     params.append('person_id=%s' % person_id)
        # if uid:
        #     params.append('uid=%s' % uid)
        # if processor:
        #     params.append('processor=%s' % processor)
        # if method:
        #     params.append('method=%s' % method)
        # if funds_json:
        #     params.append('funds_json=%s' % funds_json)
        # if amount:
        #     params.append('amount=%s' % amount)
        # if group:
        #     params.append('group=%s' % group)
        # if batch_number:
        #     params.append('batch_number=%s' % batch_number)
        # if batch_name:
        #     params.append('batch_name=%s' % batch_name)
        response = self._request(ENDPOINTS.CONTRIBUTIONS, command='add', args=args)
        # response = self._request('%s/add?%s' % (ENDPOINTS.CONTRIBUTIONS,
        #                                         '&'.join(params)))
        return response['payment_id']

    def edit_contribution(self, **kwargs):
                          # payment_id=None,
                          # date=None,
                          # name=None,
                          # person_id=None,
                          # uid=None,
                          # processor=None,
                          # method=None,
                          # funds_json=None,
                          # amount=None,
                          # group=None,
                          # batch_number=None,
                          # batch_name=None):
        """Edit an existing contribution.

        Args:
          payment_id: The ID of the payment that should be modified.
          date: Date of transaction in DD-MM-YYYY format (ie. 24-5-2015)
          name: Name of person that made the transaction. Used to help match up
                contribution to correct profile within Breeze.  (ie. John Doe)
          person_id: The Breeze ID of the donor. If unknown, use UID instead of
                     person id  (ie. 1234567)
          uid: The unique id of the person sent from the giving platform. This
               should be used when the Breeze ID is unknown. Within Breeze a
               user will be able to associate this ID with a given Breeze ID.
               (ie. 9876543)
          email: Email address of donor. If no person_id is provided, used to
                 help automatically match the person to the correct profile.
                 (ie. sample@breezechms.com)
          street_address: Donor's street address. If person_id is not provided,
                          street_address will be used to help automatically
                          match the person to the correct profile.
                          (ie. 123 Sample St)
          processor: The name of the processor used to send the payment. Used
                     in conjunction with uid. Not needed if using Breeze ID.
                     (ie. SimpleGive, BluePay, Stripe)
          method: The payment method. (ie. Check, Cash, Credit/Debit Online,
                  Credit/Debit Offline, Donated Goods (FMV), Stocks (FMV),
                  Direct Deposit)
          funds_json: JSON string containing fund names and amounts. This
                      allows splitting fund giving. The ID is optional. If
                      present, it must match an existing fund ID and it will
                      override the fund name.
                      ie. [ {
                              'id':'12345',
                              'name':'General Fund',
                              'amount':'100.00'
                            },
                            {
                              'name':'Missions Fund',
                              'amount':'150.00'
                            }
                          ]
          amount: Total amount given. Must match sum of amount in funds_json.
          group: This will create a new batch and enter all contributions with
                 the same group into the new batch. Previous groups will be
                 remembered and so they should be unique for every new batch.
                 Use this if wanting to import into the next batch number in a
                 series.
          batch_number: The batch number to import contributions into. Use
                        group instead if you want to import into the next batch
                        number.
          batch_name: The name of the batch. Can be used with batch number or
                      group.

        Returns:
          Payment id.

        Throws:
          BreezeError on failure to edit contribution."""

        args = [f'{k}={v}' for k, v in kwargs.items()]

        # if payment_id:
        #     params.append('payment_id=%s' % payment_id)
        # if date:
        #     params.append('date=%s' % date)
        # if name:
        #     params.append('name=%s' % name)
        # if person_id:
        #     params.append('person_id=%s' % person_id)
        # if uid:
        #     params.append('uid=%s' % uid)
        # if processor:
        #     params.append('processor=%s' % processor)
        # if method:
        #     params.append('method=%s' % method)
        # if funds_json:
        #     params.append('funds_json=%s' % funds_json)
        # if amount:
        #     params.append('amount=%s' % amount)
        # if group:
        #     params.append('group=%s' % group)
        # if batch_number:
        #     params.append('batch_number=%s' % batch_number)
        # if batch_name:
        #     params.append('batch_name=%s' % batch_name)
        # response = self._request('%s/edit?%s' % (ENDPOINTS.CONTRIBUTIONS,
        #                                          '&'.join(params)))
        response = self._request(ENDPOINTS.CONTRIBUTIONS, command='edit', args=args)
        return response['payment_id']

    def delete_contribution(self, payment_id):
        """Delete an existing contribution.

        Args:
          payment_id: The ID of the payment that should be deleted.

        Returns:
          Payment id.

        Throws:
          BreezeError on failure to delete contribution."""

        response = self._request(ENDPOINTS.CONTRIBUTIONS, command="delete", args=[f'payment_id={payment_id}'])
        # response = self._request('%s/delete?payment_id=%s' % (
        #     ENDPOINTS.CONTRIBUTIONS, payment_id
        # ))
        return response['payment_id']

    def list_form_entries(self, form_id, details=False):
        """return entries for the given form

        Args:
          form_id:the ID of the form 
          details: Option to return all information (slower) or just names.

        returns:
          JSON response. For example:
          [
		{
			"id":"11",
			"form_id":"15326",
			"created_on":"2021-03-09 13:04:02",
			"person_id":null,
			"response":{
			    "45":{
				"id":"13",
				"oid":"1512",
				"first_name":"Zoe",
				"last_name":"Washburne",
				"created_on":"2021-03-09 13:04:03"
			    },
			    "46":"zwashburne@test.com",
			    "47":"Red"
			}
		    },
          ]"""

        args = [f'form_id={form_id}']
        if details:
            args.append('details=1')
        return self._request(ENDPOINTS.FORMS, command='list_form_entries', args=args)
        # return self._request('%s/list_form_entries?%s' % (ENDPOINTS.FORMS, '&'.join(params)))

    def list_contributions(self,
                           # start_date=None,
                           # end_date=None,
                           # person_id=None,
                           # include_family=False,
                           # amount_min=None,
                           # amount_max=None,
                           # method_ids=None,
                           # fund_ids=None,
                           # envelope_number=None,
                           # batches=None,
                           # forms=None,
                           **kwargs):
        """Retrieve a list of contributions.

        Args:
          start_date: Find contributions given on or after a specific date
                      (ie. 2015-1-1); required.
          end_date: Find contributions given on or before a specific date
                    (ie. 2018-1-31); required.
          person_id: ID of person's contributions to fetch. (ie. 9023482)
          include_family: Include family members of person_id (must provide
                          person_id); default: False.
          amount_min: Contribution amounts equal or greater than.
          amount_max: Contribution amounts equal or less than.
          method_ids: List of method IDs.
          fund_ids: List of fund IDs.
          envelope_number: Envelope number.
          batches: List of Batch numbers.
          forms: List of form IDs.

        Returns:
          List of matching contributions.

        Throws:
          BreezeError on malformed request."""

        if kwargs.get('include_family') and not kwargs.get('person_id'):
            raise BreezeError('include_family requires a person_id.')

        args = []
        for k, v in kwargs.items():
            if isinstance(v, List):
                args.append(f"{k}={'-'.join([str(val) for val in v])}")
            elif isinstance(v, bool):
                if v:
                    args.append(f'{k}=1')
            else:
                args.append(f'{k}={v}')

        # if start_date:
        #     params.append('start=%s' % start_date)
        # if end_date:
        #     params.append('end=%s' % end_date)
        # if person_id:
        #     params.append('person_id=%s' % person_id)
        # if include_family:
        #     if not person_id:
        #         raise BreezeError('include_family requires a person_id.')
        #     params.append('include_family=1')
        # if amount_min:
        #     params.append('amount_min=%s' % amount_min)
        # if amount_max:
        #     params.append('amount_max=%s' % amount_max)
        # if method_ids:
        #     params.append('method_ids=%s' % '-'.join(method_ids))
        # if fund_ids:
        #     params.append('fund_ids=%s' % '-'.join(fund_ids))
        # if envelope_number:
        #     params.append('envelope_number=%s' % envelope_number)
        # if batches:
        #     params.append('batches=%s' % '-'.join(batches))
        # if forms:
        #     params.append('forms=%s' % '-'.join(forms))
        return self._request(ENDPOINTS.CONTRIBUTIONS, command='list', args=args)
        # return self._request('%s/list?%s' % (ENDPOINTS.CONTRIBUTIONS,
        #                                      # '&'.join(params)))

    def list_funds(self, include_totals=False):
        """List all funds.

        Args:
          include_totals: Amount given to the fund should be returned.

        Returns:
          JSON Reponse."""

        # params = []
        # if include_totals:
        #     params.append('include_totals=1')
        return self._request(ENDPOINTS.FUNDS,
                             command='list',
                             args=['include_totals=1'] if include_totals else None)
        # return self._request('%s/list?%s' %
        #                      (ENDPOINTS.FUNDS, '&'.join(params)))

    def list_campaigns(self):
        """List of campaigns.

        Returns:
          JSON response."""
        return self._request(ENDPOINTS.PLEDGES, command='list_campaigns')
        # return self._request('%s/list_campaigns' % (ENDPOINTS.PLEDGES))

    def list_pledges(self, campaign_id):
        """List of pledges within a campaign.

        Args:
          campaign_id: ID number of a campaign.

        Returns:
          JSON response."""

        return self._request(ENDPOINTS.PLEDGES, command="list_pledges", args=[f'campaign_id={campaign_id}'])
        # return self._request('%s/list_pledges?campaign_id=%s' % (
        #     ENDPOINTS.PLEDGES, campaign_id

    def get_tags(self, folder=None):
        """List of tags

        Args:
          folder: If set, only return tags in this folder id

        Returns:
          JSON response. For example:
            [
            {
                "id":"523928",
                "name":"4th & 5th",
                "created_on":"2018-09-10 09:19:40",
                "folder_id":"1539"
            },
            {
                "id":"51994",
                "name":"6th Grade",
                "created_on":"2018-02-06 06:40:40",
                "folder_id":"1539"
            },
            { ... }
            ]"""

        # params = []
        # if folder:
        #     params.append('folder_id=%s' % folder)
        return self._request(ENDPOINTS.TAGS,
                             command='list_tags',
                             args=[f'folder_id={folder}'] if folder else [])
        # return self._request('%s/%s/?%s' % (ENDPOINTS.TAGS.value, 'list_tags', '&'.join(params)))

    def get_tag_folders(self):
        """List of tag folders

        Args: (none)

        Returns:
          JSON response, for example:
             [
             {
                 "id":"1234567",
                 "parent_id":"0",
                 "name":"All Tags",
                 "created_on":"2018-06-05 18:12:34"
             },
             {
                 "id":"8234253",
                 "parent_id":"120425",
                 "name":"Kids",
                 "created_on":"2018-06-05 18:12:10"
             },
             {
                 "id":"1537253",
                 "parent_id":"5923042",
                 "name":"Small Groups",
                 "created_on":"2018-09-10 09:19:40"
             },
             {
                 "id":"20033",
                 "parent_id":"20031",
                 "name":"Student Ministries",
                 "created_on":"2018-12-15 18:11:31"
             }
             ]"""
        return self._request(ENDPOINTS.TAGS, command='list_folders')
        # return api._request("%s/%s" % (ENDPOINTS.TAGS.value, "list_folders"))

    def assign_tag(self, 
                   person_id,
                   tag_id):
        """
        Update a person's tag/s.
        
        params:
        
        person_id: an existing person's user id
        
        tag_id: the id number of the tag you want to assign to the user
        
        output: true or false upon success or failure of tag update
        """
        args = [f'person_id={person_id}', f'tag_id={tag_id}']
        # params.append(f'person_id={person_id}')
        # params.append(f'tag_id={tag_id}')
        response = self._request(ENDPOINTS.TAGS, command='assign', args=args)

        # response = self._request('%s/assign?%s' %
        #                      (ENDPOINTS.TAGS.value, '&'.join(params)))
        
        return response

    def unassign_tag(self, person_id, tag_id):
        """
        Delete a person's tag/s.
        
        params:
        
        person_id: an existing person's user id
        
        tag_id: the id number of the tag you want to assign to the user
        
        output: true or false upon success or failure of tag deletion
        """
        args = [f'person_id={person_id}', f'tag_id={tag_id}']

        response = self._request(ENDPOINTS.TAGS, command='unassign', args=args)
        # response = self._request('%s/unassign?%s' %
        #                      (ENDPOINTS.TAGS.value, '&'.join(params)))
        
        return response            

