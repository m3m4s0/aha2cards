# aha2cards
This project is still a work in progress

This tool helps you to export your [aha.io](https://aha.io) Features or Ideas in a printable card format to use in on hands planning sessions.

Hopefully this function will be available within aha.io soon [Feature Request](https://big.ideas.aha.io/ideas/APP-I-2651)

### How to use
Generate cards directly from aha! API : `python cards -api`

Generate cards from a given .csv file : `python cards -f`

## Query with API
To query the AHA.IO API you need to create a config.ini file that looks like this

[AHA.IO]

COMPANY = your_company_name

API_KEY = your_api_key

PRODUCT = aha_product_name

STATUS_TO_IGNORE = your custom status you don't need


## Next steps
* include export files
* generate pdf cards