from locust import HttpUser, task
class QuickstartUser(HttpUser):
    @task
    def hello_world(self):
        data_dict = {
          "username":"admin",
          "password":"asdasd"
        }
        self.client.post("/api/token/", data_dict)