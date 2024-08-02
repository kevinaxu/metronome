import requests
import json 
import datetime 
import csv, io 


###################################################
#
# GET /customers/:id/invoices
#
###################################################

def fetch_customer_invoices(customer_id):
    url = f"https://api.metronome.com/v1/customers/{customer_id}/invoices"
    params = {
        "limit": 100,
        "skip_zero_qty_line_items": "true",
        "sort": "date_desc"
    }
    headers = {
        'Authorization': 'Bearer 84811fb7a96fe56a484ed1810ed4a066f92073eae6184615bc365589dd1b9656'
    }

    response = requests.request("GET", url, headers=headers, params=params)
    return json.loads(response.text)


# pull out invoice data: start_timestamp, end_timestamp
def parse_customer_invoice(data):
    status = None                   # "DRAFT", "FINALIZED", None
    include_line_items = False      # True / False 

    # Using an in-memory file-like object
    output = io.StringIO()
    writer = csv.writer(output)

    keys = [
        "start_timestamp",
        "end_timestamp",
        "customer_id",
        "plan_name",
        "status",
        "total",
        "subtotal",
        "credit_type.name"
    ]

    # Write header
    writer.writerow(keys)

    for invoice in data["data"]:
        # filter based on status, if available  
        if status and invoice["status"] != status:
            continue 

        # convert JSON response into rows 
        row = [] 
        for key in keys:
            if "." in key:
                values = key.split(".")
                row.append(invoice.get(values[0], {}).get(values[1]))
            else:
                row.append(invoice.get(key, ""))
        
        # write to output 
        writer.writerow(row)

    # Get the CSV content as a string
    csv_content = output.getvalue() 
    output.close()

    # Print the CSV content
    print(csv_content)


if __name__ == "__main__":

    customer_id = "334ad07b-7bc1-4e3c-8337-a344837e344f"

    # Invoices 
    response = fetch_customer_invoices(customer_id)
    parse_customer_invoice(response)

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





def transform_get_customer_invoice(data):
    csv_string = ''

    keys = data["data"][0].keys()
    header = ','.join(keys)
    csv_string += header + '\n'

    for customer in data["data"]:
        values = [] 
        for key in keys:
            values.append(str(customer[key]))
        csv_string += ','.join(values) + '\n'

    return csv_string

def calculate_customer_total_invoice_balance(data):
    balance = 0 
    for invoice in data["data"]:
        if invoice["status"] == "DRAFT":
            balance += invoice["total"]
    return balance 

def count_customer_draft_invoice(data):
    return len(data["data"])


# data = get_customer_invoices()
# csv_string = transform_get_customer_invoice(data)
# balance = calculate_customer_total_invoice_balance(data)
# num_open_invoices = count_customer_draft_invoice(data)
# print("total balance:", round(balance, 2))
# print("# open invoices", num_open_invoices)
# print(csv_string)

###################################################
#
# GET /customers 
#
###################################################

