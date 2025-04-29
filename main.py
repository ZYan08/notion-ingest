import os 
import dotenv
import csv
from notion_client import Client
from data import USER_LIST

dotenv.load_dotenv()

DATABASE_ID = os.getenv("DATABASE_ID")
NOTION_TOKEN = os.getenv("NOTION_API_KEY")

notion_data = []

client = Client(auth=NOTION_TOKEN)
response = client.databases.query(database_id=DATABASE_ID)

database = response.get("results", [])
headers = list(database[0]["properties"].keys())
row_data = []
name = headers[-1]
user_lookup = {user.name.lower(): user.discord_id for user in USER_LIST}

for data in database:
    row = {}
    for header in headers:
        prop = data["properties"].get(header, "N/A")
        value = ""

        if prop.get("type") == "title":
            value = "".join([x["plain_text"] for x in prop.get("title", [])])
        elif prop.get("type") == "rich_text":
            value = "".join([x["plain_text"] for x in prop.get("rich_text", [])])
        elif prop.get("type") == "select":
            value = prop["select"]["name"] if prop.get("select") else ""
        elif prop.get("type") == "multi_select":
            value = ", ".join(tag["name"] for tag in prop.get("multi_select", []))
        elif prop.get("type") == "email":
            value = prop.get("email", "")
        elif prop.get("type") == "date":
            value = prop["date"]["start"] if prop.get("date") else ""
        elif prop.get("type") == "checkbox":
            value = str(prop.get("checkbox", ""))
        elif prop.get("type") == "url":
            value = prop.get("url", "")
        else:
            value = ""

        row[header] = value
    person_name = row.get(name, "").lower()
    row["Discord Tag"] = user_lookup.get(person_name, "")
    row_data.append(row)
    
with open("notion_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(row_data)
    


