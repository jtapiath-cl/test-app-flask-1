def image_generator(texto: str, firma:str = "@raspado_de_olla"):
    from PIL import Image, ImageDraw, ImageFont
    import textwrap
    
    font_loc = "static/resources/Code New Roman.otf"
    footer_loc = "static/resources/Code New Roman b.otf"
    fontsize = 60
    footer = firma
    
    img = Image.new("RGB", (1080, 1080), color = "black")
    canvas = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_loc, fontsize)
    font_footer = ImageFont.truetype(footer_loc, 45)
    
    texto_print = textwrap.fill(texto, 28)
    
    canvas.multiline_text(xy = (100, 190), text = texto_print, font = font, fill = "white", spacing = 30)
    canvas.text((100, 920), footer, font = font_footer, fill = "gray")
    
    return img

from flask import Flask, render_template, request, send_file
from flask import jsonify, abort
import os

IMG_REPO = os.path.join("static", "imgs")

app = Flask(__name__)
app.config["IMG_FOLDER"] = IMG_REPO

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/", methods=["post", "get"])
def generating_image():
    from datetime import datetime
    text_form = request.form.get("textBox1")
    signature = request.form.get("textBox2")
    img_name = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + "_img.png"
    img_path = os.path.join(app.config["IMG_FOLDER"], img_name)
    imagen = image_generator(texto = text_form, firma = signature)
    imagen.save(img_path)    
    return render_template("img.html", user_image = img_path)

@app.route("/get-image/<path:path>")
def serving_image(path):
    from datetime import datetime
    file_to_download = path
    img_name = datetime.strftime(datetime.now(), "%Y%m%d-%H%M%S") + "-meme.png"
    if os.path.exists(file_to_download):
        return send_file(file_to_download, cache_timeout = 0, as_attachment = True,
                          attachment_filename = img_name)
    else:
        abort(404, "file does not exist")

if __name__ == "__main__":
    app.run(threaded = True, debug = True, port = 1337)