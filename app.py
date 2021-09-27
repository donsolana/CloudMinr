#Import Packages
from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormTrainingClient
from azure.core.credentials import AzureKeyCredential
from pandas import DataFrame as df
import pandas
from numpy import NaN
from flask import Flask, make_response
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

#Azure Credentials 
endpoint = "https://version-0.cognitiveservices.azure.com/"
key = "9ace77082ed544689e78c7d59db75c1a"

#Initialize Form Recognizer Client
form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))


class RecieptBot(Resource):
   def get(self, receipt_url):  
        
        # Store the url for the reciept
        receiptUrl = receipt_url

        # Create result client
        poller = form_recognizer_client.begin_recognize_receipts_from_url(receiptUrl)
        result = poller.result()

        # Intialize Reciept dictionary
        itemnames_list = list()
        values_list = list()
        confidence_list = list()
        itemIDs_list =list()
        receipt_list = list()
        receipt_confidence = list()
        receipt_name = list()
        

        i = 0
        # Extract documents
        for receipt_id, receipt in enumerate(result): 
            for name, field in receipt.fields.items():
                if name == "Items":
                    for  idx, items in enumerate(field.value):
                        for item_name, item in items.value.items():
                            itemIDs_list.append(idx)
                            itemnames_list.append(item_name)
                            values_list.append(item.value)
                            confidence_list.append(item.confidence)
            
                else:
                    receipt_list.append(field.value) 
                    receipt_confidence.append(field.confidence)
                    receipt_name.append(name)
                    
        
        #put items and receipt info into dictionaries 
        item_dict = {"ID" : itemIDs_list, "item_names" : itemnames_list, "item" : values_list}
        receipt_dict = {"name": receipt_name, "" : receipt_list, "receipt_id" : receipt_id}

         #create tables for items 
        item_table = df(item_dict).pivot("ID", columns = "item_names")
        item_table.columns = ["_".join((i,j)) for i,j in item_table.columns]
        receipt_table = df(receipt_dict).pivot("receipt_id", columns = "name") #create tables for receipt metadata
        receipt_table.columns =  ["".join((i,j)) for i,j in receipt_table.columns]

        #merge tables and convert to csv
        item_table["tmp"]  = 1
        receipt_table["tmp"] = 1
        output_table = receipt_table.merge(item_table, on='tmp')
        output_table.drop("tmp", axis = "columns", inplace = True) 
        resp = make_response(output_table.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp

class InvoiceBot(Resource):
    def get(self, invoice_url):
        #Azure Credentials 
        Invoice_table = df()
        item_table = df()
        invoices = list()
        
        poller = form_recognizer_client.begin_recognize_invoices_from_url(invoice_url)
        invoices = poller.result()

        for idx, invoice in enumerate(invoices):    
            customer_name = invoice.fields.get("CustomerName")
            if customer_name:
                Invoice_table.loc[idx, "customer_name"] = customer_name.value
            else:
                Invoice_table.loc[idx, "customer_name"] = NaN
            customer_address = invoice.fields.get("CustomerAddress")
            if customer_address:
                Invoice_table.loc[idx, "customer_address"] = customer_address.value
            else:
                Invoice_table.loc[idx, "customer_address"] = NaN
            customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
            if customer_address_recipient:
                Invoice_table.loc[idx, "customer_address_recipient"] = customer_address_recipient.value
            else: 
                Invoice_table.loc[idx, "customer_address_recipient"] = NaN
            invoice_id = invoice.fields.get("InvoiceId")
            if invoice_id:
                Invoice_table.loc[idx, "invoice_id"] = invoice_id.value
            else:
                Invoice_table.loc[idx, "invoice_id"] = NaN
            invoice_date = invoice.fields.get("InvoiceDate")
            if invoice_date:
                Invoice_table.loc[idx, "invoice_date"] = invoice_date.value
            else:
                Invoice_table.loc[idx, "invoice_date"] = NaN
            invoice_total = invoice.fields.get("InvoiceTotal")
            if invoice_total:
                Invoice_table.loc[idx, "invoice_total"] = invoice_total.value
            else:
                Invoice_table.loc[idx, "invoice_total"] = NaN
            due_date = invoice.fields.get("DueDate")
            if due_date:
                Invoice_table.loc[idx, "due_date"] = due_date.value
            else:
                Invoice_table.loc[idx, "due_date"] = NaN
            Invoice_table.loc[idx, "invoice_number"] = idx+1
            for idn,item in enumerate(invoice.fields.get("Items").value):
                item_description = item.value.get("Description")
                if item_description:
                    item_table.loc[idn, "item_description"] = item_description.value
                else:
                    item_table.loc[idn, "item_description"] = NaN
                item_quantity = item.value.get("Quantity")
                if item_quantity:
                    item_table.loc[idn, "item_quantity"] = item_quantity.value
                else:
                    item_table.loc[idn, "item_quantity"] = NaN
                unit_price = item.value.get("UnitPrice")
                if unit_price:
                    item_table.loc[idn, "unit_price"] = unit_price.value
                else: 
                    item_table.loc[idn, "unit_price"] = NaN
                amount = item.value.get("Amount")
                if amount:
                    item_table.loc[idn, "Amount"] = amount.value
                else:
                    item_table.loc[idn, "Amount"] = NaN
                item_table.loc[idn, "item_number"] = idn+1
                item_table.loc[idn, "invoice_number"] = idx+1
        
        output_table = Invoice_table.merge(item_table, on="invoice_number")
        resp = make_response(output_table.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
                

api.add_resource(RecieptBot, "/receipt/<path:receipt_url>")
api.add_resource(InvoiceBot, "/invoice/<path:invoice_url>")

if __name__ == "__main__":
    app.run(debug=True)