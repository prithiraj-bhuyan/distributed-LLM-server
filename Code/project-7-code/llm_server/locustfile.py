from locust import HttpUser, task
class QuickstartUser(HttpUser):
    @task
    def hello_world(self):
        data_dict = {
          "username":"admin",
          "password":"asdasd"
        }
        self.client.post("/v1/logintoken", data_dict)