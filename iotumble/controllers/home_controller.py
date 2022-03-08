"""
This module contains the HomeController class, containing the functionality to allow HomeView
to interface with the model classes.
"""
from iotumble.controllers.abstract_controller import AbstractController
from iotumble.models.session import Session


class HomeController(AbstractController):
    """
    This class represents the home controller and implements AbstractController. It contains a
    constructor, the methods that allow HomeView to interface with the model classes, and the
    implemented abstract methods.
    """

    def __init__(self):
        """
        This constructor instantiates a HomeController object, loads an instance of HomeView, calls
        fill_inputs() to fill the inputs of HomeView, and then creates a Session object.
        """
        self.home_view = self.load_view("Home")(self)
        self.fill_inputs()
        self.session = Session()

    def connect(self, access_key_id: str, secret_access_key: str, region_name: str) -> bool:
        """
        This method connects the Session object to AWS, and creates an Amazon DynamoDB table
        resource in Session. Lastly, fill_incidents() is called and it returns its outcome.

        :param access_key_id: Access Key ID of the Session.
        :param secret_access_key: Secret Access Key of the Session.
        :param region_name: Region Name of the Session.
        :returns: Boolean outcome of fill_incidents().
        """
        if access_key_id == "" or secret_access_key == "" or region_name == "":
            self.home_view.show_message("Please fill all the session entries!")
            return False
        self.session.connect(access_key_id, secret_access_key, region_name)
        self.session.create_table("iotumble_incidents")
        return self.fill_incidents()

    def disconnect(self):
        """This method disconnects the Session object from AWS."""
        self.session.disconnect()

    def create_credentials(self):
        """
        This method checks that the AWS directory and credentials.ini paths exist. If either path
        does not exist, it creates them. Finally it passes the credentials.ini path to
        read_credentials() and returns its outcome.

        :returns: ConfigParser object of a read credentials.ini.
        """
        aws_path = ".aws"
        credentials_path = self.join_path(aws_path, "credentials.ini")
        if not self.check_path(aws_path):
            self.create_path(aws_path)
            self.create_path(credentials_path)
        else:
            if not self.check_path(credentials_path):
                self.create_path(credentials_path)
        return self.read_credentials(credentials_path)

    def fill_inputs(self):
        """
        This method calls create_credentials() to return a read credentials.ini. It then fills the
        session inputs of HomeView with the values of its outcome.
        """
        credentials = self.create_credentials()
        self.home_view.fill_inputs(credentials.get("access", "access_key_id"),
                                   credentials.get("access", "secret_access_key"),
                                   credentials.get("access", "region_name"))

    def fill_incidents(self) -> bool:
        """
        This method requests an incident count from Session and if it returns False, it passes an
        error message to HomeView, and returns False. If it returns True, it continues and uses its
        outcome to fill the incidents of HomeView, and return True.

        :returns: Boolean outcome of request_incident_count().
        """
        incident_count = self.session.request_incident_count()
        if not incident_count:
            self.home_view.show_message("The entered session access keys are not valid!")
            return False
        self.home_view.fill_incidents(incident_count)
        return True

    def switch(self, incident_id: int):
        """
        This method requests an Incident object from Session and if it returns False, it passes an
        error message to HomeView. If it returns True, it hides HomeView, and passes its outcome to
        load_controller() to load an instance of IncidentController. Finally it runs the main method
        of IncidentController.

        :param incident_id: ID of the Incident.
        """
        incident = self.session.request_incident(incident_id)
        if not incident:
            self.home_view.show_message("The selected incident does not exist!")
        else:
            self.home_view.hide()
            incident_controller = self.load_controller("Incident")(self.home_view, incident)
            incident_controller.main()

    def main(self):
        self.home_view.start()
