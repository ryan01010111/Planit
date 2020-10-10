from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from django_rest_passwordreset.signals import reset_password_token_created
from materials.models import LessonPlan

# set free lesson plan
free_lesson_plan = LessonPlan.objects.get(pk=9)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.purchased_plans.add(free_lesson_plan)
        user.save
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class PurchasedMaterialsAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        user = self.request.user
        purchased_materials = list(
            user.purchased_plans.all().values_list("pk", flat=True))

        return Response({"purchased": purchased_materials})


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    user_email = reset_password_token.user.email

    context = {
        'username': reset_password_token.user.username,
        'url': "http://localhost:8000/password_reset/?token={}".format(reset_password_token.key)
    }

    email_plaintext = render_to_string('accounts/password_reset.txt', context)
    email_html = render_to_string('accounts/password_reset.html', context)

    msg = EmailMultiAlternatives(
        'Request for Password Reset',  # subject
        email_plaintext,  # msg
        'notifications@example.com',  # from email
        [user_email],  # to email (list)
    )
    msg.attach_alternative(email_html, 'text/html')
    msg.send()
