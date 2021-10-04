"""
    Used to import different modules depends on usage
"""
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError # pylint: disable=import-error
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User




class RegisterUserSerializer(serializers.ModelSerializer):

    """
    This serializer is used Register User in db

    Raises:
        serializers.ValidationError: [Validates password]


    """

    password = serializers.CharField(
                                    style = {'input_type':'password'}, write_only = True,
                                    required=True,max_length=68, min_length=6,
                                    validators=[validate_password]
                                    )

    password2 = serializers.CharField(
                                    style = {'input_type':'password'},
                                    write_only = True,required=True,
                                    )


    class Meta:  # pylint: disable=too-few-public-methods

        """
        In this model User is used and specific fields needed for registration are mentioned
        """

        model = User
        fields = ['email','username','first_name','last_name','password','password2']


    def validate(self, attrs):

        """
        This function is used to validate passwords if they are same or not
        and then return the data
        """

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


    def create(self, validated_data):

        """
        This Function is used to store the data in db through the provided fields
        """

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

    """
    This serializer is used for login no data is being created in db through
    this serializer only the pervious data is being validated
    """


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

        """
        This serializer is used to get the generated token for the user
        """

        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }


    def validate(self, attrs):

        """
        This function is used to validate data credentials of user if it
        is present in db and returns a jwt token with it
        """

        email = attrs.get("email", None)
        password = attrs.get("password", None)
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

    """
    This serializer is used to for user when he/she logouts
    """

    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):

        """
        This function validates the refresh token
        """

        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        """
        This function adds the refreshed token in blacklist when user logouts
        """

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
