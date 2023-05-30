import streamlit_authenticator as stauth

list_of_passwords = [
    '123',
    '123',
]

for pw in list_of_passwords:
    hash = stauth.Hasher([pw]).generate()[0]
    print(f'hash for password "{pw}": {hash}')