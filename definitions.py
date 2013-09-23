TERMS = ['Terms of use must be accepted']
EMAIL = ['Email address not entered',
         'Invalid email address format',
         'Email address does not exist',
         'Email address already exist in the database']

PASSWORD = [
    'Password not entered',
    'Non-alphanumeric password',
    'Invalid password entered',
    'Temporary password emailed'
]

TWITTER_NAME = [
    'Twitter name not entered',
]

DEPOSIT_AMOUNT = [
    'Deposit amount not entered',
    'Invalid deposit amount entered'
]

RETWEET_GOAL = [
    'Retweet goal not entered',
    'Invalid retweet goal entered'
]

PRICE_PER_TWEET = [
    'Price not entered',
    'Invalid price entered'
]

PASSWORD_REPEAT = ['Repeat password not entered',
                   'Non-alphanumeric repeat password entered',
                   'Entered passwords do not match',
                   'Password changed']

PASSWORD_OLD = ['Old password not entered',
                'Non-alphanumeric old password entered']

PASSWORD_NEW = ['New password not entered',
                'Non-alphanumeric new password entered']

STORE_NAME = ['Store name not entered',
              'Non-alphanumeric storename entered',
              'Restricted storename entered',
              'Storename taken',
              'Storename must be between 5 and 18 characters long']

BITCOIN_ADDRESS = ['Bitcoin address not entered',
                   'Invalid bitcoin address format']

FIRST = ['First name not entered',
         'Non-alphanumeric first name entered']

LAST = ['Last name not entered',
        'Non-alphanumeric last name entered']

#MESSAGE
NAME = ['Sender name not entered',
        'Non-alphanumeric sender name entered']

SUBJECT = ['Message subject not entered',
           'Invalid subject format entered']

BODY = ['Message body not entered',
        'Invalid body format entered']

REGEX_NAME = '^[\w\s-]+$'
REGEX_SUBJECT = "^[\w'*$&!?,.;:()/\s-]+$"
REGEX_BODY = "^[\w'*$&!?,.;:()/\s-]+$"
MESSAGE_SUCCESS = "Your message has been sent."
MESSAGE_FAIL = "Your message has not been sent."

#REVIEW
REVIEW_SUCCESS = "Your review has been submitted. Thank you!"

ADDRESS1 = ['Street address1 not entered',
            'Invalid street address1 format',
            'Address saved']

ADDRESS2 = ['Street address2 not entered',
            'Invalid street address2 format']

CITY = ['City not entered',
        'Non-alphanumeric city entered']

STATE = ['State not entered',
         'Non-alphanumeric state entered']

ZIP = ['Zip not entered',
       'Invalid zip format entered']

PHONE = ['Phone number not entered',
         'Invalid phone number entered']

NOTE = ['Phone number not entered',
        "Invalid note format entered ( letters, numbers and. ? ! : ; - ( ) ' / ,  & $ * . , ! only )"]

QUANTITY = ['Quantity not entered',
            'Non-integer quantity entered',
            'Quantity cannot be negative',
            'Not Enough Stock Available',
            'Quantity Updated']

AMOUNT = ['Bitcoin Amount not entered',
          'Non-numeric amount entered']

SHIPPING_COST = ['Shipping cost not entered',
                 'Non-numeric shipping cost entered']

UNDEF = 'Undef error message'


#PRODUCT
TITLE = ['Title not entered',
         "Invalid name format entered ( letters, numbers and. ? ! : ; - ( ) ' / ,  & $ * . , ! only )"]

DESCRIPTION = ['Description not entered',
               "Invalid description format entered ( letters, numbers and. ? ! : ; - ( ) ' / ,  & $ * . , ! only )",
               'Description must be between 5 and 2000 characters long']

PRICE = ['Price not entered',
         'Price must be numeric',
         'Price must be greated than 0']

STOCK = ['Stock value not entered',
         'Stock value must be greater than 0',
         'Stock value must be an integer']

COUNTRIES = ['Shipping destination not selected',
             'Shipping cost must be numeric']


STORE_DESCRIPTION = ['Description must be between 5 and 200 characters long']

NULL_IMAGE = 'images/products/no-image'
NULL_LOGO = 'images/stores/no-image'


REVIEW_HEADLINE = ['Review headline not entered',
                   'Invalid review headline format']

