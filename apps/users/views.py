from functools import partial
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from users.models import UserProfile, NoteInfo, FeedBackInfo
from users.serializers import UserDetailSerializer, UserInfoPostSerializer, UserDetailPutSerializer, NoteInfoSerializer, \
    FeedBackInfoSerializer
from utils.make_openid import make_openid


class UserInfoViewset(mixins.ListModelMixin, viewsets.GenericViewSet,
                      mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = UserProfile.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserInfoPostSerializer
        elif self.action == 'update':
            return UserDetailPutSerializer
        return UserDetailSerializer

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        resp = {}
        JSCODE = request.GET.get('JSCODE', None)
        name = request.GET.get('name', None)
        # if not JSCODE:
        #     code = 400
        #     resp['msg'] = 'JSCODE不可为空'
        #     return Response(data=resp, status=code)
        # dict_result = make_openid(JSCODE)
        # if dict_result.get('errmsg'):
        #     code = 400
        #     resp['msg'] = '创建失败'
        #     return Response(data=resp, status=code)
        # openid = dict_result.get('openid')
        # if not openid:
        #     code = 400
        #     resp['msg'] = 'openid获取失败'
        #     return Response(data=resp, status=code)
        # yesno = UserProfile.objects.filter(openid=openid).first()
        # if not yesno:
        #     code = 400
        #     resp['msg'] = '用户未注册'
        #     return Response(data=resp, status=code)
        # if not yesno.is_active:
        #     code = 202
        #     resp['msg'] = '用户未审核'
        #     return Response(data=resp, status=code)
        code = 200
        if name:
            all_user = UserProfile.objects.filter(is_active=True, is_superuser=False, name__icontains=name).order_by(
                '-add_time')
        else:
            all_user = UserProfile.objects.filter(is_active=True, is_superuser=False).order_by('-add_time')
        serializer = self.get_serializer(all_user, many=True)
        return Response(data=serializer.data, status=code)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        resp = {}
        JSCODE = validated_data.get('JSCODE')
        dict_result = make_openid(JSCODE)
        if dict_result.get('errmsg'):
            code = 400
            resp['msg'] = '创建失败'
            return Response(data=resp, status=code)
        openid = dict_result.get('openid')
        if not openid:
            code = 400
            resp['msg'] = 'openid获取失败'
            return Response(data=resp, status=code)
        user_q = UserProfile.objects.filter(openid=openid)
        if user_q.exists():
            code = 202
            resp['msg'] = '此微信号已绑定一条记录'
            return Response(data=resp, status=code)
        del validated_data['JSCODE']
        validated_data['openid'] = openid
        validated_data['username'] = openid
        # validated_data['is_active'] = False
        user = UserProfile.objects.create(**validated_data)
        # payload = jwt_payload_handler(user)
        # token = jwt_encode_handler(payload)
        code = 200
        resp['msg'] = '创建成功'
        # resp['token'] = token
        return Response(data=resp, status=code)

    def update(self, request, *args, **kwargs):
        print('request', request.data)
        resp = {}
        JSCODE = request.data.get('JSCODE', None)
        if not JSCODE:
            code = 400
            resp['msg'] = 'JSCODE不可为空'
            return Response(data=resp, status=code)
        dict_result = make_openid(JSCODE)
        if dict_result.get('errmsg'):
            code = 400
            resp['msg'] = '创建失败'
            return Response(data=resp, status=code)
        openid = dict_result.get('openid')
        if not openid:
            code = 400
            resp['msg'] = 'openid获取失败'
            return Response(data=resp, status=code)
        yesno = UserProfile.objects.filter(is_active=True, openid=openid).first()
        if not yesno:
            code = 400
            resp['msg'] = '用户未绑定'
            return Response(data=resp, status=code)
        serializer = self.get_serializer(yesno, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        code = 200
        resp['msg'] = '修改成功'
        return Response(data=resp, status=code)

    def retrieve(self, request, *args, **kwargs):
        resp = {}
        JSCODE = request.GET.get('JSCODE', None)
        if not JSCODE:
            code = 400
            resp['msg'] = 'JSCODE不可为空'
            return Response(data=resp, status=code)
        dict_result = make_openid(JSCODE)
        if dict_result.get('errmsg'):
            code = 400
            resp['msg'] = '创建失败'
            return Response(data=resp, status=code)
        openid = dict_result.get('openid')
        if not openid:
            code = 400
            resp['msg'] = 'openid获取失败'
            return Response(data=resp, status=code)
        yesno = UserProfile.objects.filter(is_active=True, openid=openid).first()
        if not yesno:
            code = 400
            resp['msg'] = '用户未绑定'
            return Response(data=resp, status=code)
        code = 200
        data = UserDetailSerializer(yesno).data
        return Response(data=data, status=code)


class NoteInfoViewset(mixins.ListModelMixin, viewsets.GenericViewSet, ):
    serializer_class = NoteInfoSerializer

    def get_queryset(self):
        a = NoteInfo.objects.all().order_by('-add_time')
        return a[0:1] if a else []


class FeedBackInfoViewset(mixins.CreateModelMixin, viewsets.GenericViewSet, ):
    serializer_class = FeedBackInfoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resp = {}
        JSCODE = request.data.get('JSCODE', None)
        if not JSCODE:
            code = 400
            resp['msg'] = 'JSCODE不可为空'
            return Response(data=resp, status=code)
        dict_result = make_openid(JSCODE)
        if dict_result.get('errmsg'):
            code = 400
            resp['msg'] = '创建失败'
            return Response(data=resp, status=code)
        openid = dict_result.get('openid')
        if not openid:
            code = 400
            resp['msg'] = 'openid获取失败'
            return Response(data=resp, status=code)
        yesno = UserProfile.objects.filter(openid=openid).first()
        if not yesno:
            code = 400
            resp['msg'] = '用户未注册'
            return Response(data=resp, status=code)
        if not yesno.is_active:
            code = 202
            resp['msg'] = '用户未审核'
            return Response(data=resp, status=code)
        validated_data = serializer.validated_data
        validated_data['user']=yesno
        FeedBackInfo.objects.create(**validated_data)
        code = 200
        resp['msg'] = '反馈成功'
        return Response(data=resp, status=code)
