#Authored by Sam Arrowsmith
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from accounts.models import User
from django.forms.models import model_to_dict
from gamekeeper.forms import LoginForm
from treasurehunt.treasure import Treasure
from treasurehunt.views import getPins
import json


class GetPinsViewTest(TestCase):
    # this class of tests is designed to verify that the functionality behind the treasure hunt pins works as expected
    def setUp(self):
        name = 'treasurehunt_testuser'
        self.client = Client()
        self.user = User.objects.create_user(username=name, password='12345')
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboard')
        self.empty_hunt = Treasure("new hunt", 10, 'treasurehunt\default.png', True, id=0) 
        self.client.login(username=name, password='12345')  #log in as an authenticated user during set up so we don't have to do it during tests

        #Treasure.incrementStage(player_name=name,hunt_id=0,points=10) 
        #the hunt id needs to be the same as the id specified for the hunt

    def test_get_pins_no_hunts_started(self):
        # tests that no pins are on the map if no treasure hunts have been started
        #self.client.login(self.user)
        request = RequestFactory().get('/treasurehunt/next_locations/') 
        #RequestFactory() is needed so that a request can be constructed with a user attribute which can then be set to be an authenticated user
        request.user = self.user
        pins = getPins(request)   # performs a GET request for the relevant user who has not started any treasure hunts
        response_data = json.loads(pins.content)    # gets the JSONResponse as a dictionary
        self.assertNotIn('locations', response_data) # the list of pins to display shouldn't exist, provided they haven't accessed any treasure hunt start points
