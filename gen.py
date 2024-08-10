import xml.etree.cElementTree as ET
from PIL import Image
from numpy import asarray

# XML file Setup
root = ET.Element("tt", xmlns="http://www.w3.org/ns/ttml")
root.set("xml:lang", "")

## Head Section
head = ET.SubElement(root, "head")

### Metadata
metadata = ET.SubElement(head, "metadata")

metadata.set("xmlns:ttm", "http://www.w3.org/ns/ttml#metadata")
ET.SubElement(metadata, "ttm:title").text = "Bad Apple but its all in the subtitles"

### Style
styling = ET.SubElement(head, "styling")

styling.set("xmlns:ttm", "http://www.w3.org/ns/ttml#styling")
ET.SubElement(styling, "style").attrib = {
    "xml:id": "reg",
    "tts:color": "white",
    "tts:textAlign": "left",
}

### Layout
layout = ET.SubElement(head, "layout")

styling.set("xmlns:ttm", "http://www.w3.org/ns/ttml#layout")
ET.SubElement(layout, "region").attrib = {
    "xml:id": "regularArea",
    "style": "reg",
    "tts:extent": "100% 100%",
    "tts:origin": "0% 0%",
    "tts:backgroundColor": "black",
}

## Body Section
body = ET.SubElement(root, "body")

### Body Section Setup
body.set("region", "regularArea")
subtitle_queue = ET.SubElement(body, "div")

### Adding subtitles
sub_numb = 0

def add_subtitle(begin, end, subtitle):
    global sub_numb
    sub_numb += 1
    subtitle_element = ET.SubElement(subtitle_queue, "p")
    subtitle_element.text= subtitle
    subtitle_element.attrib = {
        "xml:id": f'subtitle{sub_numb}',
        "begin": f'{begin}s',
        "end": f'{end}s',
    }

# Adding in subtitles
## The subtitles can have 37 characters across and 17 characters tall

## The image to text conversion function
def image_to_string(frame_number):
    output = ""
    string = "悪いリンゴ"

    index = 0

    img = Image.open(f"frames/frame{frame_number}.png")
    array = asarray(img)

    for row in array:
        for pixel in row:
            index = (index + 1) % 5
            if pixel.mean() > 127:
                output += string[index]
            else:
                output += '　'
        output += "<br>"
    
    return output

for i in range(1, 2192):
    add_subtitle((i-1)/10, i/10, image_to_string(i))
    print(i)

# Writing the XML file
tree = ET.ElementTree(root)
tree.write("test.ttml", 'utf-8')

# Evil hack to get around scrubbing
with open("test.ttml", "r", encoding='utf-8') as f:
    text = f.read().replace("&lt;br&gt;", "<br>")
with open("test.ttml", "w", encoding='utf-8') as f:
    f.write(text)