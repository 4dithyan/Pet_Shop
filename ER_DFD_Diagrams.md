# 🐾 Pet Shop — ER Diagram & Data Flow Diagram (DFD)

---

## 📊 Entity Relationship (ER) Diagram

```mermaid
erDiagram
    USER {
        bigint id PK
        string username
        string email
        string password
        string phone
        string role
        boolean is_staff
        boolean is_superuser
    }

    PROFILE {
        bigint id PK
        bigint user_id FK
        string image
        text address
        string city
        string state
        string pincode
        datetime created_at
        datetime updated_at
    }

    CATEGORY {
        bigint id PK
        string name
        string slug
        text description
        datetime created_at
    }

    PET {
        bigint id PK
        string name
        bigint category_id FK
        string breed
        int age_months
        string gender
        decimal price
        text description
        boolean is_vaccinated
        boolean is_available
        string image
        datetime created_at
        datetime updated_at
    }

    PRODUCT_CATEGORY {
        bigint id PK
        string name
        string slug
        datetime created_at
    }

    PRODUCT {
        bigint id PK
        string name
        bigint category_id FK
        text description
        decimal price
        int stock_quantity
        int low_stock_threshold
        string image
        datetime created_at
        datetime updated_at
    }

    INVENTORY_LOG {
        bigint id PK
        bigint product_id FK
        string change_type
        int quantity_change
        int previous_quantity
        int new_quantity
        string reason
        bigint created_by FK
        datetime created_at
    }

    ORDER {
        bigint id PK
        string order_number
        bigint user_id FK
        decimal total_amount
        string status
        string payment_method
        text shipping_address
        string phone
        string email
        datetime created_at
        datetime updated_at
    }

    ORDER_ITEM {
        bigint id PK
        bigint order_id FK
        bigint product_id FK
        int quantity
        decimal price
    }

    APPOINTMENT {
        bigint id PK
        bigint user_id FK
        string service_type
        string pet_name
        date appointment_date
        time appointment_time
        string status
        text notes
        datetime created_at
    }

    REVIEW {
        bigint id PK
        bigint user_id FK
        bigint product_id FK
        bigint pet_id FK
        int rating
        text comment
        datetime created_at
    }

    USER ||--|| PROFILE : "has one"
    USER ||--o{ ORDER : "places"
    USER ||--o{ APPOINTMENT : "books"
    USER ||--o{ REVIEW : "writes"
    USER ||--o{ INVENTORY_LOG : "logs"
    CATEGORY ||--o{ PET : "contains"
    PRODUCT_CATEGORY ||--o{ PRODUCT : "contains"
    PRODUCT ||--o{ ORDER_ITEM : "included in"
    PRODUCT ||--o{ INVENTORY_LOG : "tracked by"
    PRODUCT ||--o{ REVIEW : "reviewed in"
    ORDER ||--o{ ORDER_ITEM : "has"
    PET ||--o{ REVIEW : "reviewed in"
```

---

## 🔄 DFD — Level 0 : Context Diagram

```mermaid
flowchart TD
    Customer(["👤 Customer"])
    Staff(["👨‍💼 Staff / Admin"])
    System(["🐾 Pet Shop System"])
    DB[("🗄️ MySQL Database")]
    Email(["📧 Gmail SMTP"])

    Customer -->|"Register / Browse / Order / Book / Review"| System
    Staff -->|"Manage Pets / Products / Orders / Appointments"| System
    System -->|"Pages / Confirmations / Alerts"| Customer
    System -->|"Send OTP Email"| Email
    Email -->|"OTP Delivered to User"| Customer
    System <-->|"Read / Write Data"| DB
```

---

## 🔄 DFD — Level 1 : Main Processes

```mermaid
flowchart TD
    Customer(["👤 Customer"])
    Staff(["👨‍💼 Staff"])

    P1["1️⃣ User Authentication\nRegister, OTP, Login, Logout"]
    P2["2️⃣ Browse Pets & Products\nSearch, Filter, View Detail"]
    P3["3️⃣ Cart Management\nAdd, Remove, View Cart"]
    P4["4️⃣ Checkout & Order\nPlace Order, Pay, Track Status"]
    P5["5️⃣ Appointment Booking\nBook, View, Cancel"]
    P6["6️⃣ Reviews\nRate Products & Pets"]
    P7["7️⃣ Admin Dashboard\nManage All Data"]

    DS1[("auth_user\nuser_profiles")]
    DS2[("categories\npets\nproduct_categories\nproducts")]
    DS3[("Session Storage\nCart")]
    DS4[("orders\norder_items\ninventory_logs")]
    DS5[("appointments")]
    DS6[("reviews")]

    Customer --> P1
    Customer --> P2
    Customer --> P3
    Customer --> P4
    Customer --> P5
    Customer --> P6
    Staff --> P7

    P1 <--> DS1
    P2 <--> DS2
    P3 <--> DS3
    P4 <--> DS4
    P4 --> DS3
    P5 <--> DS5
    P6 <--> DS6
    P7 <--> DS1
    P7 <--> DS2
    P7 <--> DS4
    P7 <--> DS5
```

