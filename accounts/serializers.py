from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
                                    style = {'input_type':'password'}, write_only = True,
                                    required=True,max_length=68, min_length=6,
                                    validators=[validate_password]
                                    )

    password2 = serializers.CharField(
                                    style = {'input_type':'password'},
                                    write_only = True,required=True,
                                    )

    class Meta:

        model = User
        fields = ['email','username','first_name','last_name','password','password2']


    def validate(self, attrs):

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):

        user = User.objects.create(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data ['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user




class LoginSerializer(serializers.Serializer):


    email = serializers.EmailField(max_length=255, min_length=3)

    password = serializers.CharField(
        style = {'input_type':'password'},
        write_only=True
        )

    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True
        )

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)


        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )

        return {
            'email':user.email,
            'tokens': user.tokens
        }

class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, data):

        self.token = data['refresh']
        return data

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')