from breeze_chms_api import breeze
import json

david_id = 13541283

test_person_id = '46554694'
api = breeze.breeze_api()
# ppl = api.get_people()
test_event_id = '331329324'  # '4001035' #'4001125'
test_calendar_id = '87273'
payment_group_id = '240957245'  # '3475247702'
payment_date = '2019-09-04'
payment_fund = '2020 Budget'
payment_batch_number = 671
payment_id = 435527682   # The one we created for testing



def add_person():
    init_fields = [
        {
            'field_id': "429856488",
            'field_type': 'address',
            'response': True,
            'details': {
                'street_address': '123 Test St',
                'city': 'Grand Rapids',
                'state': 'MI',
                'zip': '49506',
            }
        },
        {
            'field_id': '2114298903',
            'field_type': 'radio',
            'response': '201',  # "None"
        },
        {
            'field_id': '2114298948',
            'field_type': 'radio',
            'response': '213',  # Unlisted
        },
    ]
    result = api.add_person(first='OnlyFor', last='Testing', fields_json=init_fields)
    print(result)
    print(result.get('id'))


# add_person()

# det = api.get_person_details(test_person_id)
# print('\nget_person_details:')
# print(json.dumps(det, indent=2))

newfields = [
    {
        'field_id': '2114298826',
        'field_type': 'notes',
        'response': 'This profile only for testing'
    },
    {
        'field_id': '605365827',
        'field_type': 'phone',
        'response': 'true',
        'details': {'is_private': '0', 'phone_home': '800-555-1212'},
    },
    {
        'field_id': '485792520',
        'field_type': 'email',
        'response': 'true',
        'details': {'address': 'nobody@there.us'}
    },
    {
        'field_id': '756872714',
        'field_type': 'birthdate',
        'response': '1/1/2014'
    },
    {
        'field_id': '2114298948',
        'field_type': 'radio',
        'response': '213',  # Unlisted
    },
]


# newfields_str = json.dumps(newfields)
# print('\nSent in update:---------------------')
# print(json.dumps(newfields, indent=2))
def update_person():
    result = api.update_person(person_id=test_person_id, fields_json=newfields)
    print('\nReturned by update:---------------------')
    print(json.dumps(result, indent=2))


# update_person()

# for p in ppl:
#     if p['first_name'] == 'David' and p['last_name'] == 'Willcox':
#         print(p)
#         break

# details = api.get_person_details(david_id)
# profile_fields = api.get_profile_fields()
# with open('profiles.json', 'w') as f:
#     json.dump(profile_fields, f, indent=2)
# with open('profile_fields.json', 'r') as f:
#     profile_fields = json.load(f)
#
# # print(profile_fields)
# details = profile_fields['details']

# print(details)


def add_event():
    starts_on = 1690927200  # This clearly isn't right Could we use string form?
    ends_on = starts_on + 90 * 60
    args = {
        'name': "Special event for testing",
        'starts_on': starts_on,
        'ends_on': ends_on,
        'description': "I'm using this to test the Breeze API",
        'category_id': test_calendar_id,
        # 'event_id': Previous event to make this part of a series,
    }
    reply = api.add_event(**args)
    print(json.dumps(reply, indent=2))
    print(reply.get('event_id'))


def add_contribution():
    funds_json = [
        {
            'name': payment_fund,
            'amount': 30
        },
        {
            'name': 'Help Processing Fee',
            'amount': 20
        }
    ]
    pmnt_id = api.add_contribution(date=payment_date,
                                   name='OnlyFor Testing',
                                   person_id=test_person_id,
                                   method='Cash',
                                   funds_json=funds_json,
                                   amount=50,
                                   # group=payment_group_id,
                                   # payment_id=payment_group_id,
                                   batch_name="Ignore, For Testing Only (Modified)",
                                   note='Test Payment',
                                   batch_number=payment_batch_number,
                                   # batch=payment_batch_number,
                                   )
    print(pmnt_id)
    return pmnt_id


def edit_contribution():
    funds_json = [
        {
            'name': payment_fund,
            'amount': 22.43
        },
        {
            'name': 'Help Processing Fee',
            'amount': 5.00
        }
    ]
    pmnt_id = api.edit_contribution(date=payment_date,
                                    name='OnlyFor Testing (Edited)',
                                    person_id=test_person_id,
                                    method='Check',
                                    funds_json=funds_json,
                                    amount=27.43,
                                    # group=payment_group_id,
                                    payment_id=payment_id,
                                    # batch_name="Ignore, For Testing Only (Modified)",
                                    note='Test Payment (Yet another modification)',
                                    batch_number='673',
                                    # batch='672',
                                    )
    return pmnt_id


def list_payments():
    r = api.list_contributions(
        # batches=payment_batch_number,
        # start=payment_date,
        # end=payment_date,
        person_id=test_person_id,
    )
    print(json.dumps(r, indent=2))
    return None

def list_pledges():
    pledges = api.list_pledges("353956")
    # print(json.dumps(pledges, indent=2))
    with open('pledges.csv', 'w') as f:
        for p in pledges:
            nm = f'{p["last_name"]}, {p["first_name"]}'
            note = f'{p["note"]}'
            ln = f'"{nm}", "{note}"'
            print(ln, file=f)

def list_campaigns():
    c = api.list_campaigns()
    print(json.dumps(c, indent=2))

def delete_payment():
    return api.delete_contribution(payment_id=435527682)


# result = api.list_events(start='2023-08-01', end='2023-08-02')
# result = api.event_check_in(person_id=test_person_id, instance_id=test_event_id)
# result = api.event_check_out(person_id=test_person_id, instance_id=test_event_id)
# result = api.list_attendance(instance_id=test_event_id, details=True)
# result = api.delete_attendance(person_id=test_person_id, instance_id=test_event_id)
# result = api.list_eligible_people(instance_id=test_event_id)

# print(result)
# add_event()
# cals = api.list_calendars()
# print(json.dumps(cals, indent=2))
# result = add_contribution()

# result = edit_contribution()
# result = list_payments()
# result = delete_payment()
result = list_pledges()
print(result)
