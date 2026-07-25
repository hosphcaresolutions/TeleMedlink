# test_smtp.py
import smtplib
import socket
import ssl

socket.setdefaulttimeout(30)  # Set timeout to 30 seconds
try:
    print("Connecting to smtp.gmail.com:587...")
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as server:
        server.ehlo()
        print("EHLO sent, starting TLS...")
        server.starttls(context=ssl.create_default_context())
        server.ehlo()
        print("Logging in...")
        server.login('smiqmoses@gmail.com', 'your-app-password')
        print("SMTP login successful!")
except socket.timeout as e:
    print(f"Socket timeout error: {e}")
except smtplib.SMTPAuthenticationError as e:
    print(f"Authentication error: {e}")
except smtplib.SMTPException as e:
    print(f"SMTP error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")