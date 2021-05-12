from django.shortcuts import render, HttpResponse

import random
# Create your views here.


def login(request):
    return render(request, 'login.html')

def get_validCode_img(request):
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    # 方式一
    # with open('dog.jpg') as f:
    #     data = f.read()

    # 方式二 pillow 模块
    # 使用磁盘作为存储，每次都需要写入文件打开文件，IO磁盘操作都是很慢的
    # from PIL import Image
    # img = Image.new('RGB', (270, 40), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    #
    # with open('validCode.png', 'wb') as f:
    #     img.save(f, 'png')
    #
    # with open('validCode.png', 'rb') as f:
    #     data = f.read()

    # 方式3 使用内存句柄，不经过磁盘
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    img = Image.new('RGB', (270, 40), get_random_color())

    # 在图片上增加文字
    draw = ImageDraw.Draw(img)
    halfings_font = ImageFont.truetype("static/fonts/kumo.ttf", size=32)
    # 随机字符生成
    for i in range(5):
        random_number = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))
        random_upper_alpha = chr(random.randint(65,90))
        random_char = random.choice([random_low_alpha, random_number, random_upper_alpha])
        draw.text((i*50+20, 5), random_char, get_random_color(), font=halfings_font)

    # 噪点噪线
    width = 270
    height = 40
    # 划线
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())

    # 画点
    for i in range(30):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()

    return HttpResponse(data)