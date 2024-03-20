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
    ''' This class of tests is designed to verify that the functionality behind the treasure hunt pins works as expected
        - GetPins is a function in the views file which doesn't actually load any templates but does modify what is shown on the views
        - It calls treasure hunt data from the backend to display on the map where relevant
    '''
    def setUp(self):
        # two pairs of users and hunts have been made so that the tests are independent and don't interfere with one another
        empty_hunt_name = 'treasurehunt_testuser'
        hunt_started_name = 'huntstarted'
        self.client = Client()
        self.empty_hunt_user = User.objects.create_user(username=empty_hunt_name, password='12345') # this user will be used when no hunts have been started
        self.hunt_started_user = User.objects.create_user(username=hunt_started_name, password='12345') # this user will be used when hunts have been started
        self.empty_hunt = Treasure("new hunt", 10, 'treasurehunt\default.png', True, id=0) 
        self.non_empty_hunt = Treasure("hunt started", 10, 'treasurehunt\default.png', True, id=-1) 

    
    ''' still faulty, mainly the increment stage not working'''
    def test_get_pins_hunt_started(self):
        # tests that if a treasure hunt has been started by the relevant user
        self.client.login(username='huntstarted', password='12345')  #log in as an authenticated user

        Treasure.incrementStage(player_name='huntstarted',hunt_id=-1,points=10) 
        #the hunt id needs to be the same as the id specified for the relevant hunt, so that it won't interfere with other tests

        request = RequestFactory().get('/treasurehunt/next_locations/') 
        #RequestFactory() is needed so that a request can be constructed with a user attribute which can then be set to be an authenticated user
        request.user = self.hunt_started_user
        pins = getPins(request)   # performs a GET request for the relevant user who has not started any treasure hunts
        response_data = json.loads(pins.content)    # gets the JSONResponse as a dictionary
        self.assertIn('locations', response_data) # the list of pins to display shouldn't exist, provided they haven't accessed any treasure hunt start points

    def test_get_pins_no_hunts_started(self):
        # tests that no pins are on the map if no treasure hunts have been started
        self.client.login(username='treasurehunt_testuser', password='12345')  #log in as an authenticated user
        request = RequestFactory().get('/treasurehunt/next_locations/') 
        #RequestFactory() is needed so that a request can be constructed with a user attribute which can then be set to be an authenticated user
        request.user = self.empty_hunt_user
        pins = getPins(request)   # performs a GET request for the relevant user who has not started any treasure hunts
        response_data = json.loads(pins.content)    # gets the JSONResponse as a dictionary
        self.assertNotIn('locations', response_data) # the list of pins to display shouldn't exist, provided they haven't accessed any treasure hunt start points
