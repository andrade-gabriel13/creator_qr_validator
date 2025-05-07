import qrcode
import base64
from io import BytesIO

def generate_qr_code_base64(data: str) -> str:
    img = qrcode.make(data)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()
