| KPI | What it measures | Which tables |
|------|------------------|--------------|
| Total revenue | Sum of all payment values | `payments` |
| Average order value | Revenue ÷ number of orders | `payments` + `orders` |
| Monthly order volume | Count of orders per month | `orders` |
| On-time delivery rate | % of orders delivered before the estimated delivery date | `orders` |
| Average delivery days | Days from purchase to delivery | `orders` |
| Average review score | Mean of `review_score` (1–5) | `reviews` |
| Repeat customer rate | % of customers with more than one order | `customers` + `orders` |
| Revenue by category | Revenue split by product category | `order_items` + `products` + `translation` |
