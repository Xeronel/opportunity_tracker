from .config import BaseConfig, Entry


class SMTPConfig(BaseConfig):
    def __init__(self):
        is_str = lambda x: type(x) == str
        skeleton = {'sender': Entry('admin@shealy-solutions.com', is_str),
                    'username': Entry('', is_str),
                    'password': Entry('', is_str),
                    'hostname': Entry('mail.shealyelectrical.com', is_str),
                    'port': Entry('25', lambda x: is_str(x) or type(x) == int)}
        super().__init__(skeleton, 'smtp')

    @property
    def sender(self):
        return self.raw_config['sender']

    @property
    def username(self) -> str:
        """
        Username to use when connecting
        :rtype: str
        :return: postgres username
        """
        return self.raw_config['username']

    @property
    def password(self) -> str:
        """
        Email password
        :rtype: str
        :return: postgres user's password
        """
        return self.raw_config['password']

    @property
    def hostname(self) -> str:
        """
        Hostname of the mail server
        :rtype: str
        :return: hostname or ip
        """
        return self.raw_config['hostname']

    @property
    def port(self) -> str:
        """
        Port the mail server is listening on
        :rtype: str
        :return: server port
        """
        return str(self.raw_config['port'])
