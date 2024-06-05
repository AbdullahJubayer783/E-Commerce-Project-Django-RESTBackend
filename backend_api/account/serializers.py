from rest_framework import serializers
from .models import User
from xml.dom import ValidationErr
from django.utils.encoding import smart_str , force_bytes , DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode ,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.tokens import RefreshToken , TokenError


class UserRegistrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields=['email','name','password','password2','tc',]
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password doesnt match')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']

class UserChangePasswordSerializers(serializers.Serializer):
    password = serializers.CharField(max_length = 250,style = {'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length = 250,style = {'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password doesnt match')
        user = self.context.get('user')
        user.set_password(password)
        user.save()
        return attrs
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://127.0.0.1:8000/auth/users/reset-password/'+uid+'/'+token+'/'
            link = 'http://127.0.0.1:5500/resetpass.html?uid='+uid+'&'+'token='+token+'/'
            print('Encoded UID ',uid,'Token ',token,'Pass Reset link',link)
            email_subject = "Confirm email"
            email_body = render_to_string('reset_email.html',{'link':link})
            email = EmailMultiAlternatives(email_subject,'',to=[email])
            email.attach_alternative(email_body,"text/html")
            email.send()
            return attrs
        else :
            raise serializers.ValidationError('This email has not register..!')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 250,style = {'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length = 250,style = {'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            if password != password2:
                raise serializers.ValidationError('Password and Confirm Password doesnt match')
            uid = self.context.get('uid')
            token = self.context.get('token')
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            print(user)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError('Token is not valid or Expired')
            else:    
                user.set_password(password)
                user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError('Token is not valid or Expired')
        

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token':('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')



