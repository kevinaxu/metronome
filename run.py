import requests
import json 
import datetime 
import csv, io 
import os 

class CustomerReportBuilder:

    '''
    [   
        {'customer_name': 'DJLAPQ Ltd.', 'qcustomer_id': '004747b8-9124-4060-989a-8d1075af2424'}
    ]
    '''
    def __init__(self):
        self.report_data = [] 
        self.csv_filename = "out.csv"

    ###################################################
    # Customers
    ###################################################

    def load_customers(self, customer_ids=None): 
        data = self.fetch_customers(customer_ids)
        for customer in data["data"]:
            customer_record = {
                "customer_name": customer.get("name", ""),
                "customer_id": customer.get("id", "")
            }
            self.report_data.append(customer_record) 
            
    def fetch_customers(self, customer_ids):
        headers = {
            'Authorization': 'Bearer 84811fb7a96fe56a484ed1810ed4a066f92073eae6184615bc365589dd1b9656'
        }
        url = "https://api.metronome.com/v1/customers"
        params = { "limit": 10 }
        # filter based on customer_ids, if available 
        if customer_ids is not None:
            params["customer_ids"] = customer_ids
        return self.fetch_api(url, 'GET', params=params, payload=payload)



    ###################################################
    ### Credits 
    ###################################################

    def load_customer_credits(self):
        url = "https://api.metronome.com/v1/credits/listGrants"
        params = {
            "limit": 100
        }
        payload = {
            "credit_type_ids": [],
            "customer_ids": [
                "5f770337-056f-4430-813d-f6ace4ff876c"
            ],
            "credit_grant_ids": []
        }
        return self.fetch_api(url, 'POST', params=params, payload=payload)


    ###################################################
    ### Invoices 
    ###################################################

    def load_customer_invoices(self):
        for customer_record in self.report_data:
            invoice_data = self.fetch_customer_invoice(customer_record["customer_id"])
            customer_record["invoices"] = self.parse_customer_invoice(invoice_data)

    def fetch_customer_invoice(self, customer_id):
        url = f"https://api.metronome.com/v1/customers/{customer_id}/invoices"
        params = {
            "limit": 100,
            "skip_zero_qty_line_items": "true",
            "sort": "date_desc"
        }
        headers = {
            'Authorization': 'Bearer 84811fb7a96fe56a484ed1810ed4a066f92073eae6184615bc365589dd1b9656'
        }
        return self.fetch_api(url, 'GET', params=params, payload=payload)


    def parse_customer_invoice(self, data):
        status = None                   # "DRAFT", "FINALIZED", None
        keys = [
            "id",
            "start_timestamp",
            "end_timestamp",
            "plan_name",
            "status",
            "total",
            "subtotal",
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
                'Authorization': 'Bearer 84811fb7a96fe56a484ed1810ed4a066f92073eae6184615bc365589dd1b9656'
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

    def to_csv(self):
        # Write header if the file is new

        # TODO: make this dynamic 
        self.header = ["customer_name", "customer_id", "invoice_id", "start_timestamp", "end_timestamp", "plan_name", "status", "total", "subtotal", "credit_type.name"]
        self.write_header()
        
        # Iterate over customers and their invoices
        for customer in self.report_data:
            customer_values = [customer[key] for key in ["customer_name", "customer_id"]]

            for invoice in customer.get("invoices", []):
                invoice_values = [invoice[key] for key in invoice.keys()]

                # Write the row for each invoice
                self.write_row(customer_values + invoice_values)


    def write_header(self):
        # Check if the file exists
        file_exists = os.path.isfile(self.csv_filename)
        
        # Open the CSV file in append mode
        with open(self.csv_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            
            # Write the header if the file is new
            if not file_exists:
                writer.writerow(self.header)


    def write_row(self, row):
        with open(self.csv_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)



if __name__ == "__main__":

    builder = CustomerReportBuilder()
    builder.load_customers("004747b8-9124-4060-989a-8d1075af2424")
    # builder.load_customers()
    builder.load_customer_invoices()
    builder.to_csv()
    # print(builder.report_data)

    # customer_id = "334ad07b-7bc1-4e3c-8337-a344837e344f"

    # Invoices 
    # response = fetch_customer_invoices(customer_id)
    # parse_customer_invoice(response)

    # Handle 




###################################################
#
# POST /credits/listGrants 
#
###################################################


# POST /credits/listGrants
def get_customer_credit_grants():
    url = "https://api.metronome.com/v1/credits/listGrants"

    payload = {
        "credit_type_ids": [],
        "customer_ids": [
            "5f770337-056f-4430-813d-f6ace4ff876c"
        ],
        "credit_grant_ids": []
    }

    # payload="{\n    \"credit_type_ids\": [\n    ],\n    \"customer_ids\": [\n        \"5f770337-056f-4430-813d-f6ace4ff876c\"\n    ],\n    \"credit_grant_ids\": [\n    ]\n}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 84811fb7a96fe56a484ed1810ed4a066f92073eae6184615bc365589dd1b9656'
    }

    response = requests.request("POST", url, headers=headers, json=payload)
    # response = '{"data":[{"id":"c4d35b39-df82-492f-9b46-e83a6ee1af7f","name":"July grant","customer_id":"5f770337-056f-4430-813d-f6ace4ff876c","reason":"","invoice_id":null,"effective_at":"2024-07-01T00:00:00.000Z","expires_at":"2026-07-01T00:00:00.000Z","grant_amount":{"amount":1900000,"credit_type":{"id":"2714e483-4ff1-48e4-9e25-ac732e8f24f2","name":"USD (cents)"}},"paid_amount":{"amount":1900000,"credit_type":{"id":"2714e483-4ff1-48e4-9e25-ac732e8f24f2","name":"USD (cents)"}},"priority":12,"balance":{"including_pending":1655169.1199999999,"excluding_pending":1900000,"effective_at":"2024-09-01T00:00:00.000Z"},"deductions":[],"pending_deductions":[{"amount":-244830.88,"reason":"Credit deduction of $2,448.3088000000002466550 USD from credit grant July grant","effective_at":"2024-08-01T00:00:00+00:00","running_balance":1655169.1199999999,"created_by":"Metronome System","credit_grant_id":"c4d35b39-df82-492f-9b46-e83a6ee1af7f","invoice_id":"e4b78d04-8ecb-492c-8fde-a97ad5421f44"}],"custom_fields":{}},{"id":"ec9cf78b-79e6-4d00-a7be-91c86b27f057","name":"Acme Corp Promotional Credit Grant","customer_id":"5f770337-056f-4430-813d-f6ace4ff876c","reason":"Incentivize new customer","invoice_id":null,"effective_at":"2024-04-01T00:00:00.000Z","expires_at":"2026-04-01T00:00:00.000Z","grant_amount":{"amount":100000,"credit_type":{"id":"2714e483-4ff1-48e4-9e25-ac732e8f24f2","name":"USD (cents)"}},"paid_amount":{"amount":100000,"credit_type":{"id":"2714e483-4ff1-48e4-9e25-ac732e8f24f2","name":"USD (cents)"}},"priority":1,"balance":{"including_pending":0,"excluding_pending":72491.75,"effective_at":"2024-09-01T00:00:00.000Z"},"deductions":[{"amount":-11914.9,"reason":"Credit deduction of $119.149 USD from credit grant Acme Corp Promotional Credit Grant","effective_at":"2024-05-01T00:00:00+00:00","running_balance":88085.1,"created_by":"Metronome System","credit_grant_id":"ec9cf78b-79e6-4d00-a7be-91c86b27f057","invoice_id":"150e56f6-bc83-4674-8c05-8b5559ae142f"},{"amount":-15593.35,"reason":"Credit deduction of $155.9335 USD from credit grant Acme Corp Promotional Credit Grant","effective_at":"2024-07-01T00:00:00+00:00","running_balance":72491.75,"created_by":"Metronome System","credit_grant_id":"ec9cf78b-79e6-4d00-a7be-91c86b27f057","invoice_id":"dbdce152-dc58-4257-8113-3cfa6cafe970"}],"pending_deductions":[{"amount":-72491.75,"reason":"Credit deduction of $724.9175 USD from credit grant Acme Corp Promotional Credit Grant","effective_at":"2024-08-01T00:00:00+00:00","running_balance":0,"created_by":"Metronome System","credit_grant_id":"ec9cf78b-79e6-4d00-a7be-91c86b27f057","invoice_id":"e4b78d04-8ecb-492c-8fde-a97ad5421f44"}],"custom_fields":{}}],"next_page":null}'
    return json.loads(response.text)


def calculate_customer_total_credit_grant(data):
    total = 0 
    for credit in data["data"]:
        total += credit["balance"]["including_pending"]
    return round(total, 2)

# response = get_customer_credit_grants()
# total_credit = calculate_customer_total_credit_grant(response)
# print("total credit grant:", total_credit)

# print(response.text)