---

## 🔄 DFD — Level 2 : Registration & OTP Flow

```mermaid
flowchart TD
    A(["👤 User"]) -->|"Fills Registration Form"| B["Validate Form Data"]
    B -->|"Invalid"| A
    B -->|"Valid"| C["Generate 6-digit OTP"]
    C --> D["Store OTP + Form Data in Session"]
    D --> E["Send OTP via Gmail SMTP"]
    E --> F(["📧 User Email Inbox"])
    F -->|"User Enters OTP"| G["Verify OTP"]
    G -->|"OTP Wrong"| H["Show Error Message"]
    H --> F
    G -->|"OTP Matched"| I["Create User in Database"]
    I --> J["Clear Session Data"]
    J --> K["Auto Login User"]
    K --> L(["✅ Redirect to Home Page"])
```

---

## 🔄 DFD — Level 2 : Checkout & Order Flow

```mermaid
flowchart TD
    A(["👤 Customer"]) -->|"Goes to Checkout Page"| B{"Is Cart Empty?"}
    B -->|"Yes"| C["Redirect to Products Page"]
    B -->|"No"| D["Show Checkout Form\nEmail, Phone, Address, Payment"]
    D -->|"Submit Form"| E["Validate Form Data"]
    E -->|"Invalid"| D
    E -->|"Valid"| F["Create Order Record in DB"]
    F --> G["Loop Through Each Cart Item"]
    G --> H["Create OrderItem Record"]
    H --> I["Reduce Product Stock"]
    I --> J["Log Inventory Change"]
    J -->|"More Items?"| G
    J -->|"All Done"| K["Clear Cart from Session"]
    K --> L["Show Success Message"]
    L --> M(["✅ Redirect to Order Confirmation Page"])
```

---

## 🔄 DFD — Level 2 : Appointment Booking Flow

```mermaid
flowchart TD
    A(["👤 Customer"]) -->|"Clicks Book Appointment"| B["Show Appointment Form"]
    B -->|"Fills & Submits Form"| C["Validate Form Data"]
    C -->|"Invalid"| B
    C -->|"Valid"| D["Save Appointment\nStatus = Pending"]
    D --> E["Redirect to My Appointments List"]
    E --> F(["👨‍💼 Staff Reviews Appointment"])
    F -->|"Changes Status"| G{"New Status?"}
    G -->|"Approved"| H["status = Approved"]
    G -->|"Completed"| I["status = Completed"]
    G -->|"Cancelled"| J["status = Cancelled"]
```

---

## 🔄 DFD — Level 2 : Review Submission Flow

```mermaid
flowchart TD
    A(["👤 Logged-in Customer"]) -->|"Opens Product or Pet Page"| B{"Already Reviewed?"}
    B -->|"Yes"| C["Show Warning\nRedirect Back"]
    B -->|"No"| D["Show Review Form\nRating + Comment"]
    D -->|"Submit"| E["Validate Form"]
    E -->|"Invalid"| D
    E -->|"Valid"| F["Save Review to DB\nLinked to User + Product/Pet"]
    F --> G(["✅ Redirect to Product or Pet Detail Page"])
```

---

## 📌 Table Relationship Summary

| Table | Relates To | Relationship |
|---|---|---|
| `auth_user` | `user_profiles` | One to One |
| `auth_user` | `orders` | One to Many |
| `auth_user` | `appointments` | One to Many |
| `auth_user` | `reviews` | One to Many |
| `auth_user` | `inventory_logs` | One to Many |
| `categories` | `pets` | One to Many |
| `product_categories` | `products` | One to Many |
| `products` | `order_items` | One to Many |
| `products` | `inventory_logs` | One to Many |
| `products` | `reviews` | One to Many |
| `orders` | `order_items` | One to Many |
| `pets` | `reviews` | One to Many |
