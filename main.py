"""Discount test"""

LOYALTY_CARD = True
SPECIAL_OFFER = True
APPROVED = False

if LOYALTY_CARD or SPECIAL_OFFER:
    if APPROVED:
        print("true")
    else:
        print("false")
else:
    print("false")
