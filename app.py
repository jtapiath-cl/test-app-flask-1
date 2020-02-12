def image_generator(texto: str):
    from PIL import Image, ImageDraw, ImageFont
    import textwrap
    
    font_loc = "/home/jtapiath/.fonts/Code New Roman.otf"
    footer_loc = "/home/jtapiath/.fonts/Code New Roman b.otf"
    fontsize = 60
    footer = "@raspado_de_olla"
    
    img = Image.new("RGB", (1080, 1080), color = "black")
    canvas = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_loc, fontsize)
    font_footer = ImageFont.truetype(footer_loc, 45)
    
    texto_print = textwrap.fill(texto, 28)
    
    canvas.multiline_text(xy = (100, 190), text = texto_print, font = font, fill = "white", spacing = 30)
    canvas.text((100, 920), footer, font = font_footer, fill = "gray")
    
    return img

from flask import Flask, render_template, request, send_file, send_from_directory

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/", methods=["GET", "POST"])
def generating_image():
    import os
    from datetime import datetime

    text_form = request.form["text"]    
    img_name = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + "_img.png"
    img_path = os.path.join(os.getcwd(), "static", "imgs", img_name)
    imagen = image_generator(text_form)
    imagen.save(img_path)
    
    return send_from_directory("static/imgs", img_name, as_attachment = False, cache_timeout = 0)

if __name__ == "__main__":
    app.run(threaded = True, debug = False, port = 5000)