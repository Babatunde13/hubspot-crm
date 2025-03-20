import re
from enum import Enum
from marshmallow import Schema, fields, validates, ValidationError, INCLUDE

class CategoryEnum(Enum):
    GENERAL_INQUIRY = "GENERAL_INQUIRY"
    BILLING_ISSUE = "BILLING_ISSUE"
    FEATURE_REQUEST = "FEATURE_REQUEST"
    PRODUCT_ISSUE = "PRODUCT_ISSUE"

class StageEnum(Enum):
    appointmentscheduled = "appointmentscheduled"
    qualifiedtobuy = "qualifiedtobuy"
    presentationscheduled = "presentationscheduled"
    decisionmakerboughtin = "decisionmakerboughtin"
    contractsent = "contractsent"
    closedwon = "closedwon"
    closedlost = "closedlost"

class TicketSchema(Schema):
    """
    Schema for ticket validation.
    Should contain at least
    1. subject: str
    2. description: str
    3. category: enum("general_inquiry", "technical_issue", "billing", "service_request", "meeting")
    4. pipeline: str
    5. hs_ticket_priority: str
    6. hs_pipeline_stage: str
    7. additional fields should be dynamically added
    """

    subject = fields.Str(required=True)
    description = fields.Str(required=True)
    category = fields.Enum(required=True, enum=CategoryEnum)
    pipeline = fields.Str(required=True)
    hs_ticket_priority = fields.Str(required=True)
    hs_pipeline_stage = fields.Str(required=True)

    class Meta:
        unknown = INCLUDE

class DealSchema(Schema):
    """
    Schema for deal validation.
    Should contain at least
    1. dealname: str
    2. amount: float
    3: dealstage: str
    4. tickets: list[TicketSchema]
    5. additional fields should be dynamically added
    """

    dealname = fields.Str(required=True)
    amount = fields.Float(required=True)
    dealstage = fields.Enum(required=True, enum=StageEnum)
    tickets = fields.List(fields.Nested(TicketSchema), required=True)

    class Meta:
        unknown = INCLUDE

class RegisterSchema(Schema):
    """Schema for user registration validation."""
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    phone = fields.Str(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    deals = fields.List(fields.Nested(DealSchema), required=True)

    @validates("firstname")
    def validate_firstname(self, value):
        if not value.isalpha() or not value.isascii() or len(value) < 2:
            raise ValidationError("First name must be at least 2 characters long and contain only letters.")
        
    @validates("lastname")
    def validate_lastname(self, value):
        if not value.isalpha() or not value.isascii() or len(value) < 2:
            raise ValidationError("Last name must be at least 2 characters long and contain only letters.")

    @validates("password")
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.")

        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$"
        if not re.match(regex, value):
            raise ValidationError("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.")
        
    
    def get_user_data(self, data):
        user_data = {
            "email": data["email"],
            "password": data["password"],
            "phone": data["phone"],
            "firstname": data["firstname"],
            "lastname": data["lastname"]
        }
        return user_data

class LoginSchema(Schema):
    """Schema for user login validation."""
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class SearchUsersSchema(Schema):
    """Schema for search users validation."""
    cursor = fields.Str()
    limit = fields.Int(missing=10)
