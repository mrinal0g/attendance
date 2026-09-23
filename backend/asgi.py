"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f"Project is live in http://{local_ip}:8000")
application = get_asgi_application()
import qrcode

# Create QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(f"http://{local_ip}:8000")
qr.make(fit=True)

# Save as image
img = qr.make_image(fill_color="black", back_color="white")
img.save("qrcode.png")