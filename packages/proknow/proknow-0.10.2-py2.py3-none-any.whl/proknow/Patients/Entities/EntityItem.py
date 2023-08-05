from .Scorecards import EntityScorecards


class EntityItem(object):
    """

    This class is a base class for specific entity types.

    Attributes:
        id (str): The id of the entity (readonly).
        workspace_id (str): The id of the workspace (readonly).
        patient_id (str): The id of the patient (readonly).
        data (dict): The complete representation of the entity as returned from the API (readonly).
        scorecards (proknow.Patients.EntityScorecards): An object for interacting with the
            scorecards belonging to the entity.

    """

    def __init__(self, patients, workspace_id, patient_id, entity):
        """Initializes the PatientItem class.

        Parameters:
            patients (proknow.Patients.Patients): The Patients instance that is instantiating the
                object.
            workspace_id (str): The id of the workspace to which the patient belongs.
            patient_id (str): The id of the patient to which the entity belongs.
            entity (dict): A dictionary of entity attributes.
        """
        self._patients = patients
        self._requestor = self._patients._requestor
        self._workspace_id = workspace_id
        self._patient_id = patient_id
        self._id = entity["id"]
        self._data = entity
        self.scorecards = EntityScorecards(patients, workspace_id, self._id)

    @property
    def id(self):
        return self._id

    @property
    def workspace_id(self):
        return self._workspace_id

    @property
    def patient_id(self):
        return self._patient_id

    @property
    def data(self):
        return self._data

    def delete(self):
        """Deletes the entity.

        Raises:
            AssertionError: If the input parameters are invalid.
            :class:`proknow.Exceptions.HttpError`: If the HTTP request generated an error.

        Example:
            This examples shows how you can delete the entities within a patient while leaving the
            patient intact::

                from proknow import ProKnow

                pk = ProKnow('https://example.proknow.com', credentials_file="./credentials.json")
                patients = pk.patients.lookup("Clinical", ["HNC-0522c0009"])
                patient = patients[0].get()
                entities = patient.find_entities(lambda entity: True)
                for entity in entities:
                    entity.get().delete()
        """
        self._requestor.delete('/workspaces/' + self._workspace_id + '/entities/' + self._id)
