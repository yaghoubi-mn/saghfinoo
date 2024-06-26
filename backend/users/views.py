import random
import datetime

from django.conf import settings
from django.core.cache import caches
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema

from common.codes import users_codes
from .serializers import VerifyNumberSerializer, SignupSerializer, CustomTokenObtainPairSerializer
from .models import CustomUser
from .doc import verify_number_schema_responses

NUMBER_WAIT_TIME = datetime.timedelta(0, 30)
auth_cache = caches['auth']

@swagger_auto_schema(methods=["POST"], query_serializer=VerifyNumberSerializer, responses=verify_number_schema_responses, operation_description="", )
@api_view(['POST'])
def verify_number(req):

    # if req.method == "POST":
    serializer = VerifyNumberSerializer(data=req.data)
    if serializer.is_valid():
        number = serializer.data['number']
        if serializer.data.get('code') == 0:
            # send code to number
        
            now = datetime.datetime.now()
            # delay for send code to a number
            t = auth_cache.get(number, {}).get('delay', now)
            if t > now and not settings.TESTING:
                return Response({"errors":{'number':f"wait {round((t - now).total_seconds())} seconds"}, "code": users_codes.NUMBER_DELAY, "status":400})
            
            code = random.randint(10000, 99999)
            # todo: send code
            if settings.DEBUG and not settings.TESTING:
                print("code:", code)
            token = str(random.randint(10000000, 9999999999)) + random.choice(['fdf', 'dfad', 'ajifd', 'eiurei']) # random_token()

            auth_cache.set(number, {"delay":now+NUMBER_WAIT_TIME, "token":token, "code":code, "tries":0,})
            
            return Response({"msg":"code sent to number", "code":users_codes.CODE_SENT_TO_NUMBER, "token":token, "status":200}, headers={"test":True})
        else:
            # check code
            info = auth_cache.get(number, {})
            if info.get('tries', 0) > 5:
                return Response({"errors":{'code':"to manay tries"}, "code":users_codes.TO_MANNY_TRIES, "status":400})
            
            if info.get('token', '') == '' or info.get('token', '') != serializer.data['token']:
                return Response({"errors":{'code':"zero the code first"}, "code":users_codes.ZERO_CODE_FIRST, "status":400})

            if serializer.data.get('code') == info.get('code', 0):
                # sign in or go sign up
                
                auth_cache.delete(number)

                user = CustomUser.objects.filter(number=number)

                if len(user) == 0:
                    # signup
                    # user not exist go to signup
                    
                    auth_cache.set(number, {'token':serializer.data['token'],'must signup':True})

                    return Response({"msg":"Auth done. Go to /api/v1/complete-signup", "code":users_codes.COMPLETE_SIGNUP, "status":303})
                else:
                    # login
                    
                    # password = CustomUser.objects.first(number=serializer.data['number']).password
                    user = user[0]
                    refresh, access = get_jwt_tokens_for_user(user)
    
                    return Response({"msg":"You are in!", 'access':access, 'refresh':refresh, 'expire': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(), "code":users_codes.LOGIN_DONE, "status":200})
            else:
                # wrong code
                info['tries'] = info.get('tries', 0) + 1
                auth_cache.set(number, info)
                return Response({"errors":{'code':"wrong code"}, "code":users_codes.WRONG_CODE, "status":400})                
            
        
    return Response({"errors":serializer.errors, "code":users_codes.INVALID_FIELD, "status":400})


@swagger_auto_schema(methods=["POST"], query_serializer=SignupSerializer)
@api_view(['POST'])
def signup(req):
    # check number is verified before

    # check is user created before
    
    serializer = SignupSerializer(data=req.data)
    if serializer.is_valid():
        
        info = auth_cache.get(serializer.data['number'], {})

        if not info.get('must signup', False):
            return Response({"errors":{'number':"verifiy number first"}, "code":users_codes.VERIFY_NUMBER_FIRST, "status":400})

        user = CustomUser.objects.filter(number=serializer.data['number'])
        if len(user) > 0:
            return Response({"errors":{'number':"user already created"}, "code":users_codes.USER_EXIST, "status":400})

        user = CustomUser()
        user.first_name = serializer.data['first_name']
        user.last_name = serializer.data['last_name']
        user.number = serializer.data['number']
        user.set_password(serializer.data['password'])
        user.save()

        refresh, access = get_jwt_tokens_for_user(user)
        
        return Response({"msg":"done", "access":access, 'refresh':refresh, 'expire': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(), "code":users_codes.LOGIN_DONE, "status":201})
    return Response({"errors":serializer.errors, "code":users_codes.INVALID_FIELD, "status":400})


def get_jwt_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return str(refresh), str(refresh.access_token)


# @api_view(['POST'])
# def login(req):
#     serializer = SigninSerializer(data=req.data)
#     if serializer.is_valid():
#         user = authenticate(username=serializer.data['number'], password=serializer.data['password'])

#         if user:
#             token, created = Token.objects.get_or_create(user=user)

#             return Response({"msg":"You are in!", "token":token.key, "code":users_codes.LOGIN_DONE, "status":200})
#         else:
#             return Response({"error":"incurrect number or password", "code":users_codes.INCURRECT_NUMBER_OR_PASSWORD, "status":400})
#     return Response({"errors":serializer.errors, "code":users_codes.INVALID_FIELD, "status":400})


@api_view(["GET"])
@permission_classes([IsAuthenticated, ])
@authentication_classes([JWTAuthentication])
def am_i_in(req):
    return Response({"msg":"You are in!", "status":200})


# @api_view(["POST"])
# @permission_classes((IsAuthenticated,))
# def logout(req):
#     req.user.auth_token.delete()
#     return Response({"msg":"done!", "status":200})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_user_info(req):
    return Response({"first_name":req.user.first_name, "last_name":req.user.last_name, "number":req.user.number, "status":200})


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        resp = super().post(request, *args, **kwargs)
        resp.data['status'] = resp.status_code
        resp.status_code = 200
        resp.data['expire'] = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
        return resp

        

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        resp = super().post(request, *args, **kwargs)
        resp.data['status'] = resp.status_code
        resp.status_code = 200
        resp.data['expire'] = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
        return resp