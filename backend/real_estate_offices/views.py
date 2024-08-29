import math
import uuid

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from PIL import Image
from django.core.files.storage import default_storage
from django.conf import settings

from common.utils.permissions import IsRealEstateOfficeOwner, IsAdmin, IsRealtor, IsOwner
from common.utils.request import get_page_and_limit
from common.utils.database import formated_datetime_now, ScoreManager
from common import codes
from common.utils import validations
from django.db.models import Q

from .serializers import RealEstateOfficeSerializer, RealEstateOfficePreviewResponseSerializer, RealEstateOfficeResponseSerializer, CommentResponseSerializer, CommentSerializer, CommentScoreReasonResponseSerializer, ReportReasonResponseSerializer, ReportSerializer
from .models import RealEstateOffice, Comment, CommentScoreReason, ReportReason



class CreateRealEstateOfficeAPIView(APIView):
    """after create, real estate office must be confirmed by admin"""

    serializer_class = RealEstateOfficeSerializer
    permission_classes = [IsAuthenticated, IsRealtor]
    authentication_classes = [JWTAuthentication]

    def post(self, req):
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid():
            try:
                reo = RealEstateOffice.objects.get(owner=req.user)
                return Response({'errors':{"user":"user is already owner of "+reo.name}, 'code':codes.USER_IS_ALREADY_REO_OWNER, 'status':400})
            except RealEstateOffice.DoesNotExist:
                reo = serializer.save(owner=req.realtor.user)
                return Response({"msg": "done", 'status':200, 'id': reo.id})
        return Response({"errors": serializer.errors, 'code':codes.INVALID_FIELD, 'status':400})
    
class EditRealEstateOfficeAPIView(APIView):

    serializer_class = RealEstateOfficeSerializer
    permission_classes = [IsAuthenticated, (IsRealEstateOfficeOwner| IsAdmin)]
    authentication_classes = [JWTAuthentication]

    def put(self, req, real_estate_office_id):
        try:
            reo = RealEstateOffice.objects.get(id=real_estate_office_id)
        except RealEstateOffice.DoesNotExist:
            return Response({'errors':{'non-field-error':'real estate office not found'}, 'status':404})
        self.check_object_permissions(req, reo)
        
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid():
            serializer.save(id=real_estate_office_id)
            return Response({"msg":"done", 'status':200})
        return Response({"errors": serializer.errors, 'code':codes.INVALID_FIELD, 'status':400})

class GetAllRealEstateOfficeAPIView(APIView):

    def get(self, req):
        try:
            page, limit = get_page_and_limit(req)
        except ValueError as e:
            return Response({'errors':e.dict, 'code':codes.INVALID_QUERY_PARAM, 'status':400})
        
        reo = RealEstateOffice.objects.filter(is_confirmed=True).values(*RealEstateOfficePreviewResponseSerializer.Meta.fields)[page*limit:page*limit+limit]
        
        return Response({'data':reo, 'status':200})
    
class GetRealEstateOfficeAPIView(APIView):
    """get real estate office by username"""
    def get(self, req, slug):
        try:
            reo = RealEstateOfficeResponseSerializer(RealEstateOffice.objects.get(is_confirmed=True, username=slug))
            return Response({"data":reo.data, 'status':200})        
        except RealEstateOffice.DoesNotExist:
            return Response({'status':404})
        

class SearchRealEstateOfficesAPIView(APIView):

    def get(self, req):
        """search?city=something1&city=something2"""
        qp = dict(req.query_params)
        try:
            page, limit = get_page_and_limit(req)
        except ValueError as e:
            return Response({'errors':e.dict, 'code':codes.INVALID_QUERY_PARAM, 'status':400})

        query = None
        if qp.get('city', '') != '':
            if type(qp['city']) == list:
                for c in qp['city']:
                    if c == '' or c == '"':
                        continue
                    try:
                        validations.validate_name(c)
                    except ValueError as e:
                        return Response({'errors':{'city':str(e)}, 'status':400, 'code':codes.INVALID_QUERY_PARAM})
                    
                    if query:
                        query |= Q(city=c)
                    else:
                        query = Q(city=c)
            
            
        if query:
            query &= Q(is_confirmed=True)
        else:
            query = Q(is_confirmed=True)

        reo = RealEstateOffice.objects.values(*RealEstateOfficePreviewResponseSerializer.Meta.fields).filter(query)[page*limit: page*limit+limit]
        total_pages = math.ceil(RealEstateOffice.objects.filter(query).count()/limit)
    
        return Response({'data':reo, 'total_pages':total_pages, 'status':200})

        


class UploadRealEstateOfficeImageAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRealEstateOfficeOwner]
    authentication_classes = [JWTAuthentication]
    
    def post(self, req):
        image = req.FILES.get('image', '')
        if image == '':
            return Response({'errors':{'image':'image not sent'}})

        if Image.open(image).format not in ('PNG', 'JPEG'):
            return Response({"errors":{"image":"invalid image format (accepted formats: PNG, JPEG)"}})
        
        try:
            reo = RealEstateOffice.objects.get(owner=req.user)
        except RealEstateOffice.DoesNotExist:
            return Response({'errors':{'user':'user not owner of any real estate office'}, 'code':codes.USER_IS_NOT_REO_OWNER, 'status':404})

        file_ext = image.name.split('.')[-1]
        file_name = f'{uuid.uuid4()}.{file_ext}'

        if reo.image:
            default_storage.delete(reo.image)
        reo.image = default_storage.save(f'real_estate_offices/{file_name}', image, max_length=1*1024*1024)
        reo.image_full_path = f'{settings.S3_ENDPOINT_URL_WITH_BUCKET}/{reo.image}'
        reo.save()

        return Response({"msg":"done", 'status':200})




class UploadRealEstateOfficeBGImageAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRealEstateOfficeOwner]
    authentication_classes = [JWTAuthentication]
    
    def post(self, req):
        image = req.FILES.get('image', '')
        if image == '':
            return Response({'errors':{'image':'image not sent'}})

        if Image.open(image).format not in ('PNG', 'JPEG'):
            return Response({"errors":{"image":"invalid image format (accepted formats: PNG, JPEG)"}})
        
        try:
            reo = RealEstateOffice.objects.get(owner=req.user)
        except RealEstateOffice.DoesNotExist:
            return Response({'errors':{'user':'user not owner of any real estate office'}, 'code':codes.USER_IS_NOT_REO_OWNER, 'status':404})

        file_ext = image.name.split('.')[-1]
        file_name = f'{uuid.uuid4()}.{file_ext}'

        if reo.bg_image:
            default_storage.delete(reo.bg_image)
        reo.bg_image = default_storage.save(f'real_estate_offices/{file_name}', image, max_length=1*1024*1024)
        reo.bg_image_full_path = f'{settings.S3_ENDPOINT_URL_WITH_BUCKET}/{reo.bg_image}'
        reo.save()

        return Response({"msg":"done", 'status':200})



#####################################  comment ################################################

class CreateCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, req, real_estate_office_id):
        serializer = CommentSerializer(data=req.data)
        if serializer.is_valid():
            try:
                reo = RealEstateOffice.objects.get(id=real_estate_office_id)
            except RealEstateOffice.DoesNotExist:
                return Response({'errors':{'non-field-error':'real estate office not found'}, 'status':404})

            comment = serializer.save(owner=req.user, real_estate_office=reo)

            comment.real_estate_office.number_of_comments += 1
            comment.real_estate_office.save()

            ScoreManager.increase_obj_score(comment.score, comment.real_estate_office)
            return Response({'msg':'done', 'status':200})
        
        return Response({'errors':serializer.errors, 'status':400, 'code':codes.INVALID_FIELD})
    
class EditCommentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]

    def put(self, req, comment_id):
        serializer = CommentSerializer(data=req.data)
        if serializer.is_valid():
            try:
                comment = Comment.objects.get(id=comment_id)
            except Comment.DoesNotExist:
                return Response({'errors':{'non-field-error':'comment not found'}, 'status':404}) 

            self.check_object_permissions(req, comment)

            old_score = comment.score

            comment.description = serializer.data['description']
            comment.score = serializer.data['score']
            comment.modified_at = formated_datetime_now()
            comment.save()

            ScoreManager.edit_obj_score(old_score, comment.score, comment.real_estate_office)

            return Response({'msg':'done', 'status':200})
        
        return Response({'errors':serializer.errors, 'status':400, 'code':codes.INVALID_FIELD})
    
class GetAllCommentsAPIView(APIView):

    def get(self, req, real_estate_office_id):
        try:
            page, limit = get_page_and_limit(req, default_limit=16)
        except ValueError as e:
            return Response({'errors': e.dict, 'status':400, 'code':codes.INVALID_QUERY_PARAM})
        
        comments = Comment.objects.filter(real_estate_office=real_estate_office_id).values(*CommentResponseSerializer.Meta.fields).order_by('-created_at')[page*limit:page*limit+limit]
        return Response({'data':comments, 'status':200})
    
class DeleteCommentAPIVew(APIView):
    permission_classes = [IsAuthenticated, IsOwner|IsAdmin]
    authentication_classes = [JWTAuthentication]

    def delete(self, req, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'errors':{'non-field-error':'comment not found'}, 'status':404})
        
        self.check_object_permissions(req, comment)
        comment.delete()

        comment.real_estate_office.number_of_comments -= 1
        comment.real_estate_office.save()

        ScoreManager.decrease_obj_score(comment.score, comment.real_estate_office)

        return Response({'msg':'done', 'status':200})


class GetAllCommentScoreReasonAPIView(APIView):
    
    def get(self, req):
        
        score = req.query_params.get('score', 0)
        try:
            validations.validate_integer(score)
        except ValueError as v:
            return Response({'errors':{'score':str(v)}, 'status':400, 'code':codes.INVALID_QUERY_PARAM})

        if score:
            csrs = CommentScoreReason.objects.filter(score=score).values(*CommentScoreReasonResponseSerializer.Meta.fields)
        else:
            csrs = CommentScoreReason.objects.all().values(*CommentScoreReasonResponseSerializer.Meta.fields)

        return Response({'data':csrs,'status':200})




######################## report ##################################

class CreateReportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, req, real_estate_office_id):
        serializer = ReportSerializer(data=req.data)
        if serializer.is_valid():
            try:
                reo = RealEstateOffice.objects.get(id=real_estate_office_id)
            except RealEstateOffice.DoesNotExist:
                return Response({'errors':{'non-field-error':'real estate office not found'}, 'status':404})
                
            serializer.save(user=req.user, real_estate_office=reo)
            return Response({'msg':'done', 'status':200})
        
        return Response({'errors':serializer.errors, 'status':400, 'code':codes.INVALID_FIELD})
    
class GetAllReportReasonsAPIView(APIView):
    
    def get(self, req):
        reasons = ReportReason.objects.all().values(*ReportReasonResponseSerializer.Meta.fields)
        return Response({'data':reasons, 'status':200})