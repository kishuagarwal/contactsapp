import base64

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status, HTTP_HEADER_ENCODING
from rest_framework.test import APITestCase

from .models import Contact

class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.username = 'kishu'
        self.password = 'plivo'
        User.objects.create_user(username=self.username, password=self.password)

    def get_dummy_contact(self):
        contact = {
          "name" : "Test User",
          "number": "332253533",
          "email_address": "test@plivo.com"
        }
        return contact

    def get_auth(self):
        credentials = ('%s:%s' % (self.username, self.password))
        base64_credentials = base64.b64encode(
            credentials.encode(HTTP_HEADER_ENCODING)
        ).decode(HTTP_HEADER_ENCODING)
        auth = 'Basic %s' % base64_credentials
        return auth


class ContactTests(BaseAPITestCase):
    def test_create_contact(self):
        """
        Ensure we can create a new contact.
        """
        
        url = reverse('contact-list')
        contact = self.get_dummy_contact()

        response = self.client.post(url, contact,
          format='json',
          HTTP_AUTHORIZATION=self.get_auth())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().email_address, contact['email_address'])

    def test_get_contact(self):
        contact = self.get_dummy_contact()
        contact = Contact(**contact)
        contact.save()
        url = reverse('contact', kwargs={'id': contact.id})

        response = self.client.get(url,
          format='json',
          HTTP_AUTHORIZATION=self.get_auth())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], contact.id)

    def test_update_contact(self):
        contact = self.get_dummy_contact()
        contact_obj = Contact(**contact)
        contact_obj.save()
        url = reverse('contact', kwargs={'id': contact_obj.id})
  
        updated_contact = contact
        updated_contact['name'] = 'Updated name'

        response = self.client.put(url,
          updated_contact,
          format='json',
          HTTP_AUTHORIZATION=self.get_auth())
        contact_obj.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_contact['name'])
        self.assertEqual(contact_obj.name, updated_contact['name'])

    def test_delete_contact(self):
        contact = self.get_dummy_contact()
        contact_obj = Contact(**contact)
        contact_obj.save()
        url = reverse('contact', kwargs={'id': contact_obj.id})
        
        response = self.client.delete(url,
          format='json',
          HTTP_AUTHORIZATION=self.get_auth())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.filter().count(), 0)


class SearchTests(BaseAPITestCase):
    def test_search_by_name(self):
        url = reverse('search-contact')
        contact = self.get_dummy_contact()
        contact_obj = Contact(**contact)
        contact_obj.save()

        response = self.client.get(url,
          { 'name': contact_obj.name },
          format='json',
          HTTP_AUTHORIZATION=self.get_auth())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], contact_obj.name)

    def test_search_by_email(self):
        url = reverse('search-contact')
        contact = self.get_dummy_contact()
        contact_obj = Contact(**contact)
        contact_obj.save()

        response = self.client.get(url,
          { 'email_address': contact_obj.email_address },
          format='json',
          HTTP_AUTHORIZATION=self.get_auth())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email_address'], contact_obj.email_address)

    def test_non_existence(self):
        url = reverse('search-contact')

        response = self.client.get(url,
          { 'email_address': 'dummy@plivo.com' },
          format='json',
          HTTP_AUTHORIZATION=self.get_auth())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_request(self):
        url = reverse('search-contact')
        response = self.client.get(url,
          { 'email_address': 'dummy@plivo.com',
            'name': 'dummy'
          },
          format='json',
          HTTP_AUTHORIZATION=self.get_auth())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(url,
          format='json',
          HTTP_AUTHORIZATION=self.get_auth())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
