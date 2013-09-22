from oauth2client.client import OAuth2WebServerFlow
import httplib2

CLIENT_ID = '1e6dc802a76840817a9055a49dc86ae801ad4b474d5a97a1b7dce1e3cc01b1bc'
CLIENT_SECRET = '00579619f736854a922e18d2652e6608cad3f83abe0d8e3327b3c588905314e1'
CALLBACK_URL = 'https://www.bitcoinrealty.ca/callback'

coinbase_client = OAuth2WebServerFlow(
        CLIENT_ID, 
        CLIENT_SECRET, 
        'all', 
        redirect_uri=CALLBACK_URL, 
        auth_uri='https://coinbase.com/oauth/authorize', 
        token_uri='https://coinbase.com/oauth/token'
)

auth_url = coinbase_client.step1_get_authorize_url()

print auth_url

oauth_code = 'AAAAA'
#http = httplib2.Http(ca_certs='/etc/ssl/certs/ca-certificates.crt')
#token = coinbase_client.step2_exchange(oauth_code, http=http)
token = coinbase_client.step2_exchange(oauth_code, http=None)
print token.to_json()
