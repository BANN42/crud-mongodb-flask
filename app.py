from flask import Flask, render_template, request, redirect, url_for

from pymongo import MongoClient
from bson import ObjectId

# MongoDB connection details (replace with yours)
client = MongoClient("mongodb://localhost:27017")
db = client["flasker"]
collection = db["users"]

app = Flask(__name__)

# CRUD routes (implemented previously)
@app.route('/', methods=['GET'])
def welcom():
    return render_template('greeting.html')
# lister
@app.route("/items", methods=["GET"])
def list_items():
    items = list(collection.find())  # Convert cursor to list
    return render_template("list_items.html", items=items)

# Route for adding items (GET to display form, POST to handle submission)
@app.route("/add", methods=["GET", "POST"])
def add_item():
    if request.method == "GET":
        return render_template("add_item.html")  # Render add item form
    if request.method == "POST":
        data = request.form  # Get data from form fields
    # Assuming form fields are named "name" and "description"
        new_item = {
        "name": data["name"],
        "description": data["description"],
    }
        collection.insert_one(new_item)
        return redirect(url_for("list_items")) 

# editing
@app.route("/edit/<item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    if request.method == "GET":
        # Find the item based on ID
        item = collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            # Handle case where item not found (optional: error message)
            return "Item not found!"
        return render_template("edit_item.html", item=item)

    else:  # Handle edit form submission (POST)
        data = request.form
        print(f"Received form data: {data}")
        updated_data = {"$set": {"name": data["name"], "description": data["description"]}}
        collection.find_one_and_update({"_id": ObjectId(item_id)}, updated_data)
        return redirect(url_for("list_items")) 


#delete item
@app.route("/delete/<item_id>", methods=["GET", "POST"])  # Can use POST for confirmation
def delete_item(item_id):
    if request.method == "GET":  # Confirmation step (optional)
        item = collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            return "Item not found!"
        return render_template("delete_confirmation.html", item=item)  # Optional confirmation template
    else:  # Handle deletion confirmation (optional, or handle directly in GET)
        collection.delete_one({"_id": ObjectId(item_id)})
        return redirect(url_for("list_items"))  # Redirect to list view after deletion
#Registration
#login
#

if __name__ == "__main__":
    app.run(debug=True)
