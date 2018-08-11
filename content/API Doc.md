---
title: "API Documentation"
date: 2018-08-08
tags: ["API", "Datasets", "Documentation", "How to", "Reference"]
card: 'Example file: 
    <input style="color: blue" type="text" value="q/AAPL.csv" onchange="change_tag(this)"> (you can change it) <br>
    `base`    = https://data.invisement.com <br>  
    `file`    = q/AAPL.csv <br>
    `url`     = `base`/`file` <br>  
    `viewer`  = `base`?`file`'

---

### Download, Explore, or Embed

- Download any data file through its https `url`:  
 https://data.invisement.com/q/AAPL.csv

- View any data file through our `viewer`:  
https://data.invisement.com?q/AAPL.csv

- Embed `viewer` to any of our data `file` in your html page:  
`<iframe src="https://data.invisement.com?q/AAPL.csv" width="100%"></iframe>`

---

### Available Datasets

- basic/company.csv ([view](https://data.invisement.com?basic/company.csv) or [download](https://data.invisement.com/basic/company.csv))
    - Includes a basic information about companies. 
    - Columns: [`ticker`, `cik`, `irs`, `name`, `sic`, `state`]
- sec/CIK.csv
    - Consolidated financial data submitted by company in 10-K and 10-Q forms. 
    - columns: [`tag`, `date`, `qtrs`, `value`, `unit`]
- q/TICKER.csv
    - Quarterly data about core financial indicators for each company. 
    - columns: [`tag`, `period`, `value`, `unit`, `date`]
- y/TICKER.csv
    - Yearly data about core financial indicators for each company by. 
    - columns: [`tag`, `period`, `value`, `unit`, `date`]

<!---
- **q-stmt/TICKER.csv**
    - Quarterly panel data of the financial statements for each company. 
    - rows: `tag`, columns: `period`
- **y-stmt/TICKER.csv**
    - Yearly panel data of the financial statements for each company. 
    - rows: `tag`, columns: `period`
--->

Please replace `TICKER` with company's ticker symbol and `CIK` with its CIK. For instance, Apple's `TICKER` is AAPL and its `CIK` is 320193.

---
### Fetch Data Files

#### Google Sheets  
Use =importData(`url`) formula:
```sheets
=importData(https://data.invisement.com/q/AAPL.csv) 
```

#### Python
Use pandas library
```python
import pandas as pd
data = pd.read_csv(url)
```

#### R

```r
data = read.csv(url(data_url))
```

#### JavaScript
Fetch the file's url and then parse it (we recommend `Papa.parse`)
```js
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/4.1.2/papaparse.min.js"></script>

fetch(url)
    .then(response => response.text())
    .then(Papa.parse)
    .then(response => response.data) 
    ## output is js array of arrays [['col1', 'col2', ...]['1.1', '1.2', ...], ['2.1', '2.2', ...] ...]
    .then(whatever you want to do with parsed data);
```

#### Excel
In Excel, from menu select `Data` then click `from Text/CSV` 
and in `File name` enter `url`: `https://data.invisement.com/q/AAPL.csv`

---

<script>
    change_tag = function (elem) {
        old = new RegExp(elem.defaultValue, "g")
        document.body.innerHTML = document.body.innerHTML.replace(old, elem.value);
        elem.defaultValue = elem.value
    }
</script>

