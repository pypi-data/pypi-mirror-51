# tap-reviewscouk

A singer.io tap for extracting data from api.impactradius.com API, written in python 3.

Author: Hugh Nimmo-Smith (hugh@onedox.com)

## Limitations

Current limitations include:

- Only supports: Clicks, Actions, Invoices
- No error handling

## Configuration

`account_sid`, `auth_token`, `start_date` and `validation_window` config keys are required:

```json
{
  "account_sid": "12345",
  "auth_token": "IRxxxxxxx",
  "start_date": "2015-01-01",
  "validation_window": 180
}
```
