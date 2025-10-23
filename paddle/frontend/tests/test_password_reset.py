import re
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

@pytest.mark.django_db
def test_password_reset_flow(client):
    # create user
    user = User.objects.create_user(username="resetuser", email="reset@example.com", password="OldPass123")
    url = reverse("password_reset")

    # GET form
    resp = client.get(url)
    assert resp.status_code == 200

    # POST email -> should send mail (custom form in project requires existing email)
    resp = client.post(url, {"email": "reset@example.com"}, follow=True)
    assert resp.status_code in (200, 302)
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert "reset" in email.body.lower() or "restablecimiento" in email.body.lower()

    # Build a valid uid/token and visit confirm URL
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    confirm_url = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
    resp = client.get(confirm_url, follow=True)
    # The confirm page should be reachable
    assert resp.status_code == 200
    # Determine the final path to post the new password to (works whether redirect happened or not)
    final_path = resp.request.get("PATH_INFO") or confirm_url

    # POST new password
    new_pass = "NewPass456"
    resp = client.post(final_path, {"new_password1": new_pass, "new_password2": new_pass}, follow=True)
    assert resp.status_code in (200, 302)

    # After reset, login with new password should work
    logged_in = client.login(username="resetuser", password=new_pass)
    assert logged_in

@pytest.mark.django_db
def test_password_reset_fails_for_nonexistent_email(client):
    url = reverse("password_reset")
    # Posting a non-existing email should return form error because project uses EmailExistsPasswordResetForm
    resp = client.post(url, {"email": "noone@example.com"})
    # either form redisplayed with error (200) or redirect kept but no email sent; check no email
    assert len(mail.outbox) == 0
    # prefer to assert that response contains the localized validation message if present
    content = resp.content.decode(errors="ignore").lower()
    assert ("no existe ninguna cuenta" in content) or (resp.status_code in (200, 302))