import os
from flask import Flask, render_template, send_file, jsonify
from scraper import run_scraper_and_generate_excel

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        excel_buffer, item_count = run_scraper_and_generate_excel()
        if excel_buffer is None:
            return jsonify({"error": "No relevant data found or empty results."}), 404
        
        return send_file(
            excel_buffer,
            download_name="filtered_apify_results.xlsx",
            as_attachment=True,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
