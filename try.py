import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/weather', methods=['GET'])
def get_weather():
    api_key = 'a40a08819e2ca4455e9badc3a50026b6'
    province = request.args.get('province', 'Quang Tri')
    
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={province},vietnam&appid={api_key}&units=metric&lang=vi'
    response = requests.get(url)
    data = response.json()

    if data and 'list' in data:
        list_day = []
        for entry in data['list']:
            date = entry['dt_txt']
            time_str = date[11:]
            
            if time_str == '12:00:00':
                icon = entry['weather'][0]['icon']
                image_url = {
                    '01n': 'https://i.imgur.com/J3a135c.jpg',
                    '02n': 'https://i.imgur.com/CRh04K2.jpg',
                    '03n': 'https://i.imgur.com/b5BKa4x.jpg',
                    '04n': 'https://i.imgur.com/CRh04K2.jpg',
                    '09n': 'https://i.imgur.com/XHUnTV6.jpg',
                    '10n': 'https://i.imgur.com/7ECPQGA.jpg',
                    '11n': 'https://i.imgur.com/dMj6Rt9.jpg',
                }.get(icon, '')
                
                list_day.append({
                    'title': f"Ngày {date[:10]}",
                    'image_url': image_url,
                    'subtitle': f"\nNhiệt độ trung bình: {int(entry['main']['temp'])}°C \n"
                                f"Độ ẩm: {entry['main']['humidity']}% \n"
                                f"Tình trạng thời tiết: {entry['weather'][0]['description'].capitalize()}"
                })

        result = {
            "messages": [
                {"text": f"Bạn đã tra cứu dữ liệu thời tiết cho {province}. Dưới đây là thông tin thời tiết của 5 ngày tới."},
                {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": list_day
                        }
                    }
                }
            ]
        }
    else:
        result = {
            "messages": [
                {"text": "Không tìm thấy dữ liệu của thành phố bạn tra cứu 🙁 \nVui lòng thử tìm thành phố lân cận khác."}
            ]
        }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)