```python
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(name, result):

    pdf = SimpleDocTemplate(
        f"reports/{name}.pdf"
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "SkinAI Report",
        styles["Title"]
    )

    elements.append(title)

    text = Paragraph(
        str(result),
        styles["BodyText"]
    )

    elements.append(text)

    pdf.build(elements)
```
