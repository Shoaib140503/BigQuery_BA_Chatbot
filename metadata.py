"""
Metadata Definitions for BigQuery Dataset
Project: windy-skyline-453612-q2
Dataset: data_for_testing
Table: shopify_sales
"""

# Dimensions (Used for grouping, filtering, and segmentation)
DIMENSIONS = {
    "is_returning_customer_readable": "Indicates whether customer is returning or first-time.",
    "billingAddress_province": "Returns the value of the Region field of the address.",
    "billingAddress_zip": "The postal code (zip, postcode, or Eircode) of the billing address.",
    "customer_id": "The unique identifier of a customer. This field contains Shopify's path and source.",
    "date": "The month, date, year, and hour.",
    "discountCode": "The discount code applied when completing a purchase.",
    "name": "Returns the name of the order in the format set in the Standards & formats section of the General Settings of your Shopify admin.",
    "order_id": "The unique identifier of an order.",
    "productType": "The type of product you are selling. For example, hats, shirts, or shoes.",
    "product_id": "The unique identifier of the product.",
    "sku": "A unique code consisting of letters and numbers that identify characteristics about each product, such as manufacturer, brand, style, color, and size.",
    "title": "The name for your product.",
    "variantTitle": "The name for your product's variant.",
    "date_actual": "The dimension that determines how date-based data in a chart is handled.",
}

# Metrics (Numerical values used for calculations and aggregation)
METRICS = {
    "inventoryQuantity": "The product quantity in inventory.",
    "line_item_amount": "The price of the item sold.",
    "line_item_discount": "The discount provided for the individual SKU or variant.",
    "line_item_gross_amount": "Equates to product price x quantity (before taxes, shipping, discounts, and returns). Canceled, pending, and unpaid orders are included. Test and deleted orders are not included.",
    "line_item_net_amount": "Line Item Net Amount = Line Item Amount - Line Item Taxes - Line Item Discount.",
    "line_item_return": "The return value of the individual SKU or variant.",
    "line_item_shipping": "The shipping amount of the individual SKU or variant.",
    "line_item_taxes": "Taxes paid for the item.",
    "line_item_total_amount": "Equates to gross sales - discounts - returns + taxes + duties + shipping charges.",
    "on_hand": "Quantity of inventory on hand.",
    "orders": "When used with Order ID dimension, this metric indicates whether this is an order (1) or a return (0).",
    "price": "The selling price for an item before any applicable discounts.",
    "quantity": "The quantity of items sold.",
    "totalInventory": "Total inventory for an item.",
}

# Full Metadata Dictionary for Summarization
FULL_METADATA = {**DIMENSIONS, **METRICS}