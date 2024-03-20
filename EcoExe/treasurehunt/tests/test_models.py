#Authored by Sam Arrowsmith
from django.test import TestCase
from treasurehunt.models import TreasureHunt, Activities, Stage, UserTreasure

class UserTreasureModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        treasure_hunt = TreasureHunt.objects.create(points=100, name='Example Hunt')
        UserTreasure.objects.create(hunt=treasure_hunt, player='test_player', stage_completed=2, no_points=50)

    ''' these tests check that the field values are as expected for the created model'''
    def test_player_field(self):
        user_treasure = UserTreasure.objects.get(hunt__name='Example Hunt')
        self.assertEquals(user_treasure.player, 'test_player')

    def test_stage_completed_field(self):
        user_treasure = UserTreasure.objects.get(hunt__name='Example Hunt')
        self.assertEquals(user_treasure.stage_completed, 2)

    def test_no_points_field(self):
        user_treasure = UserTreasure.objects.get(hunt__name='Example Hunt')
        self.assertEquals(user_treasure.no_points, 50)
    ''' end of block of tests '''


    # this tests that the user treasure is unique
    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            treasure_hunt = TreasureHunt.objects.create(points=100, name='Example Hunt')
            UserTreasure.objects.create(hunt=treasure_hunt, player='test_player', stage_completed=2, no_points=50)

class StageModelTest(TestCase):

    '''
    Tests here check that the stage model is functional by setting up a row in the table with data, 
    checking that the data was inserted correctly, and checking uniqueness of treasure hunts by asserting
    that an exception is raised if identical data is inserted into the table
    '''

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        treasure_hunt = TreasureHunt.objects.create(points=100, name='Example Hunt')
        activity = Activities.objects.create(type='Type1', name='Activity1', info='Info1', location='Location1')
        Stage.objects.create(hunt=treasure_hunt, order=1, activity_id=activity, no_points=50, information='Information1')

    def test_order_field(self):
        stage = Stage.objects.get(hunt__name='Example Hunt')
        self.assertEquals(stage.order, 1)

    def test_activity_id_field(self):
        stage = Stage.objects.get(hunt__name='Example Hunt')
        self.assertEquals(stage.activity_id.name, 'Activity1')

    def test_no_points_field(self):
        stage = Stage.objects.get(hunt__name='Example Hunt')
        self.assertEquals(stage.no_points, 50)

    def test_information_field(self):
        stage = Stage.objects.get(hunt__name='Example Hunt')
        self.assertEquals(stage.information, 'Information1')

    def test_unique_together_constraint(self):
        #test that no new hunts can be made with the same data
        with self.assertRaises(Exception):
            treasure_hunt = TreasureHunt.objects.create(points=100, name='Example Hunt')
            activity = Activities.objects.create(type='Type1', name='Activity1', info='Info1', location='Location1')
            Stage.objects.create(hunt=treasure_hunt, order=1, activity_id=activity, no_points=50, information='Information1')

class ActivitiesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Activities.objects.create(type='Type1', name='Activity1', info='Info1', location='Location1')

    #test that the field types are right
    def test_type_field(self):
        activity = Activities.objects.get(act_id=1)
        self.assertEquals(activity.type, 'Type1')

    #test that the field names are right
    def test_name_field(self):
        activity = Activities.objects.get(act_id=1)
        self.assertEquals(activity.name, 'Activity1')

    #test that the field info is correct
    def test_info_field(self):
        activity = Activities.objects.get(act_id=1)
        self.assertEquals(activity.info, 'Info1')

    #test that the field location is right
    def test_location_field(self):
        activity = Activities.objects.get(act_id=1)
        self.assertEquals(activity.location, 'Location1')

    #test that the default location is as expected
    def test_default_location_name(self):
        activity = Activities.objects.get(act_id=1)
        default_location_name = activity.location_name
        self.assertEquals(default_location_name, 'Parker moot room!')

    #test that the default points value for an activity is as expected (10)
    def test_default_points(self):
        activity = Activities.objects.get(act_id=1)
        default_points = activity.points
        self.assertEquals(default_points, 10)

class TreasureHuntModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        TreasureHunt.objects.create(points=100, name='Example Hunt')

    def test_points_label(self):
        #test that the label has the correct name
        treasure_hunt = TreasureHunt.objects.get(hunt_id=1)
        field_label = treasure_hunt._meta.get_field('points').verbose_name
        self.assertEquals(field_label, 'points')

    def test_name_max_length(self):
        #test that the maximum length of the name field is 100
        treasure_hunt = TreasureHunt.objects.get(hunt_id=1)
        max_length = treasure_hunt._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_default_image(self):
        #test that the default image is correct
        treasure_hunt = TreasureHunt.objects.get(hunt_id=1)
        default_image = treasure_hunt.image
        self.assertEquals(default_image, '/img/Default.png')

    def test_unique_name(self):
        # Attempt to create another treasure hunt with the same name
        with self.assertRaises(Exception):
            TreasureHunt.objects.create(points=150, name='Example Hunt')

    