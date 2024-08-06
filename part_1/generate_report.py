import requests
import json 
import datetime 
import csv, io 
import os 
import pprint

class CustomerReportBuilder:

    def __init__(self):
        self.report_data = [] 

    ###################################################
    # Customers
    ###################################################

    def load_customers(self, customer_ids=None): 
        data = self.fetch_customers(customer_ids)
        if not data: 
            print("No data returned from fetch_customers()")
            return 

        for customer in data["data"]:
            customer_record = {
                "customer_name": customer.get("name", ""),
                "customer_id": customer.get("id", "")
            }
            self.report_data.append(customer_record) 
            
    def fetch_customers(self, customer_ids):
        url = "https://api.metronome.com/v1/customers"
        params = { "limit": 5 }

        # filter based on customer_ids, if available 
        if customer_ids is not None:
            params["customer_ids"] = customer_ids
        return self.fetch_api(url, 'GET', params=params)


    ###################################################
    ### Credits 
    ###################################################

    def load_customer_credits(self):
        for customer_record in self.report_data:
            credit_data = self.fetch_customer_credit(customer_record["customer_id"])
            if not credit_data: 
                print("No credit data returned for customer:", customer_record["customer_id"])
            else:
                customer_record["credits"] = self.parse_customer_credit(credit_data)

    def fetch_customer_credit(self, customer_id):
        url = "https://api.metronome.com/v1/credits/listGrants"
        params = {
            "limit": 100
        }
        payload = {
            "credit_type_ids": [],
            "customer_ids": [
                customer_id
            ],
            "credit_grant_ids": []
        }
        return self.fetch_api(url, 'POST', params=params, payload=payload)


    def parse_customer_credit(self, data):
        credit_records = [] 
        keys = [
            "id",
            "name",
            "reason",
            "effective_at",
            "expires_at",
        ]
        credit_records = [] 
        for credit in data["data"]:
            credit_record = { key:credit.get(key, "") for key in keys }
            credit_record["grant_amount"]       = credit.get("grant_amount", {}).get("amount", "")
            credit_record["paid_amount"]        = credit.get("paid_amount", {}).get("amount", "")
            credit_record["balance_inc_pending"] = credit.get("balance", {}).get("including_pending", "")
            credit_record["balance_exc_pending"] = credit.get("balance", {}).get("excluding_pending", "")
            credit_records.append(credit_record)
        
        return credit_records

    ###################################################
    ### Invoices 
    ###################################################

    def load_customer_invoices(self):
        for customer_record in self.report_data:
            invoice_data = self.fetch_customer_invoice(customer_record["customer_id"])
            if not invoice_data:
                print("No invoice data returned for customer:", customer_record["customer_id"])
            else:
                customer_record["invoices"] = self.parse_customer_invoice(invoice_data)

    def fetch_customer_invoice(self, customer_id):
        url = f"https://api.metronome.com/v1/customers/{customer_id}/invoices"
        params = {
            "limit": 100,
            "skip_zero_qty_line_items": "true",
            "sort": "date_desc"
        }
        return self.fetch_api(url, 'GET', params=params)

    def parse_customer_invoice(self, data):
        status = None                   # "DRAFT", "FINALIZED", None
        keys = [
            "id",
            "plan_name",
            "status",
            "total",
            "subtotal",
            "start_timestamp",
            "end_timestamp",
            "credit_type.name"
        ]

        invoice_records = [] 
        for invoice in data["data"]:
            # filter based on status, if available  
            if status and invoice["status"] != status:
                continue 

            # convert JSON response into rows 
            invoice_record = {} 
            for key in keys:
                if "." in key:
                    values = key.split(".")
                    invoice_record[key] = invoice.get(values[0], {}).get(values[1])
                else:
                    invoice_record[key] = invoice.get(key, "")
            invoice_records.append(invoice_record)
        
        return invoice_records


    ###################################################
    ### API Helpers 
    ###################################################

    def fetch_api(self, url, method='GET', params={}, payload={}):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer XXX'
        }
        try: 
            response = requests.request(method, url, headers=headers, params=params, json=payload)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                raise ValueError(f"Unexpected status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        except ValueError as e:
            print(f"Value error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


    

    ###################################################
    ### Write to CSV 
    ###################################################

    def to_csv(self, output_file):
        # Write header if the file is new
        self.csv_filename = output_file 

        self.header = [
            "customer_name",
            "customer_id",
            "type",
            "transaction_id",
            "plan_name",
            "status",
            "total",
            "subtotal",
            "invoice_credit_type",
            "credit_name", 
            "credit_reason",
            "grant_amount",
            "paid_amount",
            "balance_inc_pending",
            "balance_exc_pending",
            "date_start",
            "date_end",
        ]        
        self.write_header()
        
        # Iterate over customers and their invoices
        for customer in self.report_data:
            # Write invoice rows
            for invoice in customer['invoices']:
                self.write_row([
                    customer['customer_name'],
                    customer['customer_id'],
                    'invoice',
                    invoice['id'],
                    invoice['plan_name'],
                    invoice['status'],
                    invoice['total'],
                    invoice['subtotal'],
                    invoice['credit_type.name'],
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    self.convert_timestamp_format(invoice['start_timestamp']),
                    self.convert_timestamp_format(invoice['end_timestamp']),
                ])

            # Write credit rows
            for credit in customer['credits']:
                self.write_row([
                    customer['customer_name'],
                    customer['customer_id'],
                    'credit',
                    credit['id'],
                    '',
                    '',  # Plan name is not applicable to credits
                    '',  # Status is not applicable to credits
                    '',  # Total is not applicable to credits
                    '',  # Subtotal is not applicable to 
                    credit['name'],
                    credit['reason'],
                    credit['grant_amount'],
                    credit['paid_amount'],
                    credit['balance_inc_pending'],
                    credit['balance_exc_pending'],
                    self.convert_timestamp_format(credit['effective_at']),
                    self.convert_timestamp_format(credit['expires_at']),
                ])

    def convert_timestamp_format(self, date_str): 
        date_obj = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        human_readable_date = date_obj.strftime("%b %-d, %Y")
        return human_readable_date

    def write_header(self):
        file_exists = os.path.isfile(self.csv_filename)
        with open(self.csv_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(self.header)

    def write_row(self, row):
        with open(self.csv_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)


if __name__ == "__main__":
    try: 
        builder = CustomerReportBuilder()
        builder.load_customers()                # Generate report for all customers (limit: 5)
        # builder.load_customers("004747b8-9124-4060-989a-8d1075af2424")    # Run report for single customer
        builder.load_customer_invoices()        # Load customer invoice 
        builder.load_customer_credits()         # Load customer credit grants
        builder.to_csv("report.csv")            # Export to 'report.csv'

    except Exception as e:
        print(f"An error occurred while generating customer report: {e}")
