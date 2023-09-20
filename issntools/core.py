#!/usr/bin/env python
# coding: utf-8

import requests
from typing import Optional, Dict, Union

def validate_issn(issn: str) -> bool:
    """Check if the number provided is a valid ISSN."""
    
    # Compact the ISSN to remove any separators and whitespace
    number = ''.join(issn.split('-')).strip().upper()

    # Ensure the ISSN has the correct length
    if len(number) != 8:
        print("Invalid ISSN length.")
        return False

    # Ensure the first 7 characters are digits
    if not number[:-1].isdigit():
        print("Invalid format. First 7 characters should be digits.")
        return False

    # Calculate the check digit
    try:
        check = (11 - sum((8 - i) * int(n) for i, n in enumerate(number[:-1]))) % 11
        check_digit = 'X' if check == 10 else str(check)
    except ValueError:
        print("Error calculating the check digit.")
        return False

    # Compare the calculated check digit with the last digit of the ISSN
    if check_digit != number[-1]:
        print(f"Invalid check digit. Expected {check_digit} but found {number[-1]}.")
        return False

    return True


BASE_ISSN_URL = "https://portal.issn.org/resource/ISSN/{}?format=json"

def get_issn_json(issn: str) -> Optional[Dict[str, Union[str, Dict]]]:
    """
    Fetch data in JSON format for a given ISSN from the ISSN portal.

    Parameters:
        - issn: The ISSN number.

    Returns:
        - A dictionary with the JSON data if the request is successful, or None otherwise.
    """

    if not validate_issn(issn):
        print("Invalid ISSN provided.")
        return None
    
    url = BASE_ISSN_URL.format(issn)

    try:
        response = requests.get(url, timeout=30)  # Set a timeout for the request

        # Check if the response is successful and if it's of JSON type
        if response.status_code == 200 and response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        else:
            print(f"Failed to retrieve ISSN data. Status code: {response.status_code}, Content type: {response.headers.get('content-type')}")
            return None

    except requests.Timeout:
        print(f"Request timed out for ISSN: {issn}")
    except requests.RequestException as e:
        print(f"Error fetching data for ISSN {issn}: {repr(e)}")

    return None


def search_data(data, attribute, keyword=None):
    try:
        for item in data['@graph']:
            if attribute in item and (not keyword or keyword in item.get('@id', '')):
                return item[attribute]
        return None
    except Exception as e:
        print(f"Error searching data: {repr(e)}")
        return None

def get_issn_title(data):
    try:
        return search_data(data, 'value', 'KeyTitle') or search_data(data, 'mainTitle')
    except Exception as e:
        print(f"Error getting journal title: {repr(e)}")
        return None

def get_issn_country(data):
    try:
        return search_data(data, 'label', 'countries')
    except Exception as e:
        print(f"Error getting journal country: {repr(e)}")
        return None

def get_issn_url(data):
    try:
        return search_data(data, 'url')
    except Exception as e:
        print(f"Error getting journal URL: {repr(e)}")
        return None
