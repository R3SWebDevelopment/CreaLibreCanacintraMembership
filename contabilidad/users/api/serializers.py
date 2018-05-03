from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from django.contrib.auth.models import User
from customer.models import Company
from users.models import Profile
from avatar.models import Avatar
from customer.utils import validate_rfc
from customer.api.serializers import CompanySerializer
from utils.api.serializers import CommentSerializer


class RegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    country_phone_code = serializers.CharField(required=False, write_only=True, max_length=4)
    mobile_number = serializers.CharField(required=False, write_only=True, max_length=10)
    username = serializers.HiddenField(default="SAME")
    rfc = serializers.CharField(required=True, write_only=True, max_length=13)
    business_name = serializers.CharField(required=True, write_only=True, max_length=250)

    class Meta:
        model = User
        fields = '__all__'

    def validate_rfc(self, value):
        if not validate_rfc(value):
            raise serializers.ValidationError("El RFC no tiene el formato adecuado")
        return value

    def save(self, request, *args, **kwargs):
        user = super(RegistrationSerializer, self).save(request)
        cleaned_data = self.get_cleaned_data()
        mobile_number = {
            "country_code": "",
            "number": ""
        }
        profile = Profile.objects.create(user=user, mobile_number=mobile_number, notify_by_email=True,
                                         notify_by_sms=True)
        user.first_name = cleaned_data.get('first_name', '')
        user.last_name = cleaned_data.get('last_name', '')
        user.save()
        rfc = cleaned_data.get('rfc', '')
        business_name = cleaned_data.get('business_name', '')
        company, created = Company.objects.get_or_create(rfc=rfc)
        company.full_name = business_name
        company.save()
        company.collaborators.add(user)
        return user

    def get_cleaned_data(self):
        cleaned_data = super(RegistrationSerializer, self).get_cleaned_data()
        cleaned_data.update({
            "username": cleaned_data.get('email', ''),
            "first_name": self.validated_data.get('first_name', ''),
            "last_name": self.validated_data.get('last_name', ''),
            "country_phone_code": self.validated_data.get('country_phone_code', ''),
            "mobile_number": self.validated_data.get('mobile_number', ''),
            "business_name": self.validated_data.get('business_name', ''),
            "rfc": self.validated_data.get('rfc', ''),
        })
        return cleaned_data


class LogInSerializer(LoginSerializer):
    username = serializers.HiddenField(default="")

    def validate(self, attrs):
        attrs.update({
            'username': attrs.get('email', ''),
        })
        return super(LogInSerializer, self).validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    mobile_number = serializers.JSONField(default={'number': '', 'country_code': ''})
    is_admin = serializers.BooleanField(read_only=True)
    has_company = serializers.BooleanField(read_only=True)
    company = CompanySerializer(read_only=True, source='my_company')
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ('mobile_number', 'notify_by_email', 'notify_by_sms', 'is_admin', 'has_company', 'company', 'comments')


class AvatarSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Avatar
        fields = ('url', )

    def get_url(self, obj):
        return obj.get_absolute_url()


class UserSerializer(UserDetailsSerializer):
    profile = ProfileSerializer(required=False)
    avatars = AvatarSerializer(many=True, read_only=True, source='avatar_set')
    avatar = serializers.FileField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name', 'profile', 'avatars', 'avatar')
        read_only_fields = ('email', )

    def update(self, instance, validated_data):
        profile_validated_data = validated_data.pop('profile', {})
        avatar_image = validated_data.get('avatar', None)

        instance = super(UserSerializer, self).update(instance, validated_data)
        try:
            profile = instance.profile
        except:
            profile = Profile.objects.create(user=instance)
        profile_serializer = ProfileSerializer(instance=profile, data=profile_validated_data)
        if profile_serializer.is_valid(raise_exception=False):
            profile_serializer.save()

        if avatar_image:
            avatar = Avatar(user=instance, primary=True)
            avatar.avatar.save(avatar_image.name, avatar_image)
            avatar.save()

        return instance

