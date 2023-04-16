"# UFSWDN-Capstone" 
## Motivation
- I currently work for a countertop company, we fabricate and install any type of surfaces. Granite, marble, quartz, quartzite, porcelain, etc. Everything is going well but one of the big problems we have is that we, employees, dont have a way to look at what jobs are coming up or are a priority over others. This is why I decided to create a list of jobs. Another problem we currently have at work is that we dont have a way to keep track of all the sinks we use and how many we currently have in storage without having to go and count each one of them, which can be time consuming. 
I couldn't do it this time, because of time constraints, but I would like to add a way to change a jobs status to complete and have my app/website update the inventory item by looking at the jobs' sink list.
I also want to hide things from the frontend depending on certain permissions, add set of options to status on jobs, and probably add confirmation dialogs when deleting an item from either tables.

## Heroku app URL
[mccapstone.herokuapp.com](http://mccapstone.herokuapp.com/)

## Running instructions.
- To be able to run this project locally, please install all requirements from the requirements.txt file by running the following command:
<code>pip install -r requirements.txt</code>
- Then update the following global variables:
<code>
    - DATABASE_URL
    - APP_SECRET_KEY
    - AUTH0_CLIENT_ID
    - AUTH0_CLIENT_SECRET
    - AUTH0_DOMAIN
    - AUTH0_AUDIENCE
    - AUTH0_CALLBACK</code>
- The database_url is from herokuapp, app_secret_key is made up within flask, and all the rest ones are from auth0, the third party authorization service.

- If you would like to run the application locally, you can set up all the environment variables by running the file setup.sh.
- When running the application either locally or testing the live version, please keep in mind that the login button might glitch once in a while making it seem you are logged out, but you are truly logged in unless you were able to click the "logout" button.

## Auth0 Setup
- Lets first create a Regular Web application.
    - Call it whatever you want, but always keep it in mind.
- Second, create an API. Choose a name and use the same name as the Identifier.
- Third, go to the application you just created, keep track of your domain, client id, and client secret. This are going to be saved to your global variables above. Under the allowed callback and logout urls add localhost:5000 for our local enviroment, and your url of choice for deployment, I chose heroku so I added http://mccapstone.herokuapp.com, Then allow Cross-Origin Authentication
- Then go back to the API, keep track of the Identifier, it is also our Audience variable. Toggle on Enable RBAC and Add Permissions in the Access Token.
- From there go to permissions and add the following permissions:
<code>
    - read:jobs
    - read:job-details
    - patch:job
    - delete:job
    - create:job 
    - read:inventory
    - read:inventory_item
    - patch:inventory_item
    - delete:inventory_item
    - create:inventory_item
    - read:sinks
    - read:sink
    - patch:sink
    - create:sink
    - delete:sink</code>
- After this we can create two roles; an Admin and a User. We give the Admin all permissions and the User only the permissions: read:jobs and read:job-details

## Error Handling
Errors return in the following json format:

```
{
    'success':False,
    'error':404,
    'message':'Not found'
}
```

This api is able to return the following errors:
- 400
- 404
- 422
- 500
- 401

## API - Enpoints
Endpoints can either return a template or data in the form of json depending on a test variable. This allowed me to, both, deploy the application to a web server and run tests locally.
The following explanation will be taking into consideration the actual app running in a webserver, which returns a flask template most of the time with some data. 
### GET ```/```
- Fetches and displays all jobs.
- Returns pages/home.html and passes in all jobs from the Job table.
- When in testing mode:
```
{"success":True,
"jobs": list of jobs ran through format()}
```

### POST ```/job```
#### Required permission = ```read:jobs```
- Uses data from a form and creates a new job
- Redirects to the home endpoint.
- When in testing mode:
```
{"success": True,
"job_id": 1}
```

### GET ```/job/<int:id>```
#### Required permission = ```read:job```
- Uses the passed in id and references a job, if found.
- Returns the view_job.html file from pages and passes in the job information
- Wehn in testing mode:
```
{
    "success": True,
    "job": job information
}
```

### POST ```/job/<int:id>```
#### Required permission = ```patch:job```
- Updates given id job.
- Reads data from a form and uses it to update the id job.
- When in testing mode:
```
    {"success": True,
    "job": job.format()
    }
```

### DELETE ```/job/<int:id>/delete_job```
#### Required permission = ```delete:job```
- Deletes the given id job.
- Returns a redirect to home
- When in testing mode:
```
    {"success": True,
        "job": job.format()['id']
    }
```

### GET ```/inventory```
#### Required permission = ```read:inventory```
- Returns all inventory items from Inventory table.
- When in testing mode:
```
{
    "success": True, 
    "inventory": [item.format() for item in Inventory.query.all()]
}
```

### GET ```/inventory/<int:id>```
#### Required permission = ```read:inventory_item```
- Returns information of given id inventory_item
- Returns pages/view_inventory_item.html
- When in testing mode:
```
{
    "success": True,
    "inventory_item": inventory_item.format()
}
```

### POST ```/inventory/<int:id>```
#### Required permission = ```patch:inventory_item```
- Updates given id inventory_item
- Redirects to inventory endpoint
- When in testing mode:
```
{
    "success": True,
    "inventory_item": inventory_item.format()
}
```

### POST ```/inventory/add```
#### Required permission = ```create:inventory_item```
- Adds a new inventory_item.
- Uses form data to create above item.
- Returns the inventory page and passes in all items in the query.
- When in testing mode:
```
{
    "success": True, 
    "inventory_items": [inventory_item.format() for inventory_item in Inventory.query.all()], "inventory_item_id": item.id
}
```

### DELETE ```/inventory/<int:id>/delete_inventory_item```
#### Required permission = ```delete:inventory_item```
- Deletes inventory_item with the given id.
- Redirects to inventory endpoint
- When in testing mode:
```
{
    "success": True,
    "inventory_item_id": inventory_item.format()['id'],
    "inventory_items": [inventory_item.format() for inventory_item in Inventory.query.all()]
}
```

### GET ```/sinks```
#### Required permission = ```read:sinks```
- Fetches all sinks in sink table
- Returns template /pages/sinks.html
- When in testing mode:
```
{
    "success": True, 
    "sinks": [sink.format() for sink in Sink.query.all()]
}
```

### GET ```/sinks/<int:id>```
#### Required permission = ```read:sink```
- Fetches sink with id
- returns template for /pages/view_sink.html
- When in testing mode:
```
{
    "success": True,
    "sink": sink.format()
}
```

### POST ```/sinks/<int:id>```
#### Required permission = ```patch:sink```
- Updates sink with given id
- Redirects to sinks endpoint
- When in testing mode:
```
{
    "success": True,
    "sink": sink.format()
}
```

### DELETE ```/sinks/<int:id>/delete_sink```
#### Required permission = ```delete:sink```
- Deletes sink with given id
- Redirects to sinks endpoint
- When in testing mode:
```
{
    "success": True,
    "sink": sink.format()['id']
}
```

### POST ```/sinks/add```
#### Required permission = ```create:sink```
- Uses data from form to add a new sink
- Returns template for /pages/sinks.html
- When in testing mode:
```
{
    "success": True,
    "sinks": [sink.format() for sink in Sink.query.all()],
    'sink_id': sink.id
}
```

# Testing
- Had to generate 2 tokens one for Admin and one more user, this will allow me to use it until the tokens expire and test user and admin specific permissions.

- Here are two accounts with their respective passwords to be able to test the live app:
```
Admin:
admintest@gmail.com
AdminPassword1!

User:
usertest@gmail.com
UserPassword1!
```

JWTS
```
User: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdlWnQxR0JZY25jZkJ2eVpheEVIMCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ubXl4azdoZnRvbWVmbHJkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDNiNzlkZDVjNzI2NmRjNzdmOTFkMDMiLCJhdWQiOiJjYXBzdG9uZUFQSSIsImlhdCI6MTY4MTY0NDk0MCwiZXhwIjoxNjgxNjUyMTQwLCJhenAiOiJQWUVQcmJjU25XUGxUcklBanZUanAyY2FuaUpuU290VCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicmVhZDpqb2ItZGV0YWlscyIsInJlYWQ6am9icyJdfQ.jrnWdV83RqGMjlUHfckkIz1kfrjVD3frYMUzxPPxx-0Uw7QcL3ktfiS1n1m3FGQv_Vw8WSXCZgFU8CAA3PDcVZUxh9YXUiAnyYHHbiRDCfN3gQnsQQehXp9ozkWUVSImdbJWFxGnQ5q6mWHlPr_0-IQMO8bcZgN7nETfE9UUpSaEvCOZ3i9pfgpnyx3DYJjO_PozzCnDZTtqBvNoIb_OSYhf11RDQCB-aUMnu1OZcjjtrHaGGCbZ6RmPWyaFBklxbfUETAd5FhyyWZIZPl91_X0uYkG27vFifyCr8sZgZiAYArEV-scX0xc29v2nwYdRzfKHVrE6RFq8t6RB-MWlDQ

Admin: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdlWnQxR0JZY25jZkJ2eVpheEVIMCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ubXl4azdoZnRvbWVmbHJkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDNiNzk5ZWI3YWRkMTVhODliNTI1OWUiLCJhdWQiOiJjYXBzdG9uZUFQSSIsImlhdCI6MTY4MTY0NDg5MiwiZXhwIjoxNjgxNjUyMDkyLCJhenAiOiJQWUVQcmJjU25XUGxUcklBanZUanAyY2FuaUpuU290VCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmludmVudG9yeV9pdGVtIiwiY3JlYXRlOmpvYiIsImNyZWF0ZTpzaW5rIiwiZGVsZXRlOmludmVudG9yeV9pdGVtIiwiZGVsZXRlOmpvYiIsImRlbGV0ZTpzaW5rIiwicGF0Y2g6aW52ZW50b3J5X2l0ZW0iLCJwYXRjaDpqb2IiLCJwYXRjaDpzaW5rIiwicmVhZDppbnZlbnRvcnkiLCJyZWFkOmludmVudG9yeV9pdGVtIiwicmVhZDpqb2ItZGV0YWlscyIsInJlYWQ6am9icyIsInJlYWQ6c2luayIsInJlYWQ6c2lua3MiXX0.EyN_Sys7O6gVeXt7QX198sjTdu5EZEFhvD7Ab10Csz3LnV3isWEjVKjItXqQgxFmvM1jBGr5NmzPSpDO52PAhy0opnGOIFhunbTG0hyvndwXZN4xepvM3WDFOM9cUllUA9mvuIpDMnWVtzSNG4Bv7NaCWjijoZtbz-0CWzAsKPgyUULgZJ5vnjRvOFwmXkt2bS_aFGgOCML5VGn4vZRGWukPd7627gFNGqATpF12nZZdtnmA4JfJPAHIxam3HlsHzY0YbTckL8TtsnMuJgleK1bKfPq0M3TUwbgvGMVIM6cxfIhuABdQZqczOdxbj8_oH89i1xEcZaUZuLkHxlR3mg
```

If by the time someone reads this the tokens have expired, you can get them from the url after loging in with the above credentials.

## POSTMA
- If you would like to run POSTMA against the app.py file, please turn on testing mode by changing the test variable to True at the top of said file.

## Migrations
- When there is a change on database tables, we need to run the following commands
- flask db migrate
- push to github
- deploy on heroku
- heroku run flask db upgrade

## Author and Credits
- Work done by Miguel Castrejon.
- Some code segments taken from Udacity lectures.



