class EmailDTO:
    def __init__(self):
        self._header = ""
        self._body = ""
        self._recipient_email = ""

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        self._header = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def recipient_email(self):
        return self._recipient_email

    @recipient_email.setter
    def recipient_email(self, value):
        self._recipient_email = value
