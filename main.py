import pandas as pd
import time
import matplotlib.pyplot as plt
from flask import Flask, render_template, send_file, request

app = Flask(__name__)

df = pd.read_csv("data/Gold.csv")
df['Year Open'] = df['Year Open'].astype(float)
df['Year Close'] = df['Year Close'].astype(float)
df['Year'] = df['Year'].astype(int)
df['Year High'] = df['Year High'].astype(float)
df['Year Low'] = df['Year Low'].astype(float)
df['Average\nClosing Price'] = df['Average\nClosing Price'].astype(float)
df['Annual\n% Change'] = df['Annual\n% Change'].astype(float)

links = {"Download data file (.csv)": "/download_data",
         "View Raw Data": "/view_data",
         "Num_Field": '/num_f',
         "Average Closing Price": "/average_closing_price",
         "Year Open Close": "/year_open_close",
         "Year High Low": "/year_high_low",
         "Average Year Open Price": "/average_year_open_price",
         "Annual change": "/annual_change",
         "Analysis": "/analysis"}


def render_index(image=None, html_string=None, filters=None, current_filter_value="", errors=[]):
    return render_template("index.html", links=links, image=image, code=time.time(), html_string=html_string, filters=filters, current_filter_value = current_filter_value, errors=errors)


@app.route('/', methods=['GET'])
def main_page():
    return render_index()


@app.route(links["Download data file (.csv)"], methods=['GET'])
def download_data():
    return send_file("data/Gold.csv", as_attachment=True)




@app.route(links["View Raw Data"], methods=['GET', 'POST'])
def view_data():
    df = pd.read_csv("data/Gold.csv")
    html_string = df.to_html()
    return render_index(html_string=html_string)


@app.route(links["Num_Field"], methods=['GET', 'POST'])
def num_f():
    des = df.describe()
    drop_list = ['25%', "max", "75%", "min", "count"]
    for i in drop_list:
        des = des.drop(i)
    des = des.reindex(["mean", "50%", "std"])
    des.index = ["mean", "median", "standard deviation"]
    html_string = des.to_html()
    return render_index(html_string=html_string)


@app.route(links["Average Closing Price"], methods=['GET'])
def average_closing_price():
    plt.figure(num=None, figsize=(12, 6), dpi=100, facecolor='w', edgecolor='k')
    plt.plot(df.groupby('Year')['Average\nClosing Price'].mean())
    plt.title('Average Closing Price')
    plt.xlabel('Year')
    plt.ylabel('Dollars')
    plt.savefig('static/tmp/average_closing_price.png')
    return render_index(("average_closing_price.png", "Average Closing Price"))


@app.route(links["Year Open Close"], methods=['GET'])
def year_open_close():
    df = pd.read_csv("data/Gold.csv")
    errors = []
    current_filter_value = ""
    if request.method == "POST":
        current_filter = request.form.get('filters')
        current_filter_value = current_filter
        if current_filter:
            try:
                df = df.query(current_filter)
            except Exception as e:
                errors.append('font color="red">Incorrect filter</font>')
                print(e)


    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(df.groupby('Year')['Year Open'].mean(), label="Year open")
    ax.plot(df.groupby('Year')['Year Close'].mean(), label="Year close")

    ax.legend(loc=2)
    ax.set_xlabel('Year')
    ax.set_ylabel('Dollars')
    ax.set_title('Price')
    plt.savefig('static/tmp/year_open_close.png')
    return render_index(("year_open_close.png", "Year Open Close"))


@app.route(links["Year High Low"], methods=['GET', 'POST'])
def year_high_low():
    df = pd.read_csv("data/Gold.csv")

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(df.groupby('Year')['Year High'].mean(), label="Year highest")
    ax.plot(df.groupby('Year')['Year Low'].mean(), label="Year lowest")

    ax.legend(loc=2)
    ax.set_xlabel('Year')
    ax.set_ylabel('Dollars')
    ax.set_title('Price')
    plt.savefig('static/tmp/year_high_low.png')
    return render_index(("year_high_low.png", "Year High Low"))


@app.route(links["Average Year Open Price"], methods=['GET'])
def average_year_open_price():
    plt.figure(num=None, figsize=(14, 6), dpi=100, facecolor='w', edgecolor='k')
    owner_list = list(df.groupby('Year')['Year Open'].mean().index)
    price_list = df.groupby('Year')['Year Open'].mean()
    plt.title('Average year open price')
    plt.ylabel('Dollars')
    plt.xlabel('Year')
    plt.bar(owner_list, price_list)
    plt.savefig('static/tmp/average_year_open_price.png')
    return render_index(("average_year_open_price.png", "Average Year Open Price"))


@app.route(links["Annual change"], methods=['GET'])
def annual_change():
    plt.figure(num=None, figsize=(14, 6), dpi=100, facecolor='w', edgecolor='k')
    owner_list = list(df.groupby('Year')['Annual\n% Change'].mean().index)
    price_list = df.groupby('Year')['Annual\n% Change'].mean()
    plt.title('Annual change')
    plt.ylabel('%')
    plt.xlabel('Year')
    plt.bar(owner_list, price_list)
    plt.savefig('static/tmp/annual_change.png')
    return render_index(("annual_change.png", "Annual change"))


@app.route(links["Analysis"], methods=['GET'])
def download_analysis():
    return render_index(("analysis.png", "Analysis"))


if __name__ == '__main__':
    app.run()