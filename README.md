
# Part I 

* What data to include in the Customer Summary? 
	* Customer info: `customer_id`, `customer_name`,
	* Invoices: `id`, `plan_name`, `status`, `total`, `subtotal`, `credit_type.name`
	* Credit grants: `name`, `reason`, `grant_amount`, `paid_amount`, `balance_inc_pending`, `balance_exc_pending`
    * Shared data: `record type` (either `invoice` or `credit`)`date_start`, `end` 
* How to represent the data as CSV? 
	* A given Customer can be associated with many Invoices and many Credit Grants
	* I wanted to include both types of data in the customer summary report, so I decided to list out all Invoices and Credit grants for a given Customer. 
	* There is some overlap in fields (`date_start` and `date_end`)
	* I decided not to include aggregations such as total invoice balance, total credit balance, etc. and instead highlighted overall raw data. 
	* The resulting output is relatively sparse but contains all credits and all invoices for a given customer. 
* Approach: 
	* Used Postman to explore the code 
	* Python script to query the Metronome API, parse the results, and load into output CSV (see `generate_report.py` )
* The script can be modified to generate a report for: 
	* All / Some / One Customer:
		* All Customers: `builder.getCustomers()`
		* Some Customers: `builder.getCustomers("cust1,cust2,cust3")`
		* One Customer: `builder.getCustomers("cust1")`
	* Both Invoices / Credit information 
		* `builder.loadInvoiceData()`
		* `builder.loadCreditData()`
	* Filter Invoice by status

**Script**: (part_1/generate_report.py)[./part_1/generate_report.py]
**Output CSV**: (part_1/customers.csv)[./part_1/report.csv]

**Sample**: 

| customer_name | customer_id                          | type    | transaction_id                       | plan_name | status    | total     | subtotal  | invoice_credit_type | credit_name                        | credit_reason            | grant_amount | paid_amount | balance_inc_pending | balance_exc_pending | date_start  | date_end    |
| ------------- | ------------------------------------ | ------- | ------------------------------------ | --------- | --------- | --------- | --------- | ------------------- | ---------------------------------- | ------------------------ | ------------ | ----------- | ------------------- | ------------------- | ----------- | ----------- |
| DJLAPQ Ltd.   | 004747b8-9124-4060-989a-8d1075af2424 | invoice | 513e9159-0931-51f5-81e1-a7b0d6de6dbf | Free Plan | DRAFT     | 0         | 0         | USD (cents)         |                                    |                          |              |             |                     |                     | Aug 1, 2024 | Sep 1, 2024 |
| DJLAPQ Ltd.   | 004747b8-9124-4060-989a-8d1075af2424 | invoice | 672b212b-5a87-477d-b85d-b5f957ff75d1 | Free Plan | FINALIZED | 187131.72 | 269761.87 | USD (cents)         |                                    |                          |              |             |                     |                     | Jul 1, 2024 | Aug 1, 2024 |
| DJLAPQ Ltd.   | 004747b8-9124-4060-989a-8d1075af2424 | invoice | 29658a41-6eff-4515-aaec-cae015ad6126 | Free Plan | FINALIZED | 0         | 17369.85  | USD (cents)         |                                    |                          |              |             |                     |                     | Jun 1, 2024 | Jul 1, 2024 |
| DJLAPQ Ltd.   | 004747b8-9124-4060-989a-8d1075af2424 | invoice | 996a662a-ca7c-4e1e-86bb-237ccec79153 | Free Plan | FINALIZED | 0         | 0         | USD (cents)         |                                    |                          |              |             |                     |                     | May 1, 2024 | Jun 1, 2024 |
| DJLAPQ Ltd.   | 004747b8-9124-4060-989a-8d1075af2424 | invoice | bad1671b-f710-40c8-ad5a-02f4ab1175a3 | Free Plan | FINALIZED | 0         | 0         | USD (cents)         |                                    |                          |              |             |                     |                     | Apr 1, 2024 | May 1, 2024 |
| DJLAPQ Ltd.   | 004747b8-9124-4060-989a-8d1075af2424 | credit  | 2562ad52-baea-41b2-a709-f51115a049a5 |           |           |           |           |                     | Acme Corp Promotional Credit Grant | Incentivize new customer | 100000       | 100000      | 0                   | 0                   | Apr 1, 2024 | Apr 1, 2026 |

# Part II

**Process**: 
- Load sample egress data into **SQLite** database. 
- **DB Browser** used to visualize data and run SQL queries. 
- Script to create tables and import sample egress data into sqlite (see `load_sqlite.sh`) 
	- Used sqlite csv mode
	- Created table using schema from sample data and types from Entity Diagrams
	- Imported data using `.import` command making sure to ignore header row 

### Query 1

**Prompt**: Write a query that calculates the total number of images that were generated for each size between March 10th and March 25th (inclusive).

**Query**: 
```sql
SELECT sli.name, SUM(sli.quantity) AS num_images
FROM sub_line_item AS sli
JOIN billable_metric AS bm ON bm.id = sli.billable_metric_id
WHERE bm.aggregate_keys LIKE '%num_images%'
AND sli.updated_at BETWEEN '2024-03-10' AND '2024-03-26'
GROUP BY sli.billable_metric_name;
```

**Results**: (No results from this query)[./part_2/query_1.csv]

**Questions**: 
* Which table is the source of truth for the number of images generated? Looks like two tables contain this data: `sub_line_items` and `events`. However, in both cases I was not able to write a query that pulled results. 
	* `sub_line_items` - no records in time range March 10th - March 25th (query above) 
	* `events` - num_images is stored in the `properties` column. Based on the Entity Diagram, this is a `json` field. However, I was unable to parse the json field using SQLite built-in JSON extension because the `properties` is not valid JSON. 

### Query 2

**Prompt**: Recreate the March invoice for customer A1 Company. Write a query that returns a list of all the charges (description, quantity, unit price, total) for the finalized March invoice for customer A1 Company. The screenshot below provides a sample of a February finalized invoice. The query should return the corresponding lines under the CPU Hours and Storage products for March.

**Query**: 
```sql
SELECT
	inv.status, inv.total, inv.start_timestamp, inv.end_timestamp, inv.issued_at,
	sli.name, sli.quantity, sli.subtotal, inv.credit_type_name
FROM line_item AS li
JOIN sub_line_item AS sli ON li.id = sli.line_item_id
	JOIN (
	SELECT i.*
	FROM invoice AS i
	JOIN customer AS cust ON cust.id = i.customer_id
	WHERE cust.name = "A1 Company"
	AND i.start_timestamp = '2024-02-29 0:00:00'
) AS inv ON li.invoice_id = inv.id;
```

**Results**: (query_2.csv)[./part_2/query_2.csv]

**Approach**: 
- Subquery to get all invoices for customer "A1 Company" in March 
- JOIN against the `line_item` and `sub_line_item` records associated with that invoice
- Return charge information

### Query 3

**Prompt**: Generate a report of billings by Plan for the month of March 2024

Query: 
```sql
SELECT i.customer_id, i.plan_id, i.plan_name, i.status, i.total,
	li.name, li.quantity, li.total,
	i.credit_type_name, i.start_timestamp, i.end_timestamp
FROM invoice as i
JOIN line_item as li ON li.invoice_id = i.id
WHERE i.start_timestamp BETWEEN '2024-03-01 0:00:00' AND '2024-04-01 0:00:00';
```

**Results**: (query_3.csv)[./part_2/query_3.csv]

**Approach**: 
- Get all invoice `line_item` 's associated with invoice for March 
