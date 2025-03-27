Here’s a list of user prompts categorized by query type (Aggregate, Analytical, Predictive, and Miscellaneous) to test your FinWhiz application. These prompts are designed to exercise different aspects of your PostgreSQL `transactions` table schema and the chatbot’s ability to generate SQL and interpret results. I’ve corrected your typos ("Aggrgrtae" → Aggregate, "tupes" → types, "qurties" → queries) and provided a variety of examples.

---

### Aggregate Queries
These queries involve summarizing or grouping data (e.g., SUM, COUNT, AVG).

1. **"What’s the total amount I spent this month?"**
   - Tests summing amounts with a date filter.
2. **"How much did I spend on food in March 2025?"**
   - Tests category filtering and monthly aggregation.
3. **"What’s the average expense per category this year?"**
   - Tests AVG with GROUP BY and a year-long filter.
4. **"How many transactions did I have this week?"**
   - Tests COUNT with a weekly date range.
5. **"What’s the total I owe others this month?"**
   - Tests summing `who_owes_how_much` with a date filter.

---

### Analytical Queries
These queries involve comparisons, rankings, or detailed breakdowns.

6. **"What was my biggest expense this month?"**
   - Tests ORDER BY with LIMIT (already working in your logs).
7. **"What was my lowest expense this month?"**
   - Tests ORDER BY ASC with LIMIT.
8. **"Which category do I spend the most on this year?"**
   - Tests GROUP BY with ORDER BY SUM(amount) DESC and LIMIT.
9. **"What’s the difference between my debits and credits this month?"**
   - Tests conditional SUM with debit_credit comparison.
10. **"Who did I pay the most to in the last 3 months?"**
    - Tests GROUP BY `paid_to` with ORDER BY SUM(amount) DESC.

---

### Predictive Queries
These queries ask for trends or future insights, though your current schema lacks predictive models. The chatbot might infer trends or return "insufficient data" if it can’t predict.

11. **"What will my biggest expense be next month?"**
    - Tests if the chatbot can infer trends (likely needs historical extrapolation).
12. **"How much will I spend on groceries in April 2025?"**
    - Tests predictive logic based on past category spending.
13. **"Am I spending more this month than last month?"**
    - Tests month-over-month comparison (analytical but with a predictive tone).
14. **"What’s my predicted total spending for the rest of the year?"**
    - Tests extrapolation from current yearly data.
15. **"Will I owe more money next month?"**
    - Tests trend analysis on `i_owe_how_much`.

---

### Miscellaneous Queries
These test edge cases, natural language understanding, or specific fields.

16. **"Show me all my healthcare expenses this month."**
    - Tests filtering by category with a date range.
17. **"What did I spend on March 15, 2025?"**
    - Tests exact date filtering.
18. **"Who owes me money from last month?"**
    - Tests `who_owes_how_much` with a date filter.
19. **"List my credit transactions this week."**
    - Tests `debit_credit = 'credit'` with a weekly range.
20. **"What are my notes for expenses over $50 this month?"**
    - Tests filtering by amount and selecting the `notes` field.
