from django.shortcuts import render
from django.http import Http404

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Contact
from .serializers import ContactSerializer


class BaseAPIView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_contact(self, id=None, email_address=None, name=None):
        try:
            if id is not None:
                return Contact.objects.get(id=id)
            if email_address is not None:
                return Contact.objects.get(email_address=email_address)
            if name is not None:
                return Contact.objects.get(name=name)
            return None
        except Contact.DoesNotExist:
            raise Http404


class ContactAPIView(BaseAPIView):
    def get_contacts(self):
        contacts = Contact.objects.filter()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def get(self, request, id=None):
        """
        Get a single contact
        """
        if id is None:
            return self.get_contacts()

        contact = self.get_contact(id=id)
        serializer = ContactSerializer(contact)

        return Response(serializer.data)

    def post(self, request):
        """
        Save a new contact
        """
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id):
        """
        Update an existing contact
        """
        contact = self.get_contact(id=id)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        Delete an existing contact
        """
        contact = self.get_contact(id=id)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SearchAPIView(BaseAPIView):
    def get(self, request):
        """
        Returns the contact matching the name or the email address
        """
        email_address = request.GET.get('email_address', None)
        name = request.GET.get('name', None)

        if email_address and name:
            return Response('Can\'t search by both email and name', status=status.HTTP_400_BAD_REQUEST)

        if email_address is None and name is None:
            return Response('Pass either email_address or name to find contact',
                status=status.HTTP_400_BAD_REQUEST)

        if email_address:
            contact = self.get_contact(email_address=email_address)

        if name:
            contact = self.get_contact(name=name)

        serializer = ContactSerializer(contact)
        return Response(serializer.data)


