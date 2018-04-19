---
weight: 20
title: Errors

---

# Errors
>If your request or browser returns an unexpected result, there is either something wrong with your url/request/api-key (for __4xx__ errors) or something wrong with your server (for __5xx__ errors).

Code | Meaning
---------- | -------
2xx | Success!
4xx | Client Error!
5xx | Internal Server Error!
400 | Bad Request -- Check your request.
401 | Unauthorized -- Your API key is wrong
403 | Forbidden -- You have no permission for this request. Please check your Authorization.
404 | Not Found -- The specified page or request not found. Check your url.
405 | Method Not Allowed -- Your request used an invalid method. Try http GET request.
500 | Internal Server Error -- We had a problem with our server. Try again later.
503 | Service Unavailable -- We're temporally offline for maintenance. Please try again later.

