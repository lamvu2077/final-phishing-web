#importing required libraries

from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import whois
from datetime import datetime
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/api/check", methods=["POST"])
def check_url():
    try:
        data = request.get_json()
        url = data.get("url", "")
        
        if not url:
            return jsonify({
                "success": False,
                "error": "URL không được để trống"
            }), 400
        
        # Thêm http:// nếu URL không có protocol
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Trích xuất đặc trưng
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 
        
        # Dự đoán
        y_pred = gbc.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        
        # Lấy thông tin WHOIS
        whois_data = {}
        try:
            w = whois.whois(obj.domain)
            
            # Xử lý domain_name
            domain_name = str(w.domain_name) if w.domain_name else "Không có thông tin"
            if isinstance(w.domain_name, list):
                domain_name = str(w.domain_name[0]) if w.domain_name else "Không có thông tin"
            
            # Xử lý registrar
            registrar = str(w.registrar) if w.registrar else "Không có thông tin"
            
            # Xử lý creation_date
            creation_date = "Không có thông tin"
            if w.creation_date:
                if isinstance(w.creation_date, list):
                    creation_date = w.creation_date[0].strftime("%d-%m-%Y") if w.creation_date[0] else "Không có thông tin"
                else:
                    creation_date = w.creation_date.strftime("%d-%m-%Y")
            
            # Xử lý expiration_date
            expiration_date = "Không có thông tin"
            if w.expiration_date:
                if isinstance(w.expiration_date, list):
                    expiration_date = w.expiration_date[0].strftime("%d-%m-%Y") if w.expiration_date[0] else "Không có thông tin"
                else:
                    expiration_date = w.expiration_date.strftime("%d-%m-%Y")
            
            # Xử lý name_servers - chuyển thành list of strings
            name_servers = []
            if w.name_servers:
                if isinstance(w.name_servers, list):
                    name_servers = [str(ns) for ns in w.name_servers]
                else:
                    name_servers = [str(w.name_servers)]
            
            # Xử lý status - chuyển thành string hoặc list of strings
            status = "Không có thông tin"
            if w.status:
                if isinstance(w.status, list):
                    status = [str(s) for s in w.status]
                else:
                    status = str(w.status)
            
            # Xử lý emails - chuyển thành list of strings
            emails = []
            if w.emails:
                if isinstance(w.emails, list):
                    emails = [str(e) for e in w.emails]
                elif isinstance(w.emails, str):
                    emails = [w.emails]
                else:
                    emails = [str(w.emails)]
            
            # Xử lý org
            org = str(w.org) if hasattr(w, 'org') and w.org else "Không có thông tin"
            
            whois_data = {
                "domain_name": domain_name,
                "registrar": registrar,
                "creation_date": creation_date,
                "expiration_date": expiration_date,
                "name_servers": name_servers,
                "status": status,
                "emails": emails,
                "org": org
            }
                
        except Exception as e:
            whois_data = {
                "error": "Không thể truy xuất thông tin WHOIS",
                "domain_name": obj.domain,
                "registrar": "Không có thông tin",
                "creation_date": "Không có thông tin",
                "expiration_date": "Không có thông tin",
                "org": "Không có thông tin"
            }
        
        # Xác định loại tên miền
        domain_type = "Tên miền quốc tế"
        if '.vn' in obj.domain:
            if '.gov.vn' in obj.domain:
                domain_type = "Tên miền cơ quan nhà nước .GOV.VN"
            elif '.edu.vn' in obj.domain:
                domain_type = "Tên miền giáo dục .EDU.VN"
            else:
                domain_type = "Tên miền quốc gia .VN"
        
        return jsonify({
            "success": True,
            "url": url,
            "domain": obj.domain,
            "prediction": int(y_pred),
            "is_safe": bool(y_pred == 1),  # Convert numpy.bool_ to Python bool
            "phishing_probability": float(y_pro_phishing * 100),
            "safe_probability": float(y_pro_non_phishing * 100),
            "domain_type": domain_type,
            "whois": whois_data
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Lỗi khi xử lý: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)