# 💸 Expense Tracker MCP (Python + MongoDB)

A simple yet powerful expense tracking system built using **FastMCP**, **MongoDB**, and **Python**.
This project demonstrates how to build **LLM-integrated tools (MCP)** along with a clean backend for real-world usage.

---

## 🚀 Features

* Add expenses with natural fields (amount, category, description, date)
* Fetch expenses (all / filtered by category or date range)
* Monthly summary with category-wise breakdown
* Delete expenses
* MongoDB persistence
* MCP (Model Context Protocol) compatible tools
* CLI mode for testing without Cursor

---

## 🧱 Tech Stack

* Python (uv project)
* FastMCP
* MongoDB (Atlas or local)
* Pydantic (validation)
* PyMongo

---

## ⚙️ Setup

### 1. Clone repo

```bash
git clone https://github.com/nihaar6601/expense-tracker-mcp.git
cd expense-tracker-mcp
```

---

### 2. Install dependencies (using uv)

```bash
uv sync
```

---

### 3. Setup environment variables

Create `.env` file:

```env
MONGODB_URI=your_mongodb_connection_string
DB_NAME=expense_tracker
```

---

### 4. Run project

```bash
uv run server.py
```

---

## 🧠 Available Tools

### ➕ Add Expense

```python
add_expense(amount, category, description, subcategory=None, date=None)
```

---

### 📋 List Expenses

```python
listExpenses(category=None, start_date=None, end_date=None)
```

---

### 📊 Monthly Summary

```python
get_monthly_summary(start_date, end_date)
```

Returns:

* total spent
* category-wise breakdown

---

### ❌ Delete Expense

```python
delete_expense(expense_id)
```

---

## 🧠 MCP Integration

This project is MCP-compatible.

Example tool usage (via LLM):

```
Add 500 for bus travel yesterday
Show my expenses in September 2025
Delete my last expense
```

---

## 🗄️ MongoDB Schema

Example document:

```json
{
  "_id": ObjectId,
  "amount": 500,
  "category": "travel",
  "subcategory": "bus",
  "description": "Mumbai to Goa",
  "date": "2026-03-22"
}
```

---

## 🔥 Key Concepts Demonstrated

* MCP tool creation
* MongoDB querying (`find`, `aggregate`)
* Aggregation pipeline (`$match`, `$group`)
* Dynamic query building
* LLM + backend interaction design

---

## 📈 Future Improvements

* Update expense
* Payment methods (UPI, card, cash)
* Tags support
* User authentication
* Analytics (daily trends, highest spend)
* Natural language date parsing
* REST API layer

---

## 🤝 Contribution

Feel free to fork and extend. This is a great base for:

* AI agents
* personal finance apps
* backend system design practice
