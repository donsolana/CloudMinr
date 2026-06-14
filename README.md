# Azure Form Recognizer API Service

## Overview

This project is a RESTful API built with Flask and Azure Form Recognizer that extracts structured data from receipts and invoices provided via URL. The extracted information is transformed into tabular format and returned as a downloadable CSV file.

The service exposes two endpoints:

* **Receipt Extraction API** – Extracts receipt metadata and purchased items.
* **Invoice Extraction API** – Extracts invoice details, customer information, and line items.

## Features

### Receipt Processing

* Extracts receipt metadata such as:

  * Merchant Name
  * Transaction Date
  * Total Amount
  * Tax Information
  * Payment Method
* Extracts purchased item details:

  * Item Name
  * Quantity
  * Price
* Returns results as a CSV file.

### Invoice Processing

* Extracts invoice metadata including:

  * Customer Name
  * Customer Address
  * Invoice ID
  * Invoice Date
  * Due Date
  * Invoice Total
* Extracts invoice line items:

  * Description
  * Quantity
  * Unit Price
  * Amount
* Returns results as a CSV file.

---

## Technologies Used

* Python 3.x
* Flask
* Flask-RESTful
* Azure AI Form Recognizer
* Pandas
* NumPy

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/azure-form-recognizer-api.git

cd azure-form-recognizer-api
```

### Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Example requirements:

```txt
azure-ai-formrecognizer
azure-core
flask
flask-restful
pandas
numpy
```

---

## Azure Configuration

Create an Azure Form Recognizer resource in Azure Portal.

Set the following credentials:

```python
endpoint = "YOUR_FORM_RECOGNIZER_ENDPOINT"
key = "YOUR_FORM_RECOGNIZER_KEY"
```

For production environments, use environment variables:

```bash
export FORM_RECOGNIZER_ENDPOINT="your-endpoint"
export FORM_RECOGNIZER_KEY="your-key"
```

Then load them in Python:

```python
import os

endpoint = os.getenv("FORM_RECOGNIZER_ENDPOINT")
key = os.getenv("FORM_RECOGNIZER_KEY")
```

---

## Running the Application

Start the Flask application:

```bash
python app.py
```

Default server:

```text
http://127.0.0.1:5000
```

---

## API Endpoints

### 1. Receipt Extraction

#### Request

```http
GET /receipt/<receipt_url>
```

#### Example

```http
GET /receipt/https://example.com/receipt.jpg
```

#### Response

A CSV file named:

```text
export.csv
```

containing receipt metadata and item-level information.

---

### 2. Invoice Extraction

#### Request

```http
GET /invoice/<invoice_url>
```

#### Example

```http
GET /invoice/https://example.com/invoice.pdf
```

#### Response

A CSV file named:

```text
export.csv
```

containing invoice metadata and line-item information.

---

## Sample Output

### Invoice CSV

| customer_name | invoice_id | invoice_date | item_description | item_quantity | unit_price | amount |
| ------------- | ---------- | ------------ | ---------------- | ------------- | ---------- | ------ |
| John Doe      | INV-001    | 2024-01-15   | Laptop           | 1             | 1200       | 1200   |
| John Doe      | INV-001    | 2024-01-15   | Mouse            | 2             | 25         | 50     |

### Receipt CSV

| MerchantName | Total | item_Description | item_TotalPrice |
| ------------ | ----- | ---------------- | --------------- |
| Store A      | 25.50 | Bread            | 5.00            |
| Store A      | 25.50 | Milk             | 3.50            |

---

## Error Handling

The application relies on Azure Form Recognizer validation and may return errors when:

* The document URL is invalid.
* The document cannot be accessed publicly.
* The document format is unsupported.
* Azure credentials are incorrect.
* Azure service limits are exceeded.



## Project Structure

```text
project/
│
├── app.py
├── requirements.txt
├── README.md
└── .env
```

---

## Future Improvements

* Support batch document processing
* Authentication and API keys
* Swagger/OpenAPI documentation
* Docker containerization
* Async processing for large documents
* Database storage for extracted records
* Support for custom-trained Form Recognizer models

---

## License

This project is provided as-is for educational and development purposes. Review Microsoft's Azure Form Recognizer licensing and pricing before deploying to production.

## Author

Built using Flask and Azure AI Form Recognizer to automate extraction of structured data from receipts and invoices.
