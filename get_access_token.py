import http.client

conn = http.client.HTTPSConnection("dev-nmyxk7hftomeflrd.us.auth0.com")

payload = "grant_type=access_token&client_id=PYEPrbcSnWPlTrIAjvTjp2caniJnSotT&client_secret=yuMq7yBG_y2ht6LXkY_GBlG-mqvP5fPCDfaW5k2Q-2qPCbop1zGL08ad6pmPqWIF&audience=capstone"

headers = { 'content-type': "application/x-www-form-urlencoded" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))