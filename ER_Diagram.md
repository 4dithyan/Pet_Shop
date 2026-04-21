# 🐾 Pet Shop — Entity Relationship (ER) Diagram

This document contains the Entity Relationship (ER) Diagram for the Pet Shop Management System database.

## 📊 ER Diagram

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

    %% Relationships
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
