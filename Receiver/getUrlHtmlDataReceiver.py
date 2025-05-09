def convert_price_to_decimal(price_string):
    """
    Convert a price string (like '$19.99') to a decimal number.

    Args:
        price_string (str): The price string to convert

    Returns:
        float: The price as a decimal number
    """
    # Remove currency symbols, spaces, and any other non-numeric characters except for the decimal point
    cleaned_string = ''.join(char for char in price_string if char.isdigit() or char == '.')

    # Convert to float
    try:
        return float(cleaned_string)
    except ValueError:
        # Handle cases where there might be multiple decimal points after cleaning
        print(f"Error converting '{price_string}' to decimal")
        return None


# Examples
if __name__ == "__main__":
    test_prices = [
        "$19.99",
        "€24.50",
        "£10",
        "19.99 USD",
        "Rs. 1,499.00",
        "$1,234.56",
        "19.99",
        "Free",  # This will cause an error that's caught
    ]

    for price in test_prices:
        result = convert_price_to_decimal(price)
        print(f"Original: '{price}'")
        print(f"Decimal: {result}")
        print()
