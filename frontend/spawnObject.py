import json

class Member:

    #Validation methods
    def valid_id(id: str) -> bool:
        """
        Validates the ID format.
        """
        if len(id) != 8:
            raise ValueError("ID must be 8 characters long")
        for char in id:
            if char.isalpha():
                raise ValueError("ID must contain only numbers")
        return True
    def valid_phone_number(phone_number: str) -> bool:
        """
        Validates the phone number format.
        """
        if len(phone_number) != 10:
            raise ValueError("Phone number must be 10 digits long")
        if not phone_number.startswith("0"):
            raise ValueError("Phone number must start with 0")
        if not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits")
        return True
    def valid_email(email: str) -> bool:
        valid_email_domains = {"@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com", "@icloud.com", "@live.com"}
        if email.endswith() not in valid_email_domains:
            raise ValueError("Email domain is not valid or misssing @")
        



    def __init__ (self, id: str, name: str, age: int, address: str, phone_number: str, email: str):
        Member.valid_phone_number(phone_number)
        Member.valid_email(email)
        if len(name) < 3:
            raise ValueError("Name must be at least 3 characters long")
        self.id = id
        self.phone_number = phone_number
        self.name = name
        self.age = age
        self.address = address
        self.email = email
    
