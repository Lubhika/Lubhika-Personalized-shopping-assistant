from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Initialize shopping list DataFrame
items_df = pd.DataFrame(columns=['Item', 'Cost'])

@app.route('/')
def index():
    items = items_df.to_dict(orient='records')
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    item_name = request.form.get('item')
    cost = request.form.get('cost')
    if item_name and cost:
        try:
            cost = float(cost)
            global items_df
            new_item = pd.DataFrame([{'Item': item_name, 'Cost': cost}])
            items_df = pd.concat([items_df, new_item], ignore_index=True)
        except ValueError:
            pass
    return redirect(url_for('index'))

@app.route('/remove', methods=['POST'])
def remove_item():
    item_name = request.form.get('item')
    global items_df
    items_df = items_df[items_df['Item'] != item_name]
    return redirect(url_for('index'))

@app.route('/view', methods=['GET'])
def view_list():
    items = items_df.to_dict(orient='records')
    return render_template('index.html', items=items)

@app.route('/total', methods=['GET'])
def view_total_cost():
    total_cost = items_df['Cost'].sum()
    items = items_df.to_dict(orient='records')
    return render_template('index.html', items=items, total_cost=total_cost)

@app.route('/sort', methods=['POST'])
def sort_items():
    sort_by = request.form.get('sort_by')
    global items_df
    if sort_by == 'Item':
        items_df = items_df.sort_values(by='Item').reset_index(drop=True)
    elif sort_by == 'Cost':
        items_df = items_df.sort_values(by='Cost').reset_index(drop=True)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
