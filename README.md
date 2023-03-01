# Google Calendar Integration using Django REST API

This is a project to implement Google Calendar integration using Django REST API. The OAuth2 mechanism is used to get users calendar access.

## **API Endpoints and Views**

The following API endpoints are implemented:

**/rest/v1/calendar/init/ -> GoogleCalendarInitView()**

### [`https://convin-backend-task.ayushr1.repl.co/rest/v1/calendar/init/`](https://convin-backend-task.ayushr1.repl.co/rest/v1/calendar/init/)

This view would start step 1 of the OAuth, which will prompt the user for his/her credentials.

### **/rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView()**

### [`https://convin-backend-task.ayushr1.repl.co/rest/v1/calendar/redirect/`](https://convin-backend-task.ayushr1.repl.co/rest/v1/calendar/redirect/)

This view will do two things:

1. Handle the redirect request sent by Google with the code for the token. The mechanism to get the access_token from the given code is implemented.
2. Once the access_token is obtained, we get the list of events in the user's calendar.

## **Libraries Used**

Only Google's provided standard libraries are used. Nothing else.

## **Submission**

The submission is shared as a public Repl.it environment and as a Github repo here. 

[data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%2730%27%20height=%2730%27/%3e](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%2730%27%20height=%2730%27/%3e)

[https://convin-backend-task.ayushr1.repl.co/](https://convin-backend-task.ayushr1.repl.co/)

# Notes

The API is currently deployed on testing stage with external scope which is limited to authorised test users. Production requires verification with the use mentioned apis of google calendar.