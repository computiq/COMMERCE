from ninja import Router
from http import HTTPStatus
from django.contrib.auth import authenticate
from config.utils.permissions import create_token, AuthBearer
from config.utils.schemas import MessageOut
from config.utils.utils import response
from .models import EmailAccount
from .schemas import AccountSignupOut, AccountSignupIn, AccountSigninOut, \
    AccountSigninIn, AccountOut, AccountUpdateIn, PasswordChangeIn
from django.shortcuts import get_object_or_404

auth_controller = Router(tags=['auth'])


@auth_controller.post('/register', auth = None, response={200: AccountSignupOut, 403: MessageOut, 500: MessageOut})
def register(request, payload: AccountSignupIn):
    if payload.password1 != payload.password2:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'Passwords does not match!'})

    try:
        EmailAccount.objects.get(email=payload.email)
        return response(403,
                        {'message': 'Forbidden, email is already registered'})
    except EmailAccount.DoesNotExist:
        user = EmailAccount.objects.create_user(first_name=payload.first_name, last_name=payload.last_name,
                                                email=payload.email, password=payload.password1)
        if user:
            token = create_token(user.id)
            return response(HTTPStatus.OK, {
                'profile': user,
                'token': token
            })
        else:
            return response(HTTPStatus.INTERNAL_SERVER_ERROR, {'message': 'An error occurred, please try again.'})


@auth_controller.post('/login', auth = None, response={200: AccountSigninOut, 404: MessageOut})
def login(request, payload: AccountSigninIn):
    user = authenticate(email=payload.email, password=payload.password)
    if user is not None:
        return response(HTTPStatus.OK, {
            'profile': user,
            'token': create_token(user.id)
        })
    return response(HTTPStatus.NOT_FOUND, {'message': 'User not found'})


@auth_controller.get('/me',
                     auth=AuthBearer(),
                     response={200: AccountOut, 400: MessageOut})
def me(request):
    try:
        user = get_object_or_404(EmailAccount, id=request.auth.id)
    except:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'token missing'})
    return response(HTTPStatus.OK, user)


@auth_controller.put('/me',
                     auth=AuthBearer(),
                     response={200: AccountOut, 400: MessageOut})
def update_me(request, user_in: AccountUpdateIn):
    EmailAccount.objects.filter(id=request.auth.id).update(**user_in.dict())
    user = get_object_or_404(EmailAccount, id=request.auth.id)
    if not user:
        return response(HTTPStatus.BAD_REQUEST, data={'message': 'something went wrong'})
    return response(HTTPStatus.OK, user)


@auth_controller.post('/change-password',
                      auth=AuthBearer(),
                      response={200: MessageOut, 400: MessageOut})
def change_password(request, payload: PasswordChangeIn):
    if payload.new_password1 != payload.new_password2:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'Passwords do not match!'})

    try:
        user = get_object_or_404(EmailAccount, id=request.auth.id)
    except:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'token missing'})

    user_update = authenticate(email=user.email, password=payload.old_password)

    if user_update is not None:
        user_update.set_password(payload.new_password1)
        user_update.save()
        return response(HTTPStatus.OK, {'message': 'password updated'})

    return response(HTTPStatus.BAD_REQUEST, {'message': 'something went wrong, please try again later'})
