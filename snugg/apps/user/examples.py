from drf_spectacular.utils import OpenApiExample


class TestUser:
    signin_example = signup_example = OpenApiExample(
        name="test user",
        value={
            "user": {
                "pk": 1,
                "email": "test@gmail.com",
                "username": "testuser",
                "birth_date": "1997-06-21",
                "created_at": "2022-03-08T21:39:02.361832+09:00",
                "last_login": "2022-03-18T14:17:18.522627+09:00",
            },
            "token": {
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NzY2NzAzOCwiaWF0IjoxNjQ3NTgwNjM4LCJqdGkiOiJlMzEzZDJhNTVmYjc0MTkwOTZlMDk3ZjMxOGM2ZjhlZCIsInVzZXJfaWQiOjF9.b_CNB_ZgxLa_PXsddMltzxpM23JaZNmZ-1TnnzDuHRk",
                "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ3NTg0MjM4LCJpYXQiOjE2NDc1ODA2MzgsImp0aSI6ImM3N2M4NDY2YTM4MzQ1MTRiMmVlMmRlZDkyNGVkZWI1IiwidXNlcl9pZCI6MX0.6_g_HtvdYyRv6u6fwl99E39FWbvJf3zFPZ9iSZuVmUE",
            },
        },
    )
