from flask import Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
app_url = "http://165.192.69.52:8003/oslc/spq/GetLeaseRecords?oslc.select=*"
auth = HTTPBasicAuth("20529345", "MOhan@1")

@app.route("/", methods=["GET"])
def get_lease_record():
    name = request.args.get("name")
    try:
        response = requests.get(app_url, auth=auth)
        response.raise_for_status()
        data = response.json()

        lease_record = next((item for item in data["rdfs:member"] if item.get("spi:triNameTX") == name), None)

        if lease_record:
            lease_name = lease_record["spi:triNameTX"]
            lease_status = lease_record["spi:triStatusCL"]
            start_date = lease_record.get("spi:triStartDA")  
            end_date = lease_record.get("spi:triAccountingEndDateDA")  
            
            return jsonify({
                "lease_name": lease_name,
                "lease_status": lease_status,
                "start_date": start_date,
                "end_date": end_date
            }), 200
        else:
            return jsonify({"error": "Lease record not found"}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
