from ast import GtE
from tracemalloc import start
from mcp.server.fastmcp import FastMCP
from datetime import datetime
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from typing import Optional 

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
expenses_collection = db["expenses"]


class Expense(BaseModel):
    amount: float
    category: str
    subcategory: str
    description: str
    date: Optional[str] = Field(default_factory=lambda: str(date.today()))

mcp = FastMCP("expense-tracker")

@mcp.tool()
def hello(name: str) -> str :
    """Say Hello """
    return f"Hello, {name} !!!!! Aeee"

@mcp.tool()
def test_db() :
    """ Tests db connection """
    count = expenses_collection.count_documents({})
    return f"Testing DB Connection : {count}"

#expenseList = []        ## Temporary Storage


CATEGORIES = [
    "food",
    "travel",
    "shopping",
    "rent",
    "bills",
    "entertainment",
    "health",
    "other"
]

@mcp.resource("expense://categories")
def getCategories() -> str :
    return "\n".join(CATEGORIES)

@mcp.tool()
def addExpense(amount, category, subcategory, description, date) :
    """ Add expense for user """
    expense = Expense(
        amount=amount,
        category=category,
        subcategory=subcategory,
        description=description,
        date=str(date) if date else str(datetime.now().date()),
    )

    expenses_collection.insert_one(expense.model_dump())
    #expenseList.append(expense)

    return f"Expense Added {description} : {amount}"


def listExpenseQuery(category:Optional[str], startDt:Optional[str], endDt:Optional[str]) -> dict :
    """ Method to return expenses based on category and optional date range """
    query = {}

    if category:
        query["category"] = category.lower().strip()
    
    if startDt or endDt:
        query["date"] = {}
        if startDt:
            query["date"]["$gte"] = startDt
        
        if endDt:
            query["date"]["$lte"] = endDt

    return query


@mcp.tool()
def listExpenses(category:Optional[str], startDt:Optional[str], endDt:Optional[str]) -> list :
    """ List expenses, optionally by category and within the date range, if specified """
    
    query = listExpenseQuery(category, startDt, endDt)
    
    docs = list(expenses_collection.find(query).sort("date", -1))
    for doc in docs:
        doc["_id"] = str(doc["_id"])
    
    return docs

@mcp.tool()
def getMonthlySummary(startDt:Optional[str], endDt:Optional[str]) :
    """Get total spending and category-wise breakdown for a date range."""

    pipeline = [
        {
            "$match": {
                "date": {
                    "$gte": startDt,
                    "$lte": endDt
                }
            }
        },
        {
            "$group": {
                "_id": "$category",
                "total": {"$sum": "$amount"}
            }
        }
    ]

    categoryData = list(expenses_collection.aggregate(pipeline))
    totalSpent = sum(item["total"] for item in categoryData)

    return {
        "startDate": startDt,
        "endDate": endDt,
        "totalSpent": totalSpent,
        "categoryBreakdown": categoryData
    }

if __name__ == "__main__":
    mcp.run()