REVIEW_BODY = ['Review body not entered']

MESSAGE_SUBJECT = ['Message subject not entered',
                   'Invalid message subject format']

MESSAGE_BODY = ['Message body not entered']

INVALID_QUERY = 'Non-alphanumeric search query entered'
INVALID_SHIPPING = 'Invalid shipping rate entered'
INVALID_VENDOR_TOKEN = 'Invalid user token entered'
OK_RESPONSE = "OK"

SUCCESS_LOGIN = "Login successful!"
VERIFY_SUCCESS = "Email successfully verified"
UPDATE_SUCCESS = "Information saved"
CLOSE_SUCCESS = "Store closed successfully"

REGEX_QUERY = '^[\w-]+$'
REGEX_BITCOIN_ADDRESS = '^[\w-]+$'
REGEX_EMAIL = '^[^@ ]+@[^@ ]+\.[^@ ]+$'
REGEX_PASSWORD = '^[\w-]+$'
REGEX_PHONE = '^[\w-]*$'
#REGEX_REVIEW_HEADLINE = '^[\w\s-]+$'
REGEX_REVIEW_HEADLINE = "^[\w'*$&!?,.;:()/\s-]+$"
REGEX_MESSAGE_SUBJECT = "^[\w'*$&!?,.;:()/\s-]+$"
REGEX_MESSAGE_BODY = "^[\w'*$&!?,.;:()/\s-]+$"
REGEX_DESCRIPTION = "^[\w'*$&!?,.;:()/\s-]+$"
REGEX_NOTE = "^[\w'*$&!?,.;:()/\s-]*$"
REGEX_TITLE = "^[\w'*$&!?,.;:()/\s-]+$"
REGEX_STORENAME = '^[\w-]+$'
REGEX_TOKEN = '^[\w-]+$'
REGEX_FIRST = '^[\w\s-]+$'
REGEX_LAST = '^[\w\s-]+$'
REGEX_STREET_ADDRESS_1 = '^[\w\s\-\.]+$'
REGEX_STREET_ADDRESS_2 = '^[\w\s\-\.]*$'
REGEX_CITY = '^[\w\s-]+$'
REGEX_STATE = '^[\w\s-]+$'
REGEX_ZIP = '^[\w-]+$'
REGEX_COUNTRY = '^[\w-]+$'

currencies = ['USD',
              'AUD',
              'CHF',
              'RUB',
              'SEK',
              'THB',
              'CNY',
              'JPY',
              'GBP',
              'NZD',
              'PLN',
              'EUR',
              'DKK',
              'SGD',
              'HKD',
              'CAD']

productCategories = {'ZZ': 'All Categories',
                     'AA': 'Automotive & Industrial',
                     'AB': 'Books',
                     'AC': 'Clothing, Shoes & Jewelry',
                     'AD': 'Electronics & Office',
                     'AE': 'Grocery, Health & Beauty',
                     'AF': 'Home, Garden & Tools',
                     'AG': 'Miscellaneous',
                     'AH': 'Movies, Music & Games',
                     'AI': 'Pets',
                     'AJ': 'Sports & Outdoors',
                     'AK': 'Toys, Kids & Baby',
                     'AL': 'Art & Collectibles'}

shippingCarriers = {'AA': 'DHL',
                    'AB': 'Fedex',
                    'AC': 'UPS',
                    'AD': 'UPS Mail Innovations',
                    'AE': 'USPS',
                    'AF': 'Other'}

campaign_types = {
        'AA': 'One-time',
        'AB': 'Extended'
    }

niches = {
        'AA': 'Music',
        'AB': 'Fashion',
        'AC': 'Design',
        'AD': 'Technology',
        'AE': 'Television',
        'AF': 'Commerce'
    }

orderCancelationReasons = {'AA': 'Order not paid within 24 hours of placement',
                           'AB': 'Fraudulent customer information provided',
                           'AC': 'Buyer refund granted',
                           'AD': 'Payment address fault',
                           'AE': 'Developer testing'}

offerCancelationReasons = {
        'AA': 'Developer testing',
        'AB': 'Not enough stock'
        }

carriers = ['DHL',
            'Fedex',
            'UPS',
            'UPS Mail Innovations',
            'USPS',
            'Other']


questions = ['Was description of the item accurate?',
             'Did seller ship the item quickly?',
             'Was price of the item fair?',
             'Were shipping and handling charges reasonable?',
             'Would you buy from the seller again?']

restrictedStoreNames = ['addressBook',
                        'buyPhysical',
                        'buyer',
                        'cancel',
                        'category',
                        'checkoutDigital',
                        'checkout',
                        'createBuyer',
                        'createSeller',
                        'disconnect',
                        'deleteAddress',
                        'deletePhysical',
                        'deleteProduct',
                        'deleteUser',
                        'faq',
                        'get_session_user',
                        'images',
                        'invoice',
                        'loadAddress',
                        'loadCountries',
                        'loadRating',
                        'login',
                        'loginAction',
                        'logout',
                        'orders',
                        'orders',
                        'policy',
                        'promoteAddress',
                        'receipt',
                        'resetAddress',
                        'recoverPassword',
                        'saveAddress',
                        'saveBuyerInfo',
                        'savePassword',
                        'savePaymentStatus',
                        'savePhysical',
                        'saveSellerInfo',
                        'saveUser',
                        'saveQuantity',
                        'saveReview',
                        'saveStore',
                        'saveTrackingNumber',
                        'scripts',
                        'searchAction',
                        'seller',
                        'sendToken',
                        'settings',
                        'styles',
                        'summaryOrders',
                        'summaryPayments',
                        'summaryProducts',
                        'summarySessions',
                        'summaryUsers',
                        'terms',
                        'verifyDetailsDigital',
                        'verifyDetailsPhysical',
                        'verifyToken']
#%s/, .*/

accountTypes = ['admin',
                'buyer',
                'seller']

paymentStatuses = ['Not paid',
                   'Paid']

shippingStatuses = ['Not shipped',
                    'Shipped']

countries = {'AA': 'Afghanistan',
             'AB': 'Albania',
             'AC': 'Algeria',
             'AD': 'Andorra',
             'AE': 'Angola',
             'AF': 'Antigua and Deps',
             'AG': 'Argentina',
             'AH': 'Armenia',
             'AI': 'Australia',
             'AJ': 'Austria',
             'AK': 'Azerbaijan',
             'AL': 'Bahamas',
             'AM': 'Bahrain',
             'AN': 'Bangladesh',
             'AO': 'Barbados',
             'AP': 'Belarus',
             'AQ': 'Belgium',
             'AR': 'Belize',
             'AS': 'Benin',
             'AT': 'Bhutan',
             'AU': 'Bolivia',
             'AV': 'Bosnia Herzegovina',
             'AW': 'Botswana',
             'AX': 'Brazil',
             'AY': 'Brunei',
             'AZ': 'Bulgaria',
             'BA': 'Burkina',
             'BB': 'Burundi',
             'BC': 'Cambodia',
             'BD': 'Cameroon',
             'BE': 'Canada',
             'BF': 'Cape Verde',
             'BG': 'Central African Rep',
             'BH': 'Chad',
             'BI': 'Chile',
             'BJ': 'China',
             'BK': 'Colombia',
             'BL': 'Comoros',
             'BM': 'Congo',
             'BN': 'Congo (Democratic Rep)',
             'BO': 'Costa Rica',
             'BP': 'Croatia',
             'BQ': 'Cuba',
             'BR': 'Cyprus',
             'BS': 'Czech Republic',
             'BT': 'Denmark',
             'BU': 'Djibouti',
             'BV': 'Dominica',
             'BW': 'Dominican Republic',
             'BX': 'East Timor',
             'BY': 'Ecuador',
             'BZ': 'Egypt',
             'CA': 'El Salvador',
             'CB': 'Equatorial Guinea',
             'CC': 'Eritrea',
             'CD': 'Estonia',
             'CE': 'Ethiopia',
             'CF': 'Fiji',
             'CG': 'Finland',
             'CH': 'France',
             'CI': 'Gabon',
             'CJ': 'Gambia',
             'CK': 'Georgia',
             'CL': 'Germany',
             'CM': 'Ghana',
             'CN': 'Greece',
             'CO': 'Grenada',
             'CP': 'Guatemala',
             'CQ': 'Guinea',
             'CR': 'Guinea-Bissau',
             'CS': 'Guyana',
             'CT': 'Haiti',
             'CU': 'Honduras',
             'CV': 'Hungary',
             'CW': 'Iceland',
             'CX': 'India',
             'CY': 'Indonesia',
             'CZ': 'Iran',
             'DA': 'Iraq',
             'DB': 'Ireland (Republic)',
             'DC': 'Israel',
             'DD': 'Italy',
             'DE': 'Ivory Coast',
             'DF': 'Jamaica',
             'DG': 'Japan',
             'DH': 'Jordan',
             'DI': 'Kazakhstan',
             'DJ': 'Kenya',
             'DK': 'Kiribati',
             'DL': 'Korea North',
             'DM': 'Korea South',
             'DN': 'Kosovo',
             'DO': 'Kuwait',
             'DP': 'Kyrgyzstan',
             'DQ': 'Laos',
             'DR': 'Latvia',
             'DS': 'Lebanon',
             'DT': 'Lesotho',
             'DU': 'Liberia',
             'DV': 'Libya',
             'DW': 'Liechtenstein',
             'DX': 'Lithuania',
             'DY': 'Luxembourg',
             'DZ': 'Macedonia',
             'EA': 'Madagascar',
             'EB': 'Malawi',
             'EC': 'Malaysia',
             'ED': 'Maldives',
             'EE': 'Mali',
             'EF': 'Malta',
             'EG': 'Marshall Islands',
             'EH': 'Mauritania',
             'EI': 'Mauritius',
             'EJ': 'Mexico',
             'EK': 'Micronesia',
             'EL': 'Moldova',
             'EM': 'Monaco',
             'EN': 'Mongolia',
             'EO': 'Montenegro',
             'EP': 'Morocco',
             'EQ': 'Mozambique',
             'ER': 'Myanmar (Burma)',
             'ES': 'Namibia',
             'ET': 'Nauru',
             'EU': 'Nepal',
             'EV': 'Netherlands',
             'EW': 'New Zealand',
             'EX': 'Nicaragua',
             'EY': 'Niger',
             'EZ': 'Nigeria',
             'FA': 'Norway',
             'FB': 'Oman',
             'FC': 'Pakistan',
             'FD': 'Palau',
             'FE': 'Panama',
             'FF': 'Papua New Guinea',
             'FG': 'Paraguay',
             'FH': 'Peru',
             'FI': 'Philippines',
             'FJ': 'Poland',
             'FK': 'Portugal',
             'FL': 'Qatar',
             'FM': 'Romania',
             'FN': 'Russian Federation',
             'FO': 'Rwanda',
             'FP': 'St Kitts and Nevis',
             'FQ': 'St Lucia',
             'FR': 'Saint Vincent and the Grenadines',
             'FS': 'Samoa',
             'FT': 'San Marino',
             'FU': 'Sao Tome and Principe',
             'FV': 'Saudi Arabia',
             'FW': 'Senegal',
             'FX': 'Serbia',
             'FY': 'Seychelles',
             'FZ': 'Sierra Leone',
             'GA': 'Singapore',
             'GB': 'Slovakia',
             'GC': 'Slovenia',
             'GD': 'Solomon Islands',
             'GE': 'Somalia',
             'GF': 'South Africa',
             'GG': 'South Sudan',
             'GH': 'Spain',
             'GI': 'Sri Lanka',
             'GJ': 'Sudan',
             'GK': 'Suriname',
             'GL': 'Swaziland',
             'GM': 'Sweden',
             'GN': 'Switzerland',
             'GO': 'Syria',
             'GP': 'Taiwan',
             'GQ': 'Tajikistan',
             'GR': 'Tanzania',
             'GS': 'Thailand',
             'GT': 'Togo',
             'GU': 'Tonga',
             'GV': 'Trinidad and Tobago',
             'GW': 'Tunisia',
             'GX': 'Turkey',
             'GY': 'Turkmenistan',
             'GZ': 'Tuvalu',
             'HA': 'Uganda',
             'HB': 'Ukraine',
             'HC': 'United Arab Emirates',
             'HD': 'United Kingdom',
             'HE': 'United States',
             'HF': 'Uruguay',
             'HG': 'Uzbekistan',
             'HH': 'Vanuatu',
             'HI': 'Vatican City',
             'HJ': 'Venezuela',
             'HK': 'Vietnam',
             'HL': 'Yemen',
             'HM': 'Zambia',
             'HN': 'Zimbabwe',
             'ZZ': 'Worldwide'}
