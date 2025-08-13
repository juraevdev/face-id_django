from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken


from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from accounts.utils import encode_face, verify_face


class RegisterView(generics.GenericAPIView):
    serializer_class = CustomUserSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        face_image = request.data.get('face_image')

        if not (username and email and face_image):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        face_encoding = encode_face(face_image)
        if face_encoding is None:
            return Response({"error": "No face detected."}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "User already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create(
            username=username,
            email=email,
            face_encoding=face_encoding.tolist()
        )
        serializer = CustomUserSerializer(user)
        return Response({"message": "User registered successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = CustomUserSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        face_image = request.data.get('face_image')
        email = request.data.get('email')

        if not face_image:
            return Response({"error": "Face image is required."}, status=status.HTTP_400_BAD_REQUEST)

        face_encoding = encode_face(face_image)
        if face_encoding is None:
            return Response({"error": "No face detected."}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


        if verify_face(face_image, user.face_encoding):
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Face not recognized."}, status=status.HTTP_401_UNAUTHORIZED)


class DeleteUserView(generics.GenericAPIView):
    def delete(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
