from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import UserProfile, CHOICE_LEVEL, NoteInfo


class UserDetailSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'mobile', 'backup_m', 'work', 'group', 'add_time', ]


class UserInfoPostSerializer(serializers.Serializer):
    JSCODE = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(write_only=True, required=True)
    work = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    mobile = serializers.CharField(write_only=True, required=True, validators=[
        UniqueValidator(queryset=UserProfile.objects.all(), message='手机号不能重复')
    ], max_length=11, min_length=10)
    backup_m = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    group = serializers.ChoiceField(choices=CHOICE_LEVEL, label='类型', required=True)

    # class Meta:
    #     model = UserProfile
    #     fields = ['JSCODE', 'username', 'add_time', 'mobile', 'backup_m', 'group', 'work']


class UserDetailPutSerializer(serializers.Serializer):
    name = serializers.CharField(write_only=True, required=False)
    work = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    mobile = serializers.CharField(write_only=True, required=False, validators=[
        UniqueValidator(queryset=UserProfile.objects.all(), message='手机号不能重复')
    ], max_length=11, min_length=10)
    backup_m = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    group = serializers.ChoiceField(choices=CHOICE_LEVEL, label='类型', required=False)

    # def validate_name(self, data):
    #     return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        # instance.username = validated_data.get('name', instance.username)
        instance.work = validated_data.get('work', instance.work)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.backup_m = validated_data.get('backup_m', instance.backup_m)
        instance.group = validated_data.get('group', instance.group)
        instance.save()
        return instance

    class Meta:
        model = UserProfile
        fields = ['name', 'mobile', 'work', 'backup_m', 'group']

class NoteInfoSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = NoteInfo
        fields = '__all__'

class FeedBackInfoSerializer(serializers.Serializer):
    content=serializers.CharField(required=True,label='提交内容')