import datetime

from ninja import Schema
from pydantic import EmailStr

from config.utils.schemas import Token


class AccountOut(Schema):
    email: EmailStr
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    address1: str = None
    address2: str = None
    company_name: str = None
    company_website: str = None
    date_joined: datetime.datetime
    is_verified: bool = None


class AccountSignupIn(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    password1: str
    password2: str


class AccountSignupOut(Schema):
    profile: AccountOut
    token: Token


class AccountConfirmationIn(Schema):
    email: EmailStr
    verification_code: str


class AccountUpdateIn(Schema):
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    address1: str = None
    address2: str = None
    company_name: str = None
    company_website: str = None


class AccountSigninOut(Schema):
    profile: AccountOut
    token: Token


class AccountSigninIn(Schema):
    email: EmailStr
    password: str


class PasswordChangeIn(Schema):
    old_password: str
    new_password1: str
    new_password2: str
