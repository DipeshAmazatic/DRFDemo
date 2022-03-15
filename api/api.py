# from rest_framework import viewsets, permissions, generics, status
# from .serializers import LoginSerializer
# from rest_framework.response import Response
# from knox.models import AuthToken
# from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ChangePasswordSerializer
# from .models import CustomUser
# from django.contrib.auth.hashers import make_password

# class LeadViewset(viewsets.ModelViewSet):
#     serializer_class = LoginSerializer
#     permission_classes = [
#         permissions.IsAuthenticated
#     ]

#     def get_queryset(self):
#         return self.request.user.leads.all()
    
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class SignUpAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         user.password = make_password(user.password)
#         user.save()
#         token = AuthToken.objects.create(user)
#         return Response({
#             "users": UserSerializer(user, context=self.get_serializer_context()).data,
#             "token": token[1]
#         })


# class SignInAPI(generics.GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         return Response({
#             "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             "token": AuthToken.objects.create(user)[1]
#         })


# class MainUser(generics.RetrieveAPIView):
#     permission_classes = [
#         permissions.IsAuthenticated
#     ]
#     serializer_class = UserSerializer

#     def get_object(self):
#         return self.request.user

# class ChangePasswordView(generics.UpdateAPIView):
#         """
#         An endpoint for changing password.
#         """
#         serializer_class = ChangePasswordSerializer
#         model = CustomUser
#         permission_classes = [
#             permissions.IsAuthenticated
#         ]

#         def get_object(self, queryset=None):
#             obj = self.request.user
#             return obj

#         def update(self, request, *args, **kwargs):
#             self.object = self.get_object()
#             serializer = self.get_serializer(data=request.data)
#             if serializer.is_valid():
#                 # Check old password
#                 if not self.object.check_password(serializer.data.get("old_password")):
#                     return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#                 self.object.set_password(serializer.data.get("new_password"))
#                 self.object.save()
#                 response = {
#                     'status': 'success',
#                     'code': status.HTTP_200_OK,
#                     'message': 'Password updated successfully',
#                     'data': []
#                 }

#                 return Response(response)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)