---
weight: 10
title: API Reference
---

# SEC Data

## Basic Information of Companies

> URL: [www.finmint.us/company.csv](/data/sec/company.csv)

Company.csv file consists basic information about over 14000 companies. Updates monthly, first Sunday.

### Columns:
- `name`: Company Name
- `symbol`: Ticker Symbol
- `address`: HQ Address
- `cik`: CIK assigned by SEC
- `sik`: SIK number assigned by SEC
- `irs`: Tax number assigned by IRS
- `sector`: Company's Sector
- `industry`: Company's Industry
- `ceo`: Latest CEO of company

## 10K-10Q Financial Statements

> URL: www.finmint.us/data/sec/SYMBOL.csv  
SYMBOL is the `ticker symbol` of the company, such as `AAPL` for Apple Inc. and `MSFT` for Microsoft Corporation.

Financial data is extracted from reports---especially 10K and 10Q forms---that companies submit to Security Exchange Commission. The original data is often difficult to read or navigate. We offer those data, consolidated and homogenized, in a single `.csv` file per company.

### Columns:
- `cik` is the official number assgined to each company and often is used by official documents to identify the company.
- `stmt` is the financial statement that this item is extracted. (BS = Balance Sheet, IS = Income Statement, CF = Cash Flow, EQ = Equity, CI = Comprehensive Income, UN = Unclassifiable Statement).
- `item` is the item tag that is used by company such as `Net Income` or `Accounts Payable`.
- `date` is the item date as `integer` type in `yyyymmdd` format: 20081231 is 12/31/2008.
- `qtrs` shows how many quarters the sumber covers. 0 is for point in time (often for Balance Sheet items), 1 is for one quarter coverage, 4 is for one year coverage, and so on.
- `uom` is unit of measurement.
- `value` is the (often) numeric value of the item at given time and qtrs.
- `fiscal` is the fiscal quarter according to the company's fiscal year.
- `report` is the number of attached report that item.
### Row Key:
- Each row is unique for <`stmt`, `item`, `date`, `qtrs`>

