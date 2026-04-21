import base64
import urllib.request

mermaid_code = """erDiagram
    USERS { 
        int USER_ID PK 
        string NAME 
        string EMAIL 
        string PASSWORD 
    }
    ADMIN { 
        int ADMIN_ID PK 
        string ADMIN_NAME 
        string PASSWORD 
    }
    PACKAGES { 
        int PACKAGE_ID PK 
        string P_NAME 
        text DESCRIPTION 
        decimal PRICE 
    }
    BOOKINGS { 
        int BOOKING_ID PK 
        date BOOKING_DATE 
        string STATUS 
    }
    REVIEW { 
        int REVIEW_ID PK 
        int RATING 
        text REVIEW_TEXT 
    }
    PAYMENTS { 
        int PAYMENT_ID PK 
        date PAYMENT_DATE 
        decimal AMOUNT 
    }
    USERS ||--o{ BOOKINGS : "MAKES"
    USERS ||--o{ REVIEW : "WRITES"
    PACKAGES ||--o{ BOOKINGS : "IS_FOR"
    ADMIN ||--o{ PACKAGES : "MANAGES"
    ADMIN ||--o{ BOOKINGS : "VIEWS"
    BOOKINGS ||--|| PAYMENTS : "HAS"
"""

encoded_code = base64.urlsafe_b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
url = f"https://mermaid.ink/img/{encoded_code}?type=png"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    print(f"Downloading ER Diagram from: {url}")
    with urllib.request.urlopen(req) as response, open("ER_Diagram.png", 'wb') as out_file:
        out_file.write(response.read())
    print("Successfully saved as ER_Diagram.png")
except Exception as e:
    print(f"Error downloading image: {e}")
