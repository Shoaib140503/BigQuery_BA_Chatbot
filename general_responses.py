def handle_general_queries(user_query: str):
    """Handles general queries like greetings, bot introduction, objectives, and business concepts."""
    user_query = user_query.lower()

    general_responses = {
        # 🔹 Greetings & Formal Queries
        "hello": "Hello! How can I assist you today?",
        "hey": "Hey! How can I help with your business analytics?",
        "how are you": "I'm just a bot, but I'm always ready to help!",
        "who are you": "I am InsightBot, your AI-powered business analytics assistant!",
        "what is your name": "I am InsightBot, your AI-powered business analytics assistant!",
        "what is your objective": "My goal is to help you analyze business data, generate SQL queries, and provide meaningful insights from BigQuery.",
        "what can you do": "I can generate optimized SQL queries, analyze business trends, and help with sales, inventory, and customer insights!",
        "thank you": "You're welcome! Let me know if you need anything else.",
        "bye": "Goodbye! Have a great day!",

        # 🔹 Business & Finance Terms
        "what is revenue": "Revenue is the total income generated from sales before expenses are deducted. It is calculated as 'Total Sales × Price per Unit'.",
        "what is gross profit": "Gross profit is revenue minus the cost of goods sold (COGS). It shows how much profit a business makes after covering direct production costs.",
        "what is net profit": "Net profit is the final profit after deducting all expenses, including operating costs, taxes, and interest. It represents the actual earnings of a business.",
        "what is customer retention rate": "Customer retention rate measures the percentage of customers who continue doing business with you over a given period. It's a key indicator of business stability.",
        "what is average order value": "Average Order Value (AOV) is the average amount spent per transaction, calculated as 'Total Revenue ÷ Number of Orders'.",
        "what is inventory turnover": "Inventory turnover measures how quickly inventory is sold and replaced. A high turnover indicates strong sales, while a low turnover may signal overstocking or slow sales.",

        # 🔹 Business Best Practices
        "how can i increase sales": "To increase sales, consider running promotions, optimizing pricing strategies, improving customer service, and enhancing marketing efforts.",
        "how can i reduce inventory costs": "Reducing inventory costs can be achieved by optimizing stock levels, negotiating better supplier deals, and minimizing excess stock with demand forecasting.",
        "how can i improve customer retention": "Customer retention can be improved by offering loyalty programs, personalized recommendations, excellent customer service, and follow-up engagement.",
        "how to optimize pricing strategy": "Pricing optimization involves analyzing competitor pricing, demand patterns, and customer preferences to set the most profitable price points.",

        # 🔹 Market Trends & Competitor Insights
        "how do i analyze market trends": "Analyzing market trends involves tracking sales patterns, studying customer behavior, monitoring competitor actions, and leveraging external market data.",
        "how do i compare my business to competitors": "Compare business performance using industry benchmarks, competitor sales data, and customer feedback analysis.",
        "what are key performance indicators for e-commerce": "Key KPIs include conversion rate, customer lifetime value (CLV), return on investment (ROI), cart abandonment rate, and churn rate.",

        # 🔹 E-commerce & Retail-Specific Queries
        "why are my sales declining": "Sales decline can result from seasonal changes, increased competition, pricing issues, or poor customer engagement. Analyzing sales trends can help identify the cause.",
        "how do i identify my top-selling products": "Top-selling products can be identified by analyzing sales volume, revenue, and customer demand over time.",
        "how can i reduce cart abandonment": "Cart abandonment can be reduced by offering free shipping, simplifying the checkout process, and sending reminder emails to potential customers.",
        "how can i improve inventory forecasting": "Accurate inventory forecasting requires analyzing past sales data, seasonality trends, and demand fluctuations to optimize stock levels."
    }

    # Check if the user query matches any predefined responses
    for key in general_responses:
        if key in user_query:
            return general_responses[key]

    return None  # Return None if the query is not a general question