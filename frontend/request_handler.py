import requests
from requests.exceptions import RequestException


class RequestHandler:
    def __init__(self):
        self.base_url = "http://localhost:8080"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
        })
        self.email = None

    def get_cookie(self, name):
        cookie_value = None
        cookie_string = self.session.cookies.get_dict()
        if name in cookie_string:
            cookie_value = cookie_string[name]
        return cookie_value

    def handle_error(self, error):
        if isinstance(error, RequestException):
            response = error.response
            if response is not None:
                print('Error Response Data:', response.text)
                print('Error Response Status:', response.status_code)
                print('Error Response Headers:', response.headers)
            else:
                print('No response received:', error.request)
        else:
            print('Request Error:', str(error))

    def _get_headers_with_csrf(self):
        # Fetch the CSRF token from cookies and add it to the headers
        csrf_token = self.get_cookie('csrftoken')
        headers = {
            'X-CSRFToken': csrf_token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        } if csrf_token else {}
        return headers

    def login(self, email, password):
        try:
            data = {'email': email, 'password': password}
            headers = self._get_headers_with_csrf()
            response = self.session.post(f"{self.base_url}/user/token/", json=data, headers=headers)
            response.raise_for_status()
            if(response.status_code==200):
                self.email = data['email']
                print(self.email)
            return response
        except RequestException as error:
            self.handle_error(error)

    def logout(self):
        try:
            data = {'email': self.email}
            headers = self._get_headers_with_csrf()
            response = self.session.post(f"{self.base_url}/user/logout/", json=data, headers=headers)
            response.raise_for_status()
            if(response.status_code==200):
                self.email = None
                print(self.email)
            return response
        except RequestException as error:
            self.handle_error(error)

    def signup(self, email, password, name, is_active=True):
        try:
            data = {
                'email': email,
                'password': password,
                'name': name,
                'is_active': is_active
            }
            headers = self._get_headers_with_csrf()
            response = self.session.post(f"{self.base_url}/user/create/", json=data, headers=headers)
            response.raise_for_status()
            return response
        except RequestException as error:
            self.handle_error(error)

    def get_request(self, url, params=None):
        headers = self._get_headers_with_csrf()
        try:
            res = self.session.get(
                f"{self.base_url}{url}",
                params=params,
                headers=headers
            )
            res.raise_for_status()
            return res
        except RequestException as error:
            self.handle_error(error)

    def post_request(self, url, data=None, params=None):
        headers = self._get_headers_with_csrf()
        try:
            res = self.session.post(
                f"{self.base_url}{url}",
                json=data,
                params=params,
                headers=headers
            )
            res.raise_for_status()
            return res
        except RequestException as error:
            self.handle_error(error)

    def put_request(self, url, data=None, params=None):
        headers = self._get_headers_with_csrf()
        try:
            res = self.session.put(
                f"{self.base_url}{url}",
                json=data,
                params=params,
                headers=headers
            )
            res.raise_for_status()
            return res
        except RequestException as error:
            self.handle_error(error)

    def delete_request(self, url, params=None):
        headers = self._get_headers_with_csrf()
        try:
            res = self.session.delete(
                f"{self.base_url}{url}",
                params=params,
                headers=headers
            )
            res.raise_for_status()
            return res
        except RequestException as error:
            self.handle_error(error)

handler = RequestHandler()
res = handler.login('user@example1.com', 'string')


print("Cookies set by the server:")
for cookie in res.cookies:
    print(f'{cookie.name}: {cookie.value}')

print(len(handler.session.cookies))
for cookie in handler.session.cookies:
    print (f'{cookie.name} : {cookie.value}')
handler.logout()