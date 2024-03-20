#Authored by Sam Arrowsmith
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from accounts.models import User
from django.forms.models import model_to_dict
from gamekeeper.forms import LoginForm
from treasurehunt.treasure import Treasure
from treasurehunt.views import getPins
from treasurehunt import models
import json


class GetPinsViewTest(TestCase):
    ''' This class of tests is designed to verify that the functionality behind the treasure hunt pins works as expected
        - GetPins is a function in the views file which doesn't actually load any templates but does modify what is shown on the views
        - It calls treasure hunt data from the backend to display on the map where relevant
    '''
    def setUp(self):
        name = "user"
        self.client = Client()
        self.user = User.objects.create_user(username=name, password='12345') # this user will be used when no hunts have been started

        # Below is the creation of a hunt with activities
        self.hunt = Treasure("hunt started", 10, 'treasurehunt\default.png', True, id=1) 
        activity_id1 = self.hunt.addActivity("2,2", "quiz", "", 10, "Parker Moot Room!")
        self.hunt.addStage(1, activity_id1)

        activity_id2 = self.hunt.addActivity("2,3", "quiz", "", 10, "Parker Moot Room!")
        self.hunt.addStage(2, activity_id2)

        activity_id3 = self.hunt.addActivity("2,4", "quiz", "", 10, "Parker Moot Room!")
        self.hunt.addStage(3, activity_id3)

        activity_id4 = self.hunt.addActivity("2,7", "quiz", "", 10, "Parker Moot Room!")
        self.hunt.addStage(4, activity_id4)

    def test_get_pins_no_hunts_started(self):
        # tests that no pins are on the map if no treasure hunts have been started
        self.client.login(username='user', password='12345')  #log in as an authenticated user
        request = RequestFactory().get('/treasurehunt/next_locations/') 
        #RequestFactory() is needed so that a request can be constructed with a user attribute which can then be set to be an authenticated user
        request.user = self.user
        pins = getPins(request)   # performs a GET request for the relevant user who has not started any treasure hunts
        response_data = json.loads(pins.content)    # gets the JSONResponse as a dictionary
        self.assertNotIn('locations', response_data) # the list of pins to display shouldn't exist, provided they haven't accessed any treasure hunt start points
