# Security Aspects

## GitHub API Webhook Requests

Requests that are coming from GitHub API for push events are validated against the GitHub secret token.

```python
import hmac
import hashlib
def verify_github_signature_from_webhook(secret_token: str, payload_body: any, signature_header: str) -> None:
  if not signature_header:
    raise HTTPException(
      status_code=403,
      detail="You really should not be here"
    )
  hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
  expected_signature = "sha256=" + hash_object.hexdigest()
  if not hmac.compare_digest(expected_signature, signature_header):
    raise HTTPException(
      status_code=403,
      detail="We know you are trying as hard as you can, but you are both not allowed and not smart enough to do this pal..."
    )
```


## Competitor User and Admin User

The competitor user are separated from the admin user, and have a different authentication system.

Admin system is internal, and basically unchangable, whereas the competitor user is authenticated via Firebase Authentication.

There is no chance for the competitor user to access the admin system, and vice versa.


## Backend & Engine Side Secret Tokens

Entire privilidges actions are taken in the services of Backend and Engine, which are mostly the GitHub PAT tokens and AWS credentials.

Since both of these services are running in a private network, the secrets are not exposed.

The GitHub requests are completely sent form the backend, for repository creation, invitation sending and webhook creation.

The repository cloning is done by the Engine, and cloned repository are copied to the Docker image build context, which will run in AWS.


## Backend / Engine Communication

This part is not yet implemented, yet the idea in mind is to create a validation token that will be sent with the requests between the Backend and Engine.

This might be quite similar to the validation process of the GitHub API webhook requests.


## Protection Against Endpoint Abuse

The endpoints are protected against abuse by using the following methods:
- **Rate Limiting**: The API endpoints are rate-limited to prevent abuse and excessive requests from a single user or IP address.
- **Authentication**: Almost all endpoints require authentication, ensuring that only authorized users can access them. If an authenticated user tries to abuse the system, they will be blocked after a certain number of failed attempts.
- **Error Handling**: Proper error handling is implemented to prevent information leakage and to ensure that the system does not reveal sensitive information in error messages.
- **Logging and Monitoring**: All API requests and responses are logged for monitoring purposes. This helps in identifying any suspicious activity or potential abuse of the system.
- **CORS Policy**: The CORS policy is set to allow only specific origins, preventing unauthorized domains from accessing the API.
- **CSRF Protection**: CSRF protection is implemented to prevent cross-site request forgery attacks. This ensures that requests made to the API are intentional and not made by malicious actors.

