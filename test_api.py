"""
Script test API backend Flask
Chạy script này khi server Flask đang chạy để kiểm tra API
"""

import requests
import json

def test_api():
    # URL của API
    api_url = "http://127.0.0.1:5000/api/check"
    
    # Test cases
    test_urls = [
        "google.com",
        "facebook.com",
        "vnnic.vn",
        "example.com"
    ]
    
    print("=" * 60)
    print("KIỂM TRA API PHISHING URL DETECTION")
    print("=" * 60)
    print()
    
    for url in test_urls:
        print(f"Đang kiểm tra: {url}")
        print("-" * 60)
        
        try:
            # Gửi request
            response = requests.post(
                api_url,
                headers={"Content-Type": "application/json"},
                json={"url": url},
                timeout=30
            )
            
            # Kiểm tra response
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    print(f"✓ Kết quả: {'AN TOÀN' if data['is_safe'] else 'GIẢ MẠO'}")
                    print(f"  Tỷ lệ phishing: {data['phishing_probability']:.2f}%")
                    print(f"  Tỷ lệ an toàn: {data['safe_probability']:.2f}%")
                    print(f"  Loại tên miền: {data['domain_type']}")
                    print(f"  Domain: {data['domain']}")
                else:
                    print(f"✗ Lỗi: {data.get('error', 'Unknown error')}")
            else:
                print(f"✗ HTTP Error {response.status_code}")
                print(f"  Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("✗ Lỗi: Không thể kết nối đến server!")
            print("  Vui lòng chạy 'python app.py' trước.")
            break
        except requests.exceptions.Timeout:
            print("✗ Lỗi: Request timeout")
        except Exception as e:
            print(f"✗ Lỗi: {str(e)}")
        
        print()
    
    print("=" * 60)
    print("HOÀN THÀNH KIỂM TRA")
    print("=" * 60)

if __name__ == "__main__":
    print("\n⚠️  Lưu ý: Đảm bảo Flask server đang chạy (python app.py)\n")
    input("Nhấn Enter để bắt đầu test...")
    print()
    test_api()