def get_customers(): 
    # payload = {}
    # headers = {
    #     'Authorization': 'Bearer 84811fb7a96fe56a484ed1810ed4a066f92073eae6184615bc365589dd1b9656'
    # }
    # url = "https://api.metronome.com/v1/customers?limit=100"
    # response = requests.request("GET", url, headers=headers, data=payload)

    response = '{"data":[{"name":"DJLAPQ Ltd.","id":"004747b8-9124-4060-989a-8d1075af2424","customer_config":{"salesforce_account_id":null},"external_id":"ERTMPA4M","ingest_aliases":["ERTMPA4M"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"OUWIIM Inc.","id":"0602ebf7-659e-470a-a536-9fbd413fb42b","customer_config":{"salesforce_account_id":null},"external_id":"5O9CTU3A","ingest_aliases":["5O9CTU3A"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"RTLKR LLC","id":"15b367c9-04b9-4064-9a58-b589928898fd","customer_config":{"salesforce_account_id":null},"external_id":"3DWGSEDM","ingest_aliases":["3DWGSEDM"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"BQYGSA Corp.","id":"1715df37-9b9b-4829-b381-e7febaefb102","customer_config":{"salesforce_account_id":null},"external_id":"L9RN960G","ingest_aliases":["L9RN960G"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"HWU LLC","id":"20ffd2e6-ff2e-4347-8045-9e744ef8a986","customer_config":{"salesforce_account_id":null},"external_id":"OOHAOMTT","ingest_aliases":["OOHAOMTT"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"NYMRRFC Corp.","id":"2209a058-dbe1-4e8c-8325-fb8daa1cc987","customer_config":{"salesforce_account_id":null},"external_id":"MTYYAJA3","ingest_aliases":["MTYYAJA3"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"YCXZKJHDGH LLC","id":"2294f7f7-19a6-44a2-b9f9-4b6b79134d12","customer_config":{"salesforce_account_id":null},"external_id":"QFP5F6QS","ingest_aliases":["QFP5F6QS"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"FZR Ltd.","id":"2ac3705a-51a6-4149-8f6a-0113941e94e7","customer_config":{"salesforce_account_id":null},"external_id":"848LH7WS","ingest_aliases":["848LH7WS"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"JEAVPMO Co.","id":"2ae68df2-533e-44bf-9b4d-ac766c7ac3da","customer_config":{"salesforce_account_id":null},"external_id":"8J8VZ78P","ingest_aliases":["8J8VZ78P"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"NSFYJ Corp.","id":"334ad07b-7bc1-4e3c-8337-a344837e344f","customer_config":{"salesforce_account_id":null},"external_id":"V198GY0R","ingest_aliases":["V198GY0R"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"MWOX LLC","id":"37154c55-bd42-4b7e-a453-51dd005b35b7","customer_config":{"salesforce_account_id":null},"external_id":"D5WAPI0G","ingest_aliases":["D5WAPI0G"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"HDCEOZSD Inc.","id":"3e233dbd-0280-4def-aaa9-011a3a4ba745","customer_config":{"salesforce_account_id":null},"external_id":"X4UFS3DN","ingest_aliases":["X4UFS3DN"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"AJLUAY Corp.","id":"40430943-1fa7-48f4-86ba-0c27ad2386a4","customer_config":{"salesforce_account_id":null},"external_id":"3UXXAJV8","ingest_aliases":["3UXXAJV8"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"IITGBOGYI Corp.","id":"5b9a90c0-75cc-4771-958e-9974a3324dc3","customer_config":{"salesforce_account_id":null},"external_id":"SDOYRUW1","ingest_aliases":["SDOYRUW1"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"UBHRWJKDA LLC","id":"5f770337-056f-4430-813d-f6ace4ff876c","customer_config":{"salesforce_account_id":null},"external_id":"X6N0OP6Q","ingest_aliases":["X6N0OP6Q"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"TCEZCCLJ Co.","id":"5fb28f87-7884-4ce1-9b37-d3687f2d8cf2","customer_config":{"salesforce_account_id":null},"external_id":"1CU0WYC9","ingest_aliases":["1CU0WYC9"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"Example-Customer-5","id":"67c54616-a4d5-4717-8c95-4aa3b3e547b2","customer_config":{"salesforce_account_id":null},"external_id":"67c54616-a4d5-4717-8c95-4aa3b3e547b2","ingest_aliases":[],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"TTKPUBJEA Inc.","id":"69e51ea4-2ca3-4bf1-b606-6a8b496d98d5","customer_config":{"salesforce_account_id":null},"external_id":"X2UFRXH6","ingest_aliases":["X2UFRXH6"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"GFRSUWSM LLC","id":"6c2e6096-2adc-4ced-b660-2211bc59b449","customer_config":{"salesforce_account_id":null},"external_id":"IF4AL4RN","ingest_aliases":["IF4AL4RN"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"Example-Customer-4","id":"6d82ef71-38ef-449a-acb5-43909ff8dcf4","customer_config":{"salesforce_account_id":null},"external_id":"6d82ef71-38ef-449a-acb5-43909ff8dcf4","ingest_aliases":[],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"UTNAVKA Corp.","id":"6e2856ae-5f8f-4d61-815b-fc0fbde62648","customer_config":{"salesforce_account_id":null},"external_id":"SNEM3G6S","ingest_aliases":["SNEM3G6S"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"RKFCZA LLC","id":"6e46bd95-c129-4ff4-8a8f-a2b8e20575bb","customer_config":{"salesforce_account_id":null},"external_id":"CU4G9BIQ","ingest_aliases":["CU4G9BIQ"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"EWLGCNLZYO LLC","id":"6f723b7f-c288-4581-8744-c4f6e3618db8","customer_config":{"salesforce_account_id":null},"external_id":"6VHQ8EM0","ingest_aliases":["6VHQ8EM0"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"WSFQO LLC","id":"70b5f746-575e-463c-8710-b7cbd44ee29e","customer_config":{"salesforce_account_id":null},"external_id":"ACM3Q3BN","ingest_aliases":["ACM3Q3BN"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"LUAGEVIDE Inc.","id":"72bdf92e-6545-4438-b037-a9accd83df42","customer_config":{"salesforce_account_id":null},"external_id":"F2923GD5","ingest_aliases":["F2923GD5"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"SMHZ Ltd.","id":"743597b7-09ce-47cb-a58e-3125133bbeb0","customer_config":{"salesforce_account_id":null},"external_id":"AU5RVGYF","ingest_aliases":["AU5RVGYF"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"B1 Company","id":"7c5a8bc2-823e-4b11-9f41-6d5e711c2485","customer_config":{"salesforce_account_id":null},"external_id":"b1_company","ingest_aliases":["b1_company"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"Example-Customer-3","id":"8251d9e1-dc48-4d80-a80d-2686373c4213","customer_config":{"salesforce_account_id":null},"external_id":"8251d9e1-dc48-4d80-a80d-2686373c4213","ingest_aliases":[],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"BSLUNCUJV Inc.","id":"8406da13-89a4-4187-bfbf-97e5cfce7e1a","customer_config":{"salesforce_account_id":null},"external_id":"2OQ7MJSO","ingest_aliases":["2OQ7MJSO"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"BPLS LLC","id":"841b795b-8d8f-46cb-8afc-dcd02017ae07","customer_config":{"salesforce_account_id":null},"external_id":"UH0EPDMP","ingest_aliases":["UH0EPDMP"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"B2 Company","id":"8dcc5073-51d8-49a9-bec3-a9f8ee2f6f6b","customer_config":{"salesforce_account_id":null},"external_id":"8dcc5073-51d8-49a9-bec3-a9f8ee2f6f6b","ingest_aliases":[],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"SCLXHPBFWA Corp.","id":"90277e63-6b05-4309-9c9b-3d2be627b868","customer_config":{"salesforce_account_id":null},"external_id":"OMTMNZX3","ingest_aliases":["OMTMNZX3"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"A1 Company","id":"9ca4743f-5c9e-46e3-a2db-1d484405d5ad","customer_config":{"salesforce_account_id":null},"external_id":"a1_company","ingest_aliases":["a1_company"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"LFQRAK Corp.","id":"a82c9499-4cf6-482d-ae24-946abb51cd0c","customer_config":{"salesforce_account_id":null},"external_id":"TPOAZ77I","ingest_aliases":["TPOAZ77I"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"XBSPENF Co.","id":"aaa84bd5-f852-4ed7-a0bf-af68f0195b9c","customer_config":{"salesforce_account_id":null},"external_id":"TLSDO3FL","ingest_aliases":["TLSDO3FL"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"BEQRRRJ Co.","id":"ab3a00d6-299d-4a9d-9c27-dfdf0a3e6207","customer_config":{"salesforce_account_id":null},"external_id":"Y79ABSFU","ingest_aliases":["Y79ABSFU"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"EBX Inc.","id":"b66d1125-dbfe-43c3-b8b7-d17380ed3db2","customer_config":{"salesforce_account_id":null},"external_id":"NQ7JXX87","ingest_aliases":["NQ7JXX87"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"SMLF Corp.","id":"b744587f-2bed-4021-b6e4-a391bf06c227","customer_config":{"salesforce_account_id":null},"external_id":"VGME3HX0","ingest_aliases":["VGME3HX0"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"EVEYTUBPAU LLC","id":"c001a9e7-0608-498a-99e5-97e562b1d4d2","customer_config":{"salesforce_account_id":null},"external_id":"RRMCD81W","ingest_aliases":["RRMCD81W"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"Example-Customer-2","id":"c12ca317-81fc-4ecf-9052-8d8e95fe91ea","customer_config":{"salesforce_account_id":null},"external_id":"c12ca317-81fc-4ecf-9052-8d8e95fe91ea","ingest_aliases":[],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"BOUCWKOV LLC","id":"c185f11c-d07b-429a-990f-625cbd34bd33","customer_config":{"salesforce_account_id":null},"external_id":"GSQGVQYX","ingest_aliases":["GSQGVQYX"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"PZDTNYQO LLC","id":"c2e35176-2976-4a5a-8251-defe343bd1d1","customer_config":{"salesforce_account_id":null},"external_id":"01M9ZRH3","ingest_aliases":["01M9ZRH3"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"MCTPLJ Ltd.","id":"c59e8fb7-5b98-4d60-ab04-384fc6b3ae63","customer_config":{"salesforce_account_id":null},"external_id":"UU0TMIK8","ingest_aliases":["UU0TMIK8"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"SXLBM LLC","id":"cb03e255-9e2f-4f6e-be86-d38af0347d91","customer_config":{"salesforce_account_id":null},"external_id":"0BKBM3BW","ingest_aliases":["0BKBM3BW"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"DQKCCQ LLC","id":"ceb0de3a-addf-42bc-9d9d-3cbfd5aced1f","customer_config":{"salesforce_account_id":null},"external_id":"NLQZTO6A","ingest_aliases":["NLQZTO6A"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"JILCIYMWQO Corp.","id":"d2ad44af-e5f8-4f6c-8c50-e8c95411b451","customer_config":{"salesforce_account_id":null},"external_id":"FLBWAKPU","ingest_aliases":["FLBWAKPU"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"WWUZYRPNT LLC","id":"d2c703e8-924d-489d-b9e7-e12734ecdb6f","customer_config":{"salesforce_account_id":null},"external_id":"O2A59JK9","ingest_aliases":["O2A59JK9"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"USGTLYTFWC Co.","id":"d6e0e20c-55a9-44aa-89cd-8544600d2f73","customer_config":{"salesforce_account_id":null},"external_id":"FK3ADTOI","ingest_aliases":["FK3ADTOI"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"NOO Co.","id":"d73b37f6-916a-4784-b820-3a92d66a07dc","customer_config":{"salesforce_account_id":null},"external_id":"M0VWZTWP","ingest_aliases":["M0VWZTWP"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"WFADG LLC","id":"dbfd6a0c-7621-4daf-9450-7dc10e534c7c","customer_config":{"salesforce_account_id":null},"external_id":"KY7FX7NN","ingest_aliases":["KY7FX7NN"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"CAD LLC","id":"ddd08099-6fd3-4929-843e-167cde350679","customer_config":{"salesforce_account_id":null},"external_id":"Q6QFZ6S6","ingest_aliases":["Q6QFZ6S6"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"Example-Customer","id":"f1b1e9dc-ed3d-4993-864a-af33addb1152","customer_config":{"salesforce_account_id":null},"external_id":"f1b1e9dc-ed3d-4993-864a-af33addb1152","ingest_aliases":[],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"UUMSWBDBE Corp.","id":"f367a3c6-59a9-4eb6-a4b2-ba20b493011e","customer_config":{"salesforce_account_id":null},"external_id":"8Z0GOX9B","ingest_aliases":["8Z0GOX9B"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"ZAJGHIMYP Ltd.","id":"f7e81f46-f099-4d4a-b35c-258985df6a55","customer_config":{"salesforce_account_id":null},"external_id":"BC2UZLLI","ingest_aliases":["BC2UZLLI"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"GDPMJNOUF Corp.","id":"f8a084c6-b432-4bcf-8a78-c2e4373b8fa0","customer_config":{"salesforce_account_id":null},"external_id":"L0U82PKR","ingest_aliases":["L0U82PKR"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"VJRWHOGMKN Inc.","id":"f8ed8d1d-6901-46cc-8f62-961d45d634b9","customer_config":{"salesforce_account_id":null},"external_id":"37SP3F6P","ingest_aliases":["37SP3F6P"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"JIVTJXZWU Ltd.","id":"fa04d74f-010b-4b5a-b005-748684c2d2cd","customer_config":{"salesforce_account_id":null},"external_id":"24ADKO62","ingest_aliases":["24ADKO62"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}},{"name":"OYZVSBFZB Ltd.","id":"fc8ba3ae-2d8a-41fb-81a6-ca8d1cd556e3","customer_config":{"salesforce_account_id":null},"external_id":"GEJ17RD7","ingest_aliases":["GEJ17RD7"],"custom_fields":{},"current_billable_status":{"value":"billable","effective_at":null}}],"next_page":null}'
    return json.loads(response)


def transform_get_customers_response(data):
    csv_string = ''
    keys = data["data"][0].keys()
    header = ','.join(keys)
    csv_string += header + '\n'

    for customer in data["data"]:
        values = [] 
        for key in keys:
            values.append(str(customer[key]))
        csv_string += ','.join(values) + '\n'

    return csv_string     


# data = get_customers()
# csv_string = transform_get_customers_response(data)
# print(csv_string)

