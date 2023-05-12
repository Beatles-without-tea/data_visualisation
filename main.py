from flask import Flask, render_template
import pandas as pd
import folium

app = Flask(__name__)

@app.route('/templates/map.html')
def show_map():
    return render_template('map.html')

@app.route('/')
def index():
    # Render the map HTML file
     # Define the title for the web page

    title = 'Paris Prices by Neighborhood'

    return render_template('main.html', title=title)

if __name__ == '__main__':
    app.run()
