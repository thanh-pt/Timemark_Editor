from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import os
import datetime

app = Flask(__name__)

localhost = True

UPLOAD_FOLDER = 'TimemarkEditor/static/uploads/'
OUTPUT_FOLDER = 'TimemarkEditor/static/outputs/'
if localhost:
    UPLOAD_FOLDER = 'static/uploads/'
    OUTPUT_FOLDER = 'static/outputs/'
FONT_REGR = 'RobotoCondensed-Regular.ttf'
FONT_BOLD = 'RobotoCondensed-Bold.ttf'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def dateToWeekday(date_str: str) -> str:
    day, month, year = map(int, date_str.split('/'))
    date_obj = datetime.date(year, month, day)
    weekdays = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
    return weekdays[date_obj.weekday()]

def drawText(draw, text: str, size: int, pos: tuple, color: tuple = (255, 255, 255), isBorder: bool = False, isBold: bool = False):
    if isBold: font = ImageFont.truetype(FONT_BOLD, size)
    else: font = ImageFont.truetype(FONT_REGR, size)
    if isBorder:
        border_color = (0, 0, 0)
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]:
            draw.text((pos[0] + dx, pos[1] + dy), text, fill=border_color, font=font)
    draw.text(pos, text, fill=color, font=font)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        uploaded_file = request.files['image']

        if uploaded_file.filename == '':
            return 'No file selected', 400

        input_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(input_path)

        image = Image.open(input_path)
        width, height = image.size
        if width > height:
            image = image.rotate(-90, expand=True)
            width, height = image.size
        if height > 2560:
            target_size = (1920, 2560)  # Kích thước mục tiêu
            image.thumbnail(target_size)  # Resize ảnh với tỷ lệ giữ nguyên
        draw = ImageDraw.Draw(image)

        drawText(draw, time, 235, (50, 2080), isBorder=True)
        drawText(draw, date, 68, (633, 2130))
        drawText(draw, dateToWeekday(date), 68, (633, 2220))
        draw.rectangle([(590, 2130), (600, 2304)], fill=(247, 197, 64))
        # Static object in image
        drawText(draw, "Trường Sa, X. Xuân Canh, H. Đông Anh, Thành Phố", 62, (50, 2357))
        drawText(draw, "Hà Nội", 62, (50, 2433))
        draw.rectangle([(590, 2130), (600, 2304)], fill=(247, 197, 64))

        drawText(draw, "Time", 60, (1655, 2415), (247, 197, 64), isBold = True)
        drawText(draw, "mark", 60, (1780, 2415), isBold = True)
        drawText(draw, "Ngày giờ chân thực", 40, (1600, 2490))

        # Lưu file đầu ra
        output_filename = 'output_' + uploaded_file.filename
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        image.save(output_path)

        # Trả về đường dẫn đến ảnh
        output_url = f'/static/outputs/{output_filename}'
        return {"output_url": output_url}, 200  # Trả về JSON chứa URL

    return render_template('index.html')

if __name__ == '__main__':
    if localhost:
        app.run(host='0.0.0.0', port=5000, debug=True)
    else: app.run()

