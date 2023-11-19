from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Contact
from django.core.mail import send_mail


class ContactCreateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        phone = data["phone"]
        budget = data["budget"]

        try:
            send_mail(
                subject,
                "New Client Request: "
                + "\n\nName: "
                + name
                + "\nEmail: "
                + email
                + "\n\nMessage:\n"
                + message
                + "\nPhone: "
                + phone
                + "\n\nBudget: "
                + budget,
                "nico.weibel09@gmail.com",
                ["nico.weibel09@gmail.com"],
                fail_silently=False,
            )

            Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
                budget=budget,
            )

            return Response({"success": "Message sent successfully"})
        except:
            return Response({"error": "Message not sent"})
