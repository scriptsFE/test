### Importing Packages ###
import requests;
import urllib3;
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);

## Cookies File ##
cookiesFile = open('cookies.txt', 'r');
cookies = [c for c in cookiesFile.read().split('\n') if c.strip() != ''];

## User ID Input ##
user_ID = input('Roblox\'s user ID?\nType the user ID... ');

#################### GET PROXIES ####################
## Proxies File ##
try:
  proxiesFile = open('proxies.txt', 'r');
  proxies = [p for p in proxiesFile.read().split('\n') if p.strip() != ''];
except FileNotFoundError:
  proxies = [];

#################### CHECKS ####################
if len(proxies) == 0:
  print('\x1b[33mNo proxies detected. The code will error.\x1b[0m');

if len(cookies) == 0:
  print('\x1b[33mThis feature will not work without cookies.\x1b[0m');

#################### MAIN FOLLOW BOTTER ####################
for cookie in cookies:
  csrfHeaders = {
    'Cookie': '.ROBLOSECURITY=' + cookie,
  };

  ## Get CSRF Token directly (no proxy) ##
  try:
    csrfRequest = requests.post('https://auth.roblox.com/v2/logout', headers=csrfHeaders, verify=False);
    if csrfRequest.status_code != 403:
      print('\x1b[31mCookie is invalid or expired. Status: ' + str(csrfRequest.status_code) + '\x1b[0m');
      break;
    csrfToken = csrfRequest.headers['x-csrf-token'];
    print('\x1b[32mLogged in! Got CSRF token. Trying proxies...\x1b[0m');
  except Exception as e:
    print('\x1b[31mFailed to connect to Roblox: ' + str(e) + '\x1b[0m');
    break;

  ## Headers with valid token ##
  headers = {
    'X-CSRF-TOKEN': csrfToken,
    'Cookie': '.ROBLOSECURITY=' + cookie,
  };

  ## Send follow request directly ##
  print('\x1b[32mSending follow to {user}...\x1b[0m'.format(user=user_ID));
  try:
    r = requests.post(
      'https://friends.roblox.com/v1/users/{user}/follow'.format(user=user_ID),
      headers=headers,
      verify=False,
      timeout=10
    );
    if r.status_code == 200:
      print('\x1b[32mSuccessfully followed! Check your followers list.\x1b[0m');
    elif r.status_code == 401:
      print('\x1b[31mCookie rejected. Status: 401\x1b[0m');
    elif r.status_code == 403:
      print('\x1b[31mBlocked by Roblox. Status: 403\x1b[0m');
    else:
      print('\x1b[31mUnexpected response: ' + str(r.status_code) + ' - ' + r.text + '\x1b[0m');
  except Exception as e:
    print('\x1b[31mError sending follow: ' + str(e) + '\x1b[0m');
