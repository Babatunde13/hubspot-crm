from datetime import datetime, timedelta
from hubspot.client import Client as HubSpot
from hubspot.crm.contacts import (
    SimplePublicObjectInputForCreate as ContactSimplePublicObjectInputForCreate,
    SimplePublicObjectInput as ContactSimplePublicObjectInput,
    PublicObjectSearchRequest as ContactPublicObjectSearchRequest
)
from hubspot.crm.deals import (
    SimplePublicObjectInput as DealSimplePublicObjectInput,
    SimplePublicObjectInputForCreate as DealSimplePublicObjectInputForCreate,
    PublicObjectSearchRequest as DealPublicObjectSearchRequest
)
from hubspot.crm.tickets import SimplePublicObjectInputForCreate as TicketSimplePublicObjectInputForCreate
from app.config import config
from app.logger import Logger

class HubspotService:
    def __init__(self):
        tokens = self._generate_tokens()
        self.client = HubSpot(access_token=tokens.access_token)
        self.last_expiration = self._get_last_token_expiration(tokens.expires_in)
        self.logger = Logger("HubspotService")
        self.TICKET_FROM_CONTACT = 16
        self.TICKET_FROM_DEAL = 28
        self.DEAL_FROM_CONTACT = 4

    def _get_last_token_expiration(self, expiry: int):
        return datetime.now() + timedelta(seconds=expiry)

    def _generate_tokens(self):
        client = HubSpot()
        return client.oauth.tokens_api.create(
            grant_type="refresh_token",
            client_id=config.HUBSPOT_CLIENT_ID,
            client_secret=config.HUBSPOT_CLIENT_SECRET,
            refresh_token=config.HUBSPOT_REFRESH_TOKEN,
        )
    
    def refresh_token(self):
        if datetime.now() >= self.last_expiration:
            tokens = self._generate_tokens()
            self.client = HubSpot(access_token=tokens.access_token)
            self.last_expiration = self._get_last_token_expiration(tokens.expires_in)
            self.logger.info("Refreshed HubSpot access token")

    def search_contact(self, email):
        try:
            contact_search = self.client.crm.contacts.search_api.do_search(ContactPublicObjectSearchRequest(
                filter_groups=[{
                    "filters": [{
                        "propertyName": "email",
                        "operator": "EQ",
                        "value": email
                    }]
                }],
                properties=["id"],
                limit=1,
            ))
            if contact_search.results:
                return contact_search.results[0].id
            return None
        except Exception as e:
            self.logger.error("Error searching contact", {"error": str(e)})

    def search_deal(self, deal_name):
        try:
            deal_search = self.client.crm.deals.search_api.do_search(DealPublicObjectSearchRequest(
                filter_groups=[{
                    "filters": [{
                        "propertyName": "dealname",
                        "operator": "EQ",
                        "value": deal_name
                    }]
                }],
                properties=["id"],
                limit=1,
            ))
            if deal_search.results:
                return deal_search.results[0].id
            return None
        except Exception as e:
            self.logger.error("Error searching deal", {"error": str(e)})

    def create_or_update_contact(self, properties: dict):
        email = properties.get("email")
        if not email:
            raise ValueError("Email is required")
        try:
            self.refresh_token()
            contact_id = self.search_contact(email)
            if contact_id:
                self.client.crm.contacts.basic_api.update(contact_id, ContactSimplePublicObjectInput(properties=properties))
                self.logger.info(f"Updated contact with email: {email}")
            else:
                contact = self.client.crm.contacts.basic_api.create(ContactSimplePublicObjectInputForCreate(properties=properties))
                contact_id = contact.id
                self.logger.info(f"Created new contact with email: {email}")
            return { "data": contact_id }
        except Exception as e:
            self.logger.error("Error creating or updating contact", {"error": str(e)})
            return { "error": "Error creating or updating contact" }

    def create_or_update_deal(self, contact_id: str, deal_name: str, properties: dict):
        try:
            self.refresh_token()
            deal_id = self.search_deal(deal_name)
            if deal_id:
                self.client.crm.deals.basic_api.update(deal_id, DealSimplePublicObjectInput(properties=properties))
                self.logger.info(f"Updated deal with name: {deal_name}")
            else:
                associations = [
                    {
                        "to": { "id": contact_id },
                        "types": [
                            {
                                "associationCategory": "HUBSPOT_DEFINED",
                                "associationTypeId": self.DEAL_FROM_CONTACT
                            }
                        ]
                    }
                ]
                deal = self.client.crm.deals.basic_api.create(DealSimplePublicObjectInputForCreate(
                    properties=properties,
                    associations=associations
                ))
                deal_id = deal.id
                self.logger.info(f"Created new deal with name: {deal_name}")

            return { "data": deal_id }
        except Exception as e:
            self.logger.error("Error creating or updating deal", {"error": str(e)})
            return { "error": "Error creating or updating deal" }

    def get_ticket_by_id(self, ticket_id):
        try:
            self.refresh_token()
            ticket_response = self.client.crm.tickets.basic_api.get_by_id(ticket_id)
            ticket = ticket_response.properties
            ticket["id"] = ticket_id
            ticket["description"] = ticket.pop("content")
            ticket["category"] = ticket.pop("hs_ticket_category")
            ticket["pipeline"] = ticket.pop("hs_pipeline")
            self.logger.info(f"Retrieved ticket with ID: {ticket_id}")
            return { "data": ticket }
        except Exception as e:
            self.logger.error("Error retrieving ticket", {"error": str(e)})
            return { "error": "Error retrieving ticket" }

    def create_ticket(self, contact_id, deal_id, properties):
        try:
            associations = [
                {
                    "to": { "id": deal_id },
                    "types": [
                        {
                            "associationCategory": "HUBSPOT_DEFINED",
                            "associationTypeId": self.TICKET_FROM_DEAL
                        }
                    ]
                },
                {
                    "to": { "id": contact_id },
                    "types": [
                        {
                            "associationCategory": "HUBSPOT_DEFINED",
                            "associationTypeId": self.TICKET_FROM_CONTACT
                        }
                    ]
                }
            ]
            self.refresh_token()
            ticket = self.client.crm.tickets.basic_api.create(TicketSimplePublicObjectInputForCreate(
                properties=properties,
                associations=associations
            ))
            self.logger.info(f"Created new ticket linked to contact ID: {contact_id} and deal ID: {deal_id}")
            return { "data": ticket }
        except Exception as e:
            self.logger.error("Error creating ticket", {"error": str(e)})
            return { "error": "Error creating ticket" }

    def get_contacts(self, limit, after):
        try:
            self.refresh_token()
            contacts_response = self.client.crm.contacts.basic_api.get_page(
                limit=limit, after=after, associations=["deals"]
            )

            contacts = []
            for contact in contacts_response.results:
                contact_data = contact.properties
                contact_data["id"] = contact.id
                contact_data["deals"] = []

                if contact.associations and "deals" in contact.associations:
                    for deal_assoc in contact.associations["deals"].results:
                        deal_response = self.client.crm.deals.basic_api.get_by_id(
                            deal_assoc.id, associations=["tickets"]
                        )
                        deal = deal_response.properties
                        deal["id"] = deal_assoc.id

                        tickets = []
                        if deal_response.associations and "tickets" in deal_response.associations:
                            for ticket_assoc in deal_response.associations["tickets"].results:
                                ticket_id = ticket_assoc.id

                                ticket_response = self.client.crm.tickets.basic_api.get_by_id(ticket_id)
                                ticket = ticket_response.properties
                                ticket["id"] = ticket_id
                                ticket["description"] = ticket.pop("content")
                                ticket["category"] = ticket.pop("hs_ticket_category")
                                ticket["pipeline"] = ticket.pop("hs_pipeline")
                                tickets.append(ticket)

                        deal["tickets"] = tickets
                        contact_data["deals"].append(deal)

                contacts.append(contact_data)

            next_after = contacts_response.paging.next.after if contacts_response.paging else None
            self.logger.info("Retrieved contacts", { "count": len(contacts), "next_after": next_after })
            return { "data": { "contacts": contacts, "next_after": next_after } }
        except Exception as e:
            self.logger.error("Error retrieving contacts", {"error": str(e)})
            return { "error": "Error retrieving contacts" }

    def get_pipeline_tickets(self):
        try:
            self.refresh_token()
            pipelines_response = self.client.crm.pipelines.pipelines_api.get_all("tickets")
            pipelines = []

            for pipeline in pipelines_response.results:
                pipeline_data = {
                    "id": pipeline.id,
                    "label": pipeline.label,
                    "stages": []
                }

                for stage in pipeline.stages:
                    stage_data = {
                        "id": stage.id,
                        "label": stage.label,
                        "display_order": stage.display_order
                    }
                    pipeline_data["stages"].append(stage_data)

                pipelines.append(pipeline_data)

            return {"data": pipelines}
        except Exception as e:
            self.logger.error("Error retrieving pipeline tickets", {"error": str(e)})
            return {"error": "Error retrieving pipeline tickets"}
    
    def get_deal_stages(self):
        pipelines = self.client.crm.pipelines.pipelines_api.get_all("deals")
        stages = []
        for pipeline in pipelines.results:
            for stage in pipeline.stages:
                print(stage)
                stages.append({
                    "id": stage.id,
                    "label": stage.label,
                    "display_order": stage.display_order
                })
        return stages
    

hubspot_service = HubspotService()
