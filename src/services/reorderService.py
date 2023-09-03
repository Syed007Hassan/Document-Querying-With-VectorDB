from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import json
import smtplib
from email.message import EmailMessage
from src.models.emailModel import EmailDTO
from src.models.reorderModel import ReorderModel
from src.services.palm_api_Service import palm_create_response
from config import baseUrl
from datetime import datetime
import base64
import io
from email.mime.application import MIMEApplication


class ReorderService:
    def __init__(self):
        self.model = ReorderModel()
        self.base_url = baseUrl

    def save_reorder_data(self, reorder_data):
        self.model.add_reorder_data(reorder_data)

    def save_vendor_data(self, vendor_data):
        self.model.add_vendor_data(vendor_data)

    def get_reorder_data(self):
        try:
            url = self.base_url + "/api/Item/GetItemsReorderStatus"
            response = requests.get(url)
            response.raise_for_status()
            reorder_data = response.json()
            self.save_reorder_data(reorder_data)
            message = """Hi username,
            It’s been a long time. Please share the purpose of your visit...
            Is it for General purpose or do you want to Reorder Item?"""
            return [message] + reorder_data
        except requests.exceptions.RequestException as e:
            return "An error occurred while getting reorder data. Please try again later."
        except Exception as e:
            return "An error occurred while processing your request. Please try again later."

    def get_vendor_data(self, item_code):
        try:
            url = self.base_url + \
                "/api/Contact/GetContactNamesWithReorderItems/{}".format(
                    item_code)
            response = requests.get(url)
            response.raise_for_status()
            vendor_data = response.json()
            self.save_vendor_data(vendor_data)
            message = "These are the vendors that deal with the items with id of: " + item_code
            for vendor in vendor_data:
                vendor['itemCode'] = item_code
            return [message] + vendor_data
        except requests.exceptions.RequestException as e:
            return "An error occurred while getting vendor data. Please try again later."
        except Exception as e:
            return "An error occurred while processing your request. Please try again later."

    @staticmethod
    def save_pdf(pdf_content):
        try:
            decoded_pdf_content = base64.b64decode(
                pdf_content, validate=True).decode('utf-8')
            with open('reorder.pdf', 'wb') as f:
                f.write(decoded_pdf_content)
            return 'PDF saved successfully'
        except Exception as e:
            return f"An error occurred while saving the PDF: {e}"

    def send_email(self, item_code, vendor_id, item_quantity, itemCost, pdf_content):
        try:
            # ReorderService.save_pdf(pdf_content)
            # Decode the base64-encoded PDF content
            pdf_content_dict = json.loads(pdf_content)
            pdf_content_encoded = pdf_content_dict['pdfContentEncoded']
            pdf_content_decoded = base64.b64decode(pdf_content_encoded)
            url = self.base_url + \
                "/api/Contact/GetContactByID/{}".format(vendor_id)
            response = requests.get(url)
            response.raise_for_status()
            vendor_data = response.json()
            if (vendor_data['emailId'] == None or vendor_data['emailId'] == " "):
                vendor_data['emailId'] = "hassan.ali@onetechnologyservices.com"
            url = self.base_url + "/api/Item/GetItemByNo/{}".format(item_code)
            response = requests.get(url)
            response.raise_for_status()
            item_data = response.json()
            url = self.base_url + "/api/Item/addReorderQuantity?itemCode=" + \
                item_code+"&quantity="+item_quantity

            response = requests.post(url)
            nowDate = str(datetime.now())
            body = palm_create_response('Write an email to vendor name ' + vendor_data['name'] + ' and email ' + vendor_data['emailId'] + ' and I want to add order a item ' + item_data['itemName'] + 'that has a cost price of ' +
                                        itemCost + ' and its quantity is ' + item_quantity + ' and todays dat is' + nowDate + '. It should be a professional email and you can extract my name from this email muhammad.ahsan@onetechnologyservices.com.')

            # Set up the email message
            msg = MIMEMultipart()
            msg['Subject'] = "Reorder Item " + item_data['itemName']
            msg['From'] = "muhammad.ahsan@onetechnologyservices.com"
            msg['To'] = vendor_data['emailId']
            # Add the body text
            body_text = MIMEText(body)
            msg.attach(body_text)

           # Add the PDF file as an attachment
            pdf_attachment = MIMEApplication(
                pdf_content_decoded, _subtype='pdf')
            pdf_attachment.add_header(
                'Content-Disposition', 'attachment', filename='PO.pdf')
            msg.attach(pdf_attachment)

            # Send the email
            smtp_host = "smtp.office365.com"
            smtp_port = 587
            smtp_username = "muhammad.ahsan@onetechnologyservices.com"
            smtp_password = "Nurs@1234"

            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)

            return 'Email sent successfully'
        except Exception as e:
            return f"An error occurred while sending the email: {e}"
        except Exception as e:
            print("Error in send_email: %s", str(e))
            return "An error occurred while processing your request. Please try again later."
