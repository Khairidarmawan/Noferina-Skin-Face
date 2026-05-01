```python
import streamlit_authenticator as stauth

names = ["Admin"]

usernames = ["admin"]

passwords = ["12345"]

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "skin_ai",
    "abcdef",
    cookie_expiry_days=30
)
```
