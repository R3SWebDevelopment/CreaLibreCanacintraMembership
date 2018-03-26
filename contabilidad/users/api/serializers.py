from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from django.contrib.auth.models import User
from users.models import Profile
from avatar.models import Avatar


class RegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    country_phone_code = serializers.CharField(required=True, write_only=True, max_length=4)
    mobile_number = serializers.CharField(required=True, write_only=True, max_length=10)
    username = serializers.HiddenField(default="SAME")

    class Meta:
        model = User
        fields = '__all__'

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
        return user

    def get_cleaned_data(self):
        cleaned_data = super(RegistrationSerializer, self).get_cleaned_data()
        cleaned_data.update({
            "username": cleaned_data.get('email', ''),
            "first_name": self.validated_data.get('first_name', ''),
            "last_name": self.validated_data.get('last_name', ''),
            "country_phone_code": self.validated_data.get('country_phone_code', ''),
            "mobile_number": self.validated_data.get('mobile_number', ''),
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

    class Meta:
        model = Profile
        fields = ('mobile_number', 'notify_by_email', 'notify_by_sms')


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

