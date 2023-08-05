# tap-impactradius

A singer.io tap for extracting data from api.impactradius.com API, written in python 3.

Author: Hugh Nimmo-Smith (hugh@onedox.com)

## Limitations

Current limitations include:

- Only supports merchant reviews (no product reviews)
- No error handling

## Configuration

An `impactradius.account_sid` and `impactradius.auth_token` config keys are required:

```json
{
  "account_sid": "abcdefgh1234567890",
  "auth_token": "abcdefgh1234567890",
  "start_date": "2015-01-01T00:00:00.000Z"
}
```
