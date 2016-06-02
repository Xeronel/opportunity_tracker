import yaml
import os


class Config:
    def __init__(self):
        self.__load_config()
        file_path = os.path.dirname(__file__)
        web_defaults = {'debug': False,
                        'autoreload': False,
                        'compiled_template_cache': True,
                        'static_path': os.path.join(file_path, 'static'),
                        'template_path': os.path.join(file_path, 'templates'),
                        'cookie_secret': {0: 'j9Wy1m*3CnwKw!AFd5sd3kl@'},
                        'key_version': 0}
        db_defaults = {'database': 'sss',
                       'username': 'postgres',
                       'password': '',
                       'hostname': 'localhost',
                       'port': "5432",
                       'size': 1,
                       'max_size': None,
                       'auto_shrink': False}

        # Make sure cookie_secret is stored as a dictionary
        if 'cookie_secret' in self.web_config \
                and type(self.web_config['cookie_secret']) == str \
                and self.web_config['cookie_secret']:
            self.web_config['cookie_secret'] = {0: self.web_config['cookie_secret']}

        # Load defaults for missing or unset keys
        self.web_config = self.__load_defaults(web_defaults, self.web_config)
        self.db_config = self.__load_defaults(db_defaults, self.db_config)

        # Set some additional defaults if in debug mode
        if self.debug:
            self.web_config['compiled_template_cache'] = False
            self.web_config['autoreload'] = False
        else:
            self.web_config['compiled_template_cache'] = True
            self.web_config['autoreload'] = True

    @staticmethod
    def __load_defaults(defaults: dict, config: dict) -> dict:
        """
        Merge a user set dictionary with a normalized one containing default values
        :param defaults: Dictionary containing all keys with default values set
        :param config: Dictionary to merge with defaults
        :return: Merged dictionary
        """
        for k, v in defaults.items():
            if k not in config or not config[k]:
                config[k] = v
        return config

    def __load_config(self):
        """Setup raw config field dictionaries"""
        with open('config.yaml', 'r') as f:
            self.raw_config = yaml.load(f.read())
        self.web_config = self.raw_config['web_server']
        self.db_config = self.raw_config['database']

    @property
    def debug(self) -> bool:
        """
        Tornado web application debug setting
        :rtype: bool
        :return: debug mode
        """
        return self.web_config['debug']

    @property
    def autoreload(self) -> bool:
        """
        Tornado autoreload application setting
        :rtype: bool
        :return: autoreload setting
        """
        return self.web_config['autoreload']

    @property
    def compiled_template_cache(self) -> str:
        """
        Recompile templates on each page view or cache them
        :rtype: bool
        :return: template cache setting
        """
        return self.web_config['compiled_template_cache']

    @property
    def static_path(self) -> str:
        """
        The location of static web files
        :rtype: str
        :return: static file directory
        """
        return self.web_config['static_path']

    @property
    def template_path(self) -> str:
        """
        The location of html template files
        :rtype: str
        :return: template directory
        """
        return self.web_config['template_path']

    @property
    def cookie_secret(self) -> dict:
        """
        A dictionary of cookie secrets indexed by version number
        :rtype: dict
        :return: cookie secret dictionary
        """
        return self.web_config['cookie_secret']

    @property
    def key_version(self) -> int:
        """
        Which cookie secret version to use
        :rtype: int
        :return: cookie secret version
        """
        return int(self.web_config['key_version'])

    @property
    def username(self) -> str:
        """
        Username to use when connecting to postgres
        :rtype: str
        :return: postgres username
        """
        return self.db_config['username']

    @property
    def password(self) -> str:
        """
        Postgres users password
        :rtype: str
        :return: postgres user's password
        """
        return self.db_config['password']

    @property
    def database(self) -> str:
        """
        Postgres database to connect to
        :rtype: str
        :return: Postgres database name
        """
        return self.db_config['database']

    @property
    def hostname(self) -> str:
        """
        Hostname of the postgres server
        :rtype: str
        :return: hostname or ip
        """
        return self.db_config['hostname']

    @property
    def port(self) -> str:
        """
        Port the postgres server is listening on
        :rtype: str
        :return: server port
        """
        return str(self.db_config['port'])

    @property
    def size(self) -> int:
        """
        Minimum number of database connections to keep open
        :rtype: int
        :return: number of database connections
        """
        return int(self.db_config['size'])

    @property
    def max_size(self) -> int:
        """
        Maximum number of simultaneous database connections
        :rtype: int
        :return: max number of database connections
        """
        # Set to None if no limit
        return self.db_config['max_size']

    @property
    def auto_shrink(self) -> bool:
        """
        Automatically garbage collect database connections that have been idle for 120 seconds
        (only applies if max_size is set)
        :rtype: bool
        :return: auto shrink setting
        """
        return self.db_config['auto_shrink']
