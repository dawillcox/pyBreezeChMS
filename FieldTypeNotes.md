"address",

"address_primary",
Example:
        "429856488": [
          {
            "field_type": "address_primary",
            "street_address": "1845 N 22nd St<br />PO Box 976",
            "city": "Decatur",
            "state": "IL",
            "zip": "62525",
            "longitude": "-88.927474",
            "latitude": "39.861568",
            "is_primary": "1",
            "is_private": "0"
          }
        ],
Notice, the data structure obviously would support multiple
addresses in the field, but apparently that isn't supported.
The only field_type I see in the data says address_primary
and has is_primary set.

"birthdate",
You'll see:
        "756872714": "1994-02-03",
        "birthdate": "1994-02-03",
Where the first is the id from the profile.

"checkbox",
        "2114298810": [
          {
            "name": "Campus Ministry",
            "value": "135"
          },
          {
            "name": "Worship",
            "value": "145"
          }
        ],
where the field with the given key is the checkbox.uu

"date",
        "2114298806": "02/12/2014",


"dropdown",
        "2114298858": {
          "value": "158",
          "name": "Transfer"
        },
Where value is (presumably) the tag for the value, and
name is the selected value.

"email",

"email_primary"
        "485792520": [
          {
            "address": "",
            "is_primary": "1",
            "allow_bulk": "1",
            "is_private": "0",
            "field_type": "email_primary"
          }
        ],
As with address, the profile field is "email," but the one
and only entry is flagged as email_primary.

"family",
      "family": [
        {
          "id": "7989991",
          "oid": "60347",
          "person_id": "14341993",
          "family_id": "2844047",
          "family_role_id": "5",
          "created_on": "2018-12-16 15:50:30",
          "role_name": "Spouse",
          "role_id": "5",
          "order": "2",
          "details": {
            "id": "14341993",
            "first_name": "Patricia",
            "force_first_name": "Patricia",
            "last_name": "Abruzzi",
            "thumb_path": "",
            "path": "img/profiles/generic/gray.png"
          }
        },
        {
          "id": "7989992",
          "oid": "60347",
          "person_id": "14341992",
          "family_id": "2844047",
          "family_role_id": "5",
          "created_on": "2018-12-16 15:50:30",
          "role_name": "Spouse",
          "role_id": "5",
          "order": "2",
          "details": {
            "id": "14341992",
            "first_name": "Phil",
            "force_first_name": "Phil",
            "last_name": "Abruzzi",
            "thumb_path": "",
            "path": "img/profiles/generic/gray.png"
          }
        }
      ]


Family is a weird case. It doesn't appear in the profile,
it just appears in details as "name".
"grade",

"multiple_choice",
        "2114298804": {
          "value": "73",
          "name": "She/Her/Hers/Herself"
        },
Actually, you can only have one value

"name",
Doesn't seem to appear as a profile field, only in the family section.


"notes",
        "2114298868": "Student (Former?)",
        "notes": "Student (Former?)",


"paragraph",
Looks like just a section header,

"phone",
        "605365827": [
          {
            "field_type": "phone",
            "phone_number": "(773) 964-3742",
            "phone_type": "mobile",
            "do_not_text": "0",
            "is_private": "0",
            "people_meta_id": "329930440"
          }
        ],
Or
        "605365827": [
          {
            "field_type": "phone",
            "phone_number": "(248) 266-6170",
            "phone_type": "home",
            "do_not_text": "0",
            "is_private": "0",
            "people_meta_id": "262833265"
          },
          {
            "field_type": "phone",
            "phone_number": "",
            "phone_type": null,
            "do_not_text": null,
            "is_private": null,
            "people_meta_id": "262833269"
          },
          {
            "field_type": "phone",
            "phone_number": "",
            "phone_type": null,
            "do_not_text": null,
            "is_private": null,
            "people_meta_id": "262833270"
          }
        ],


"single_line",

Note: Name isn't a profile field 