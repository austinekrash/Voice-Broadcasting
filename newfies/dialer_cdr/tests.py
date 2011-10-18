from django.contrib.auth.models import User
from django.test import TestCase, Client
from dialer_cdr.test_utils import build_test_suite_from
#from user_profile.models import UserProfile
import base64


class BaseAuthenticatedClient(TestCase):
    """Common Authentication"""

    def setUp(self):
        """To create admin user"""
        self.client = Client()
        self.user = \
        User.objects.create_user('admin', 'admin@world.com', 'admin')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.is_active = True
        self.user.save()
        auth = '%s:%s' % ('admin', 'admin')
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()
        self.extra = {
            'HTTP_AUTHORIZATION': auth,
        }
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)


class NewfiesTastypieApiTestCase(BaseAuthenticatedClient):
    """Test cases for Newfies-Dialer API."""
    fixtures = ['gateway.json', 'auth_user', 'voipapp','phonebook', #'contact',
                'campaign', 'campaign_subscriber']

    def test_create_campaign(self):
        """Test Function to create a campaign"""
        response = self.client.post('/api/v1/campaign/',
        {"name": "mycampaign", "description": "", "callerid": "1239876", "startingdate": "1301392136.0", "expirationdate": "1301332136.0", "frequency": "20", "callmaxduration": "50", "maxretry": "3", "intervalretry": "3000", "calltimeout": "45", "aleg_gateway": "1", "voipapp": "1", "extra_data": "2000"},
        **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_read_campaign(self):
        """Test Function to get all campaigns"""
        response = self.client.get('/api/v1/campaign/?format=json',
                   **self.extra)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/campaign/1/?format=json',
                   **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_update_campaign(self):
        """Test Function to update a campaign"""
        response = self.client.put('/api/v1/campaign/1/',
                   {"status": "2"}, **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_delete_campaign(self):
        """Test Function to delete a campaign"""
        response = self.client.delete('/api/v1/campaign/1/',
        **self.extra)
        self.assertEqual(response.status_code, 204)

    def test_delete_cascade_campaign(self):
        """Test Function to cascade delete a campaign"""
        response = \
        self.client.delete('/api/v1/campaign/delete_cascade/1/',
        **self.extra)
        self.assertEqual(response.status_code, 204)

    def test_create_phonebook(self):
        """Test Function to create a phonebook"""
        response = self.client.post('/api/v1/phonebook/',
        {"name": "mylittlephonebook", "description": "Test",
         "campaign_id": "1"}, **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_read_phonebook(self):
        """Test Function to get all phonebooks"""
        response = self.client.get('/api/v1/phonebook/',
        **self.extra)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/phonebook/1/',
        **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_create_bulk_contact(self):
        """Test Function to bulk create contacts"""
        response = self.client.post('/api/v1/bulkcontact/',
        {"phoneno_list": "12345,54344", "phonebook_id": "1"},
        **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_create_campaign_subscriber(self):
        """Test Function to create a campaign subscriber"""
        response = self.client.post('/api/v1/campaignsubscriber/',
        {"contact": "650784355", "last_name": "belaid", "first_name": "areski", "email": "areski@gmail.com", "phonebook_id" : "1"},
        **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_read_campaign_subscriber(self):
        """Test Function to get all campaign subscriber"""
        response = self.client.get('/api/v1/campaignsubscriber/?format=json',
                   **self.extra)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/campaignsubscriber/1/?format=json',
                   **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_update_campaign_subscriber(self):
        """Test Function to update a campaign subscriber"""
        response = self.client.put('/api/v1/campaignsubscriber/1/',
                   {"status": "2", "contact": "123546"}, **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_create_callrequest(self):
        """Test Function to create a callrequest"""
        response = self.client.post('/api/v1/callrequest/',
        {"request_uuid": "2342jtdsf-00153",
         "call_time": "2011-05-01 11:22:33", "phone_number": "8792749823",
         "voipapp": "1", "timeout": "30000", "callerid": "650784355",
         "call_type": "1"}, **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_read_callrequest(self):
        """Test Function to get all callrequests"""
        response = self.client.get('/api/v1/callrequest/?format=json',
        **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_create_answercall(self):
        """Test Function to create a answercall"""
        response = self.client.post('/api/v1/answercall/',
        {"ALegRequestUUID": "48092924-856d-11e0-a586-0147ddac9d3e"}, **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_create_hangupcall(self):
        """Test Function to create a answercall"""
        response = self.client.post('/api/v1/hangupcall/',
        {"ALegRequestUUID": "48092924-856d-11e0-a586-0147ddac9d3e",
         "HangupCause": "SUBSCRIBER_ABSENT"}, **self.extra)
        self.assertEqual(response.status_code, 200)


        
class NewfiesApiTestCase(BaseAuthenticatedClient):
    """Test cases for Newfies-Dialer API."""
    fixtures = ['gateway.json', 'auth_user', 'voipapp','phonebook', 'contact',
                'campaign', 'campaign_subscriber']

    def test_create_campaign(self):
        """Test Function to create a campaign"""
        response = self.client.post('/api/dialer_campaign/campaign/',
        {"name": "mycampaign", "description": "xyz",
         "startingdate": "1301392136.0", "expirationdate": "1301332136.0",
         "frequency": "20", "callmaxduration": "50", "maxretry": "3",
         "intervalretry": "3000", "calltimeout": "60", "aleg_gateway": "1",
         "callerid": "123987", "voipapp": "1",
         "extra_data": "2000"}, **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_read_campaign(self):
        """Test Function to get all campaigns"""
        response = self.client.get('/api/dialer_campaign/campaign/',
                   **self.extra)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/dialer_campaign/campaign/1/',
                   **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_update_campaign(self):
        """Test Function to update a campaign"""
        response = self.client.put('/api/dialer_campaign/campaign/1/',
                   {"status": "2"}, **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_delete_campaign(self):
        """Test Function to delete a campaign"""
        response = self.client.delete('/api/dialer_campaign/campaign/1/',
        **self.extra)
        self.assertEqual(response.status_code, 204)

    def test_delete_cascade_campaign(self):
        """Test Function to cascade delete a campaign"""
        response = \
        self.client.delete('/api/dialer_campaign/campaign/delete_cascade/1/',
        **self.extra)
        self.assertEqual(response.status_code, 204)

    def test_create_phonebook(self):
        """Test Function to create a phonebook"""
        response = self.client.post('/api/dialer_campaign/phonebook/',
        {"name": "mylittlephonebook", "description": "Test",
         "campaign_id": "1"}, **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_read_phonebook(self):
        """Test Function to get all phonebooks"""
        response = self.client.get('/api/dialer_campaign/phonebook/',
        **self.extra)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/dialer_campaign/phonebook/1/',
        **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_create_contact(self):
        """Test Function to create a contact"""
        response = self.client.post('/api/dialer_campaign/contact/',
        {"contact": "650784355", "name": "areski", "phonebook_id": "1"},
        **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_read_contact(self):
        """Test Function to get all pending contacts"""
        response = self.client.get('/api/dialer_campaign/contact/1/',
        **self.extra)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/dialer_campaign/contact/1/1/',
        **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_update_contact(self):
        """Test Function to update a contact"""
        response = self.client.put('/api/dialer_campaign/contact/1/1234/',
                   {"status": "2"}, **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_create_bulk_contact(self):
        """Test Function to bulk create contacts"""
        response = self.client.post('/api/dialer_campaign/bulkcontact/',
        {"phoneno_list": "12345,54344", "phonebook_id": "1"},
        **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_create_callrequest(self):
        """Test Function to create a callrequest"""
        response = self.client.post('/api/dialer_cdr/callrequest/',
        {"request_uuid": "2342jtdsf-00153",
         "call_time": "2011-05-01 11:22:33", "phone_number": "8792749823",
         "voipapp": "1", "timeout": "30000", "callerid": "650784355",
         "call_type": "1"}, **self.extra)
        self.assertEqual(response.status_code, 200)

    def test_read_callrequest(self):
        """Test Function to get all callrequests"""
        response = self.client.get('/api/dialer_cdr/callrequest/',
        **self.extra)
        self.assertEqual(response.status_code, 200)


class NewfiesApiCallRequestUpdateTestCase(BaseAuthenticatedClient):
    """Test cases for updating a Call Request API."""
    fixtures = ['gateway', 'auth_user', 'voipapp', 'phonebook', 'contact',
                'campaign', 'callrequest']

    def test_update_callrequest(self):
        """Test Function to update a callrequest"""
        response = self.client.put('/api/dialer_cdr/callrequest/1/',
                   {"status": "5"}, **self.extra)
        self.assertEqual(response.status_code, 200)


class NewfiesAdminInterfaceTestCase(TestCase):
    """Test cases for Newfies Admin Interface."""

    def setUp(self):
        """To create admin user"""
        self.client = Client()
        self.user = \
        User.objects.create_user('admin', 'admin@world.com', 'admin')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.is_active = True
        self.user.save()
        auth = '%s:%s' % ('admin', 'admin')
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()
        self.extra = {
            'HTTP_AUTHORIZATION': auth,
        }

    def test_admin_index(self):
        """Test Function to check Admin index page"""
        response = self.client.get('/admin/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/base_site.html')
        response = self.client.login(username=self.user.username,
                                     password='admin')
        self.assertEqual(response, True)

    def test_admin_newfies(self):
        """Test Function to check Newfies Admin pages"""
        response = self.client.get('/admin/auth/')
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.get('/admin/dialer_settings/')
        self.failUnlessEqual(response.status_code, 200)
        
        response = self.client.get('/admin/dialer_campaign/')
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get('/admin/dialer_campaign/contact/')
        self.failUnlessEqual(response.status_code, 200)
        response = \
        self.client.get('/admin/dialer_campaign/contact/import_contact/')
        self.failUnlessEqual(response.status_code, 200)
        response = \
        self.client.get('/admin/dialer_campaign/campaignsubscriber/')
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get('/admin/dialer_campaign/campaign/')
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get('/admin/dialer_campaign/phonebook/')
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.get('/admin/dialer_cdr/')
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get('/admin/dialer_cdr/voipcall/')
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get('/admin/dialer_cdr/callrequest/')
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.get('/admin/dialer_gateway/')
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get('/admin/dialer_gateway/gateway/')
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.get('/admin/prefix_country/')
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get('/admin/prefix_country/country/')
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get('/admin/prefix_country/prefix/')
        self.failUnlessEqual(response.status_code, 200)


class NewfiesCustomerInterfaceTestCase(BaseAuthenticatedClient):
    """Test cases for Newfies Customer Interface."""
    fixtures = ['gateway.json', 'auth_user', 'voipapp','phonebook', 'contact',
                'campaign', 'campaign_subscriber']

    def test_index(self):
        """Test Function to check customer index page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/index.html')
        response = self.client.post('/login/',
                    {'username': 'userapi',
                     'password': 'passapi'})
        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        """Test Function to check customer dashboard"""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/dashboard.html')

    def test_voipapp_view(self):
        """Test Function to check voipapp"""
        response = self.client.get('/voipapp/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'frontend/voipapp/list.html')
        response = self.client.get('/voipapp/add/')
        self.assertTemplateUsed(response,
                                'frontend/voipapp/change.html')
        response = self.client.get('/voipapp/1/')
        self.assertEqual(response.status_code, 200)        

    def test_phonebook_view(self):
        """Test Function to check phonebook"""
        response = self.client.get('/phonebook/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'frontend/phonebook/list.html')
        response = self.client.get('/phonebook/add/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/phonebook/add/',
                   data={'name': 'My Phonebook', 'description': 'phonebook',
                         'user': self.user})
        response = self.client.get('/phonebook/1/')        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'frontend/phonebook/change.html')

    def test_contact_view(self):
        """Test Function to check Contact"""
        response = self.client.get('/contact/add/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/contact/add/',
                   data={'phonebook': '1', 'contact': '1234',
                         'last_name': 'xyz', 'first_name': 'abc',
                         'status': '1'})        
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/contact/1/')
        self.assertTemplateUsed(response,
                                'frontend/contact/change.html')
        response = self.client.get('/contact/import/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'frontend/contact/import_contact.html')

    def test_campaign_view(self):
        """Test Function to check phonebook"""
        response = self.client.get('/campaign/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'frontend/campaign/list.html')
        response = self.client.get('/campaign/add/')
        response = self.client.post('/campaign/add/',
        data={"name": "mylittlecampaign", "description": "xyz",
        "startingdate": "1301392136.0", "expirationdate": "1301332136.0",
        "frequency": "20", "callmaxduration": "50", "maxretry": "3",
        "intervalretry": "3000", "calltimeout": "60", "aleg_gateway": "1",
        "voipapp": "1", "voipapp_data": "2000"})
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/campaign/1/')
        self.assertTemplateUsed(response,
                                'frontend/campaign/change.html')

    def test_voip_call_report(self):
        """Test Function to check VoIP call report"""
        response = self.client.get('/voipcall_report/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
        'frontend/report/voipcall_report.html')

    def test_user_settings(self):
        """Test Function to check User settings"""
        response = self.client.get('/user_detail_change/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
        'frontend/registration/user_detail_change.html')


class NewfiesCustomerInterfaceForgotPassTestCase(TestCase):
    """Test cases for Newfies Customer Interface. for forgot password"""

    def test_check_password_reset(self):
        """Test Function to check password reset"""
        response = self.client.get('/password_reset/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
        'frontend/registration/password_reset_form.html')

        response = self.client.get('/password_reset/done/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
        'frontend/registration/password_reset_done.html')

        response = self.client.get(
                   '/reset/1-2xc-5791af4cc6b67e88ce8e/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
        'frontend/registration/password_reset_confirm.html')

        response = self.client.get('/reset/done/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
        'frontend/registration/password_reset_complete.html')


test_cases = [
    NewfiesApiTestCase,
    NewfiesTastypieApiTestCase,
    NewfiesApiCallRequestUpdateTestCase,
    NewfiesAdminInterfaceTestCase,
    NewfiesCustomerInterfaceTestCase,
    NewfiesCustomerInterfaceForgotPassTestCase,
]


def suite():
    return build_test_suite_from(test_cases)
