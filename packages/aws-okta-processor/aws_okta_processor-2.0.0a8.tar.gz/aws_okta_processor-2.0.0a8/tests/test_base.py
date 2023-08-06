import os

from unittest import TestCase

WORKING_DIR = os.path.dirname(__file__)
ABS_PATH = os.path.abspath(WORKING_DIR)
SAML_RESPONSE_PATH = os.path.join(ABS_PATH, "SAML_RESPONSE")
SAML_RESPONSE = open(SAML_RESPONSE_PATH, 'r').read()
SIGN_IN_RESPONSE_PATH = os.path.join(ABS_PATH, "SIGN_IN_RESPONSE")
SIGN_IN_RESPONSE = open(SIGN_IN_RESPONSE_PATH, 'r').read()
SESSION_RESPONSE_PATH = os.path.join(ABS_PATH, "SESSION_RESPONSE")
SESSION_RESPONSE = open(SESSION_RESPONSE_PATH, 'r').read()
AUTH_TOKEN_RESPONSE_PATH = os.path.join(ABS_PATH, "AUTH_TOKEN_RESPONSE")
AUTH_TOKEN_RESPONSE = open(AUTH_TOKEN_RESPONSE_PATH, 'r').read()
AUTH_MFA_RESPONSE_PATH = os.path.join(ABS_PATH, "AUTH_MFA_RESPONSE")
AUTH_MFA_RESPONSE = open(AUTH_MFA_RESPONSE_PATH, 'r').read()
MFA_WAITING_RESPONSE_PATH = os.path.join(ABS_PATH, "MFA_WAITING_RESPONSE")
MFA_WAITING_RESPONSE = open(MFA_WAITING_RESPONSE_PATH, 'r').read()
APPLICATIONS_RESPONSE_PATH = os.path.join(ABS_PATH, "APPLICATIONS_RESPONSE")
APPLICATIONS_RESPONSE = open(APPLICATIONS_RESPONSE_PATH, 'r').read()


class TestBase(TestCase):
    def setUp(self):
        self.OPTIONS = [
            "--user", "user_name",
            "--organization", "org.okta.com",
            "--key", "key"
        ]
