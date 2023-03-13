## Bước 1: Import thư viện


Ở giai đoạn crawling, chúng ta cần các thư viện sau đây:
- `requests`: Thư viện dùng để gọi api đến trang web
- `BeautifulSoup`: Thư viện giúp chúng ta crawl data từ các thẻ trong file html của trang web.
- `pandas`: Thư viện giúp định hình bảng dữ liệu và lưu nó vào các file csv
- `datetime`: Thư viện giúp lấy thông tin của ngày lấy data cho file csv

```python
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup
```

## Bước 2: Gọi API và lưu raw data vào BeautifulSoup

Với `url` là đường link website dẫn đến trang chứa data về virus corona, chúng ta thực hiện lệnh gọi API và lưu vào BeautifulSoup với định dạng là `html`:

```python
url = "https://www.worldometers.info/coronavirus/"
corona_content = requests.get(url, "html.parser")
soup = BeautifulSoup(corona_content.content)
```

Sau đó, ta sẽ tìm thẻ `table` với id là `main_table_countries_today` để lấy toàn bộ các thẻ html của bảng dữ liệu:

```python
table = soup.find("table", id="main_table_countries_today")
```

## Bước 3: Trích xuất các hàng và cột và lưu data về virus corona 

Ta có thể lấy dữ liệu về các cột trong bảng dữ liệu bằng cách tìm tất cả các thẻ `<tr>` trong `<thead>`:

```python
header_row = table.find("thead").find("tr")
```

Tuy nhiên, định dạng chữ của nội dung các cột bị lỗi và không đúng theo format mong muốn, có thể gây rối khi lưu vào file csv và khi tương tác bằng DataFrame.

Chính vì vậy, ta sẽ tạo 1 dictionary với key là các cột dữ liệu còn value là 1 mảng chứa tất cả dữ liệu của cột đó:

```python
data = {
    "Country": [],
    "Total Cases": [],
    "New Cases": [],
    "Total Deaths": [],
    "New Deaths": [],
    "Total Recovered": [],
    "New Recovered": [],
    "Active Cases": [],
    "Serious, Critical": [],
    "Tot Cases/1M pop": [],
    "Deaths/1M pop": [],
    "Total tests": [],
    "Tests/1M pop": [],
    "Population": [],
    "Continent": [],
    "1 Case every X ppl": [],
    "1 Death every X ppl": [],
    "1 Test every X ppl": [],
    "New Cases/1M pop": [],
    "New Deaths/1M pop": [],
    "Active Cases/1M pop": [],
}
```

Sau đó, ta sẽ lấy tất cả các nội dung bảng dữ liệu từ các thẻ `<tr>` trong thẻ `<tbody>`:

```python
data_rows = table.find("tbody").find_all("tr")
```

Tiếp theo, ta sẽ thực hiện lấy ra từng giá trị của các cột dữ liệu và lưu nó vào dictionary trên:

```python
for row in data_rows[8:]:
    columns = row.find_all("td")[1:]
    for i, k in zip(columns, data):
        data[k].append(i.text.strip())
```

## Bước 4: Convert data thành dạng DataFrame rồi lưu vào file csv

Sau khi đã lưu đủ data vào dictionary, ta sẽ convert data sang DataFrame bằng `pandas`:

```python
df = pd.DataFrame(data)
```

Cuối cùng, ta lưu dữ liệu vào file csv tương ứng cùng với thời điểm ngày crawl data để chia thành nhiều file dữ liệu trong nhiều ngày:

```python
df.to_csv(
    f"{datetime.today().strftime(
        '%Y-%m-%d',
    )}_corona_data.csv",
    index=False
)
```

Vậy là ta đã hoàn thành crawl toàn bộ dữ liệu về tình hình dịch bệnh virus corona trên toàn thế giới và lưu nó vào file csv.