"""Small dependency-free OOXML writer for editable report paragraphs, tables and figures."""
from datetime import datetime, timezone
from html import escape
from pathlib import Path
import re
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as ET


def clean(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return text.replace('**', '').replace('`', '')


class Document:
    def __init__(self, title):
        self.title = title
        self.parts = []
        self.images = []

    def paragraph(self, text='', style=None):
        props = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ''
        self.parts.append(f'<w:p>{props}<w:r><w:t xml:space="preserve">{escape(clean(text))}</w:t></w:r></w:p>')

    def table(self, rows):
        columns = max(len(row) for row in rows)
        width = 9360 // columns
        parts = ['<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:tblBorders>']
        parts += [f'<w:{side} w:val="single" w:sz="4" w:color="D5DDE8"/>' for side in ('top','left','bottom','right','insideH','insideV')]
        parts += ['</w:tblBorders></w:tblPr><w:tblGrid>' + ''.join(f'<w:gridCol w:w="{width}"/>' for _ in range(columns)) + '</w:tblGrid>']
        for index, row in enumerate(rows):
            parts.append('<w:tr><w:trPr><w:cantSplit/>' + ('<w:tblHeader/>' if index == 0 else '') + '</w:trPr>')
            for cell in row:
                shade = '<w:shd w:fill="E9EFF8"/>' if index == 0 else ''
                bold = '<w:b/>' if index == 0 else ''
                parts.append(f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shade}</w:tcPr><w:p><w:pPr><w:spacing w:after="65"/></w:pPr><w:r><w:rPr>{bold}<w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">{escape(clean(cell))}</w:t></w:r></w:p></w:tc>')
            parts.append('</w:tr>')
        parts.append('</w:tbl>')
        self.parts.append(''.join(parts))

    def section_end(self, landscape=False):
        size = '<w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>' if landscape else '<w:pgSz w:w="11906" w:h="16838"/>'
        self.parts.append(f'<w:p><w:pPr><w:sectPr><w:footerReference w:type="default" r:id="footer"/><w:type w:val="nextPage"/>{size}<w:pgMar w:top="1000" w:right="1100" w:bottom="1000" w:left="1100" w:header="400" w:footer="400"/></w:sectPr></w:pPr></w:p>')

    def image(self, file, caption='', landscape=False):
        from PIL import Image
        with Image.open(file) as image:
            width, height = image.size
        if landscape:
            self.section_end(False)
        maximum_width = 9.4 if landscape else 6.35
        maximum_height = 5.7 if landscape else 6.6
        inches = min(maximum_width, maximum_height * width / height)
        cx, cy = int(inches * 914400), int(inches * height / width * 914400)
        index = len(self.images)+1
        self.images.append(Path(file))
        self.parts.append(f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{index}" name="Figure {index}" descr="{escape(caption, quote=True)}"/><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic><pic:nvPicPr><pic:cNvPr id="0" name="image{index}.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="img{index}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>''')
        self.paragraph(caption, 'Caption')
        if landscape:
            self.section_end(True)

    def markdown(self, content, base):
        lines = content.splitlines()
        index = 0
        code = False
        while index < len(lines):
            line = lines[index].strip()
            if line.startswith('```'):
                code = not code
            elif code:
                self.paragraph(line, 'Code')
            elif line.startswith('|'):
                rows = []
                while index < len(lines) and lines[index].strip().startswith('|'):
                    cells = [cell.strip() for cell in lines[index].strip().strip('|').split('|')]
                    if not all(re.fullmatch(r'[:\- ]+', c or '-') for c in cells):
                        rows.append(cells)
                    index += 1
                self.table(rows)
                continue
            elif line.startswith('!['):
                match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line)
                if match:
                    image = Path(base) / match[2]
                    self.image(image, match[1], landscape='system_diagram' in image.name)
            elif line.startswith('# '):
                self.paragraph(line[2:], 'Title')
            elif line.startswith('## '):
                self.paragraph(line[3:], 'Heading1')
            elif line.startswith('### '):
                self.paragraph(line[4:], 'Heading2')
            elif line:
                self.paragraph(('• '+line[2:]) if line.startswith('- ') else line)
            index += 1

    def save(self, file):
        namespaces = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"'
        footer = '<w:sectPr><w:footerReference w:type="default" r:id="footer"/><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1000" w:right="1100" w:bottom="1000" w:left="1100" w:header="400" w:footer="400"/></w:sectPr>'
        document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {namespaces}><w:body>{"".join(self.parts)}{footer}</w:body></w:document>'
        styles = '''<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="100" w:line="260" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="200"/></w:pPr><w:rPr><w:b/><w:color w:val="173456"/><w:sz w:val="40"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:outlineLvl w:val="0"/><w:spacing w:before="220" w:after="120"/></w:pPr><w:rPr><w:b/><w:color w:val="173456"/><w:sz w:val="29"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:rPr><w:i/><w:color w:val="526078"/><w:sz w:val="18"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/></w:rPr></w:style></w:styles>'''
        rel_ns = 'http://schemas.openxmlformats.org/package/2006/relationships'
        rels = [f'<Relationship Id="styles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>', '<Relationship Id="footer" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>']
        rels += [f'<Relationship Id="img{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{i}.png"/>' for i in range(1,len(self.images)+1)]
        content_types = '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>'
        now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        core = f'<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>{escape(self.title)}</dc:title><dc:creator>Business Analysis Assistant</dc:creator><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created></cp:coreProperties>'
        package = {'[Content_Types].xml': content_types,
                   '_rels/.rels': f'<Relationships xmlns="{rel_ns}"><Relationship Id="doc" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="core" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>',
                   'word/document.xml': document, 'word/styles.xml': styles,
                   'word/_rels/document.xml.rels': f'<Relationships xmlns="{rel_ns}">{"".join(rels)}</Relationships>',
                   'word/footer1.xml': '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:t>Page </w:t></w:r><w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText> PAGE </w:instrText></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>',
                   'docProps/core.xml': core}
        for xml in package.values(): ET.fromstring(xml)
        with ZipFile(file, 'w', ZIP_DEFLATED) as archive:
            for name, xml in package.items(): archive.writestr(name, xml.encode('utf-8'))
            for i, image in enumerate(self.images, 1): archive.write(image, f'word/media/image{i}.png')
