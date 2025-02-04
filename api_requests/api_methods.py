import requests


class PetstoreApi:
    def __init__(self):
        self.base_url = "https://petstore.swagger.io/v2"

    def create_pet(self, pet_id: int, category_id: int, category_name: str, name: str, photo_urls: list[str],
                   tag_id: int, tag_name: str, status: str):
        payload = {
            "id": pet_id,
            "category": {
                "id": category_id,
                "name": category_name
            },
            "name": name,
            "photoUrls": photo_urls,
            "tags": [
                {
                    "id": tag_id,
                    "name": tag_name
                }
            ],
            "status": status
        }
        response = requests.post(f"{self.base_url}/pet", json=payload)
        return response

    def get_pet_id(self, pet_id: int):
        response = requests.get(f"{self.base_url}/pet/{pet_id}")
        return response

    def get_pet_by_status(self, status: str):
        response = requests.get(f"{self.base_url}/pet/findByStatus?status={status}")
        return response

    def post_pet_image(self, pet_id: int, meta_data: str, photo_path: str):
        with open(photo_path, "rb") as file:
            files = {
                "file": (photo_path, file, "image/jpeg")
            }
            data = {
                "additionalMetadata": meta_data
            }
            response = requests.post(
                f"{self.base_url}/pet/{pet_id}/uploadImage",
                files=files,
                data=data
            )
        return response

    def update_pet_info(self, pet_id: int, category_id: int, category_name: str, name: str, photo_urls: list[str],
                        tag_id: int, tag_name: str, status: str):
        payload = {
            "id": pet_id,
            "category": {
                "id": category_id,
                "name": category_name
            },
            "name": name,
            "photoUrls": photo_urls,
            "tags": [
                {
                    "id": tag_id,
                    "name": tag_name
                }
            ],
            "status": status
        }
        response = requests.put(f"{self.base_url}/pet", json=payload)
        return response

    def delete_pet(self, pet_id: int):
        response = requests.delete(f"{self.base_url}/pet/{pet_id}")
        return response

    def create_order(self, order_id: int, pet_id: int, quantity: int, ship_date: str, status: str):
        payload = {
            "id": order_id,
            "petId": pet_id,
            "quantity": quantity,
            "shipDate": ship_date,
            "status": status,
        }
        response = requests.post(f"{self.base_url}/store/order", json=payload)
        return response

    def get_store_inventory(self):
        response = requests.get(f"{self.base_url}/store/inventory")
        return response

    def get_order_id(self, order_id: int):
        response = requests.get(f"{self.base_url}/store/order/{order_id}")
        return response

    def delete_order(self, order_id: int):
        response = requests.delete(f"{self.base_url}/store/order/{order_id}")
        return response

    def create_user(self, user_id: int, username: str, first_name: str, last_name: str, email: str, password: str,
                    phone: str, status: int):
        payload = {
            "id": user_id,
            "username": username,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": password,
            "phone": phone,
            "userStatus": status
        }
        response = requests.post(f"{self.base_url}/user", json=payload)
        return response

    def get_user_by_username(self, username: str):
        response = requests.get(f"{self.base_url}/user/{username}")
        return response

    def get_user_login(self, username: str, password: str):
        headers = {
            "username": username,
            "password": password
        }
        response = requests.get(f"{self.base_url}/user/login", headers=headers)
        return response

    def get_user_logout(self):
        response = requests.get(f"{self.base_url}/user/logout")
        return response

    def delete_user(self, username):
        response = requests.delete(f"{self.base_url}/user/{username}")
        return response
