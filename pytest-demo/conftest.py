import pytest
import smtplib


@pytest.fixture(scope="module")
def smtp(request):
    server = getattr(request.module, "smtpserver", "smtp.gmail.com")
    smtp = smtplib.SMTP(server)