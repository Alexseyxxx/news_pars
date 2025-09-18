from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ActivationSerializer
from .models import User, ActivationCode


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

class ActivateView(generics.GenericAPIView):
    serializer_class = ActivationSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"]
        code = ser.validated_data["code"]
        try:
            user = User.objects.get(email=email)
            act = user.activation
            if act.code == code:
                user.is_active = True
                user.save()
                act.delete()
                return Response({"detail": "Account activated"}, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except ActivationCode.DoesNotExist:
            return Response({"detail": "Activation code not found"}, status=status.HTTP_404_NOT_FOUND)
