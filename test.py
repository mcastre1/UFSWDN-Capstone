import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

import app
from models import setup_db, Job, Inventory, Sink


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.server = app
        self.server.test = True
        self.app = self.server.app
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        self.jwt = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdlWnQxR0JZY25jZkJ2eVpheEVIMCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ubXl4azdoZnRvbWVmbHJkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMTEyOTU4NTM3MDUyNDQzMjgyOCIsImF1ZCI6ImNhcHN0b25lQVBJIiwiaWF0IjoxNjgxNjExNTQxLCJleHAiOjE2ODE2MTg3NDEsImF6cCI6IlBZRVByYmNTbldQbFRySUFqdlRqcDJjYW5pSm5Tb3RUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6aW52ZW50b3J5X2l0ZW0iLCJjcmVhdGU6am9iIiwiY3JlYXRlOnNpbmsiLCJkZWxldGU6aW52ZW50b3J5X2l0ZW0iLCJkZWxldGU6am9iIiwiZGVsZXRlOnNpbmsiLCJwYXRjaDppbnZlbnRvcnlfaXRlbSIsInBhdGNoOmpvYiIsInBhdGNoOnNpbmsiLCJyZWFkOmludmVudG9yeSIsInJlYWQ6aW52ZW50b3J5X2l0ZW0iLCJyZWFkOmpvYi1kZXRhaWxzIiwicmVhZDpqb2JzIiwicmVhZDpzaW5rIiwicmVhZDpzaW5rcyJdfQ.CfCN70i8cgG8Db1Sf8gjw3_RP8ExgZj-evxelWxgkJW8btUFF8SdnThcnE3iQsfdQ1NBWBz6gqHZFKZDVWkNN_Sq1zB__yKsc3EK76ydCOQhSGE7i0C_6HODAK8Bi1vPpTpzR9cI04mHrbjldYcbyH8BwHlglLMYqHtgYCMVgAv-1TTYBcdzy1jCk-TdSXWB9eJp4NizzzT6m1RxNg4wVw74jUjzS-d6WWIs8fECoY0JYaxNPAIs1U70WEiBRQ4NsSmsSJuLGChQtjz9pYx0apKqkYKKdAIp8ihnITn0D3nGtcv3Y_zcjyJzQGf1wpxnE3xi79orEMm3EeKCILP1Zg"
        self.user_auth = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdlWnQxR0JZY25jZkJ2eVpheEVIMCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ubXl4azdoZnRvbWVmbHJkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNTIyNzgwMzg4OTY1Njk3MTM4MyIsImF1ZCI6ImNhcHN0b25lQVBJIiwiaWF0IjoxNjgxNjEzODkxLCJleHAiOjE2ODE2MjEwOTEsImF6cCI6IlBZRVByYmNTbldQbFRySUFqdlRqcDJjYW5pSm5Tb3RUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOmpvYi1kZXRhaWxzIiwicmVhZDpqb2JzIl19.I06TYzbOl9fB6U6nlxPTCVyrZuD4ruUP3eRc8-DHrlYZHaQjBC-0b4NF6Nvl1_syTg8Dh-gwbhKemzPziapFXxubaR3qLre9w9gQSSujtPHAIpvHt4hffovUr4UxWYNTzoM6xOtN4wM-Pvj67jDZhPpjik8ZOEVM0FrZuR16pwJVrShnGrPO70V67O-agetkXEbKD-PmBiU8PLFilGLvaHCyMiOuQVTK0l5knPYowtbJhfFf1gbbka8sf8PKg6Gsaw9e2jK2phXusaKWkHuCUz9_x8gHaLk2V_RAsFIdaAO3T5P_UhpUMFORviTt3xGdWyXNbr4K-1Q_BbQmWaqHzA"

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_home(self):
        res = self.client().get('/')
        jobs = [job.format() for job in Job.query.all()]
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['jobs'], jobs)

    def test_create_job(self):
        data = {
            "job_name": "job",
            "contact_name": "contact name",
            "contact_phone": "1111",
            "address": "address",
            "material": "material",
            "status": "status",
            "edge_finish": "edge_finish",
            "sinks": "[1,2]"}

        res = self.client().post(
            '/job',
            data=data,
            headers={
                'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

        # Making sure to delete test data.
        job = Job.query.get(int(data['job_id']))
        job.delete()

    def test_create_job_400_error(self):
        data = {
            "job_name": "job",
            "contact_name": "contact name",
            "contact_phone": "1111",
            "address": "address",
            "material": "material",
            "status": "status",
            "edge_finish": "edge_finish",
            "sinks": [
                1,
                2]}

        res = self.client().post(
            '/job',
            data=data,
            headers={
                'Authorization': self.jwt})

        self.assertEqual(res.status_code, 400)

    def test_get_create_job_form(self):
        res = self.client().get('/job', headers={'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # No header passed in.
    def test_get_create_job_form_error_401(self):
        res = self.client().get('job')

        self.assertEqual(res.status_code, 401)

    def test_view_job(self):
        job = Job(
            job_name="job",
            contact_name="contact name",
            contact_phone="1111",
            address="address",
            material="material",
            status="status",
            edge_finish="edge_finish",
            sinks=[
                1,
                2])
        job.insert()

        res = self.client().get(
            f'/job/{job.id}',
            headers={
                'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["job"], job.format())

        job.delete()

    def test_view_job_400_error(self):
        res = self.client().get(
            '/job/1000000000',
            headers={
                'Authorization': self.jwt})

        self.assertEqual(res.status_code, 400)

    def test_update_job(self):
        job = Job(
            job_name="job",
            contact_name="contact name",
            contact_phone="1111",
            address="address",
            material="material",
            status="status",
            edge_finish="edge_finish",
            sinks=[
                1,
                2])
        job.insert()

        data = {
            "job_name": "jobx",
            "contact_name": "contactname",
            "contact_phone": "00001111",
            "address": "addressxx",
            "material": "materialx",
            "status": "status",
            "edge_finish": "edge_finish",
            "sinks": [
                1,
                2]}

        res = self.client().get(
            f'/job/{job.id}',
            data=data,
            headers={
                'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['job'], job.format())

        job.delete()

    # Id is too large
    def test_update_job_400_error(self):
        res = self.client().get(
            '/job/10101010',
            headers={
                'Authorization': self.jwt})

        self.assertEqual(res.status_code, 400)

    def test_inventory(self):
        res = self.client().get(
            '/inventory',
            headers={
                'Authorization': self.jwt})
        data = json.loads(res.data)

        inventory = [item.format() for item in Inventory.query.all()]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["inventory"], inventory)

    # No authorization to look at it.
    def test_inventory_error(self):
        res = self.client().get('/inventory')

        self.assertEqual(res.status_code, 401)

    def test_view_inventory_item(self):
        inventory_item = Inventory(sink_id=1, count=80)
        inventory_item.insert()

        res = self.client().get(
            f'/inventory/{inventory_item.id}',
            headers={
                'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['inventory_item'], inventory_item.format())

        inventory_item.delete()

    # Id is not found.
    def test_view_inventory_item_error(self):
        res = self.client().get(
            '/inventory/444444',
            headers={
                'Authorization': self.jwt})

        self.assertEqual(res.status_code, 400)

    def test_update_inventory_item(self):
        inventory_item = Inventory(sink_id=1, count=80)
        inventory_item.insert()

        data = {"count": 20}

        res = self.client().get(
            f'/inventory/{inventory_item.id}',
            headers={
                'Authorization': self.jwt},
            data=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['inventory_item'], inventory_item.format())

        inventory_item.delete()

    def test_update_inventory_item(self):
        data = {"count": 20}

        res = self.client().get(
            '/inventory/90',
            headers={
                'Authorization': self.jwt},
            data=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_add_inventory_item_form(self):
        res = self.client().get(
            '/inventory/add',
            headers={
                'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_inventory_item_form_error(self):
        res = self.client().get('/inventory/add')

        self.assertEqual(res.status_code, 401)

    def test_add_inventory_item(self):
        data = {'sink_id': 1, 'count': 40}

        res = self.client().post(
            '/inventory/add',
            headers={
                'Authorization': self.jwt},
            data=data)
        data = json.loads(res.data)

        inventory_items = [inventory_item.format()
                           for inventory_item in Inventory.query.all()]
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["inventory_items"], inventory_items)

        inventory_item = Inventory.query.get(int(data["inventory_item_id"]))
        inventory_item.delete()

    def test_add_inventory_item_error(self):
        data = {'sink_id': 23, 'count': 40}

        res = self.client().post(
            '/inventory/add',
            headers={
                'Authorization': self.jwt},
            data=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_delete_inventory_item(self):
        inventory_item = Inventory(sink_id=2, count=100)
        inventory_item.insert()

        res = self.client().delete(
            f'/inventory/{inventory_item.id}/delete_inventory_item',
            headers={
                'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_delete_inventory_item_error(self):
        res = self.client().delete(
            f'/inventory/3000/delete_inventory_item',
            headers={
                'Authorization': self.jwt})

        self.assertEqual(res.status_code, 400)

    def test_get_sinks(self):
        sinks = [sink.format() for sink in Sink.query.all()]
        res = self.client().get('/sinks', headers={'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['sinks'], sinks)

    def test_get_sinks_error(self):
        res = self.client().get('/sinks')

        self.assertEqual(res.status_code, 401)

    def test_view_sink(self):
        sink = Sink(description="test_desc")
        sink.insert()

        res = self.client().get(
            f'/sinks/{sink.id}',
            headers={
                'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sink'], sink.format())

        sink.delete()

    def test_view_sink_error(self):
        res = self.client().get(
            '/sinks/1234551',
            headers={
                'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_update_sink(self):
        sink = Sink(description="test_desc")
        sink.insert()

        data = {'description': 'new desc!'}

        res = self.client().get(
            f'/sinks/{sink.id}',
            headers={
                'Authorization': self.jwt},
            data=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sink'], sink.format())

    def test_update_sink_error(self):
        data = {'description': 'new desc!'}

        res = self.client().get(
            '/sinks/100000',
            headers={
                'Authorization': self.jwt},
            data=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_delete_sink(self):
        sink = Sink(description="test_desc")
        sink.insert()

        res = self.client().delete(
            f'/sinks/{sink.id}/delete_sink',
            headers={
                'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_delete_sink_error(self):
        sink = Sink(description="test_desc")
        sink.insert()

        res = self.client().delete(
            f'/sinks/2400000/delete_sink',
            headers={
                'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_add_sink_form(self):
        res = self.client().get(
            '/sinks/add',
            headers={
                'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_sink_form_error(self):
        res = self.client().get('/sinks/add')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_add_sink(self):
        data = {'description': 'description'}

        res = self.client().post(
            '/sinks/add',
            data=data,
            headers={
                'Authorization': self.jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(Sink.query.get(int(data['sink_id'])))

        sink = Sink.query.get(int(data['sink_id']))
        sink.delete()

    def test_add_sink_error(self):
        data = {'description': 90}

        res = self.client().post('/sinks/add', data=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_get_sinks_with_user_role(self):

        res = self.client().get('/sinks',
                                headers={'Authorization': self.user_auth})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
