from PIL import Image, ImageDraw, ImageFont
import os, sys
import datetime
import calendar

# Thiết lập đường dẫn hiện tại
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dir)


# Date time input
date = "15/01/2025"
time = "17:32"
# image input
image_path = "img.jpg"
output_path = "output_image.jpg"

# init image, draw, font path
image = Image.open(image_path)
draw = ImageDraw.Draw(image)
font_regr = "RobotoCondensed-Regular.ttf"
font_bold = "RobotoCondensed-Bold.ttf"

def dateToWeekday(date_str: str) -> str:
    day, month, year = map(int, date_str.split('/'))
    date_obj = datetime.date(year, month, day)
    weekday = date_obj.weekday()

    weekdays = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
    return weekdays[weekday]

def drawText(draw, text: str, size: int, pos: tuple, color: tuple = (255, 255, 255), isBorder:bool = False, isBold:bool=False):
    if isBold:
        font = ImageFont.truetype(font_bold, size)
    else: font = ImageFont.truetype(font_regr, size)
    if isBorder:
        border_color = (0, 0, 0)
        border_width = 2
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]:
            draw.text((pos[0] + dx, pos[1] + dy), text, fill=border_color, font=font)
    # Vẽ chữ chính
    draw.text(pos, text, fill=color, font=font)



# date & time
drawText(draw, time                 , 235, (50, 2080), isBorder = True)
drawText(draw, date                 , 68 , (633, 2130))
drawText(draw, dateToWeekday(date)  , 68 , (633, 2220))

# Static object in image
drawText(draw, "Trường Sa, X. Xuân Canh, H. Đông Anh, Thành Phố", 62, (50, 2357))
drawText(draw, "Hà Nội", 62, (50, 2433))
draw.rectangle([(590, 2130), (600, 2304)], fill=(247, 197, 64))

drawText(draw, "Time", 60, (1655, 2415), (247, 197, 64), isBold = True)
drawText(draw, "mark", 60, (1780, 2415), isBold = True)
drawText(draw, "Ngày giờ chân thực", 40, (1600, 2490), isBold = True)

# Lưu ảnh mới
image.save(output_path)
