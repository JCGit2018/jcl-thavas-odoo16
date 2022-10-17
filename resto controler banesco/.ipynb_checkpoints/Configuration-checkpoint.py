import os
from CyberSource.logging.log_configuration import LogConfiguration

class Configuration:
    def __init__(self):
        self.authentication_type ="http_signature"
        #self.merchantid = "testrest"
        self.merchantid =  'bc_5808831146'
        self.alternative_merchantid = "testrest_cpctv"
        self.run_environment = "apitest.cybersource.com"
        self.request_json_path = ""
        # JWT PARAMETERS
        self.key_alias = "testrest"
        self.key_pass = "testrest"
        self.key_file_name = "testrest"
        self.alternative_key_alias = "testrest_cpctv"
        self.alternative_key_pass = "testrest_cpctv"
        self.alternative_key_file_name = "testrest_cpctv"
        self.keys_directory = os.path.join(os.getcwd(), "resources")
        # HTTP PARAMETERS
        #self.merchant_keyid = "08c94330-f618-42a3-b09d-e1e43be5efda"
        #self.merchant_keyid = "08c94330-f618-42a3-b09d-e1e43be5mda" para generar error
        self.merchant_keyid = "514d1b75-3463-45b2-aa09-36ced899db68" #de la pagina cybersource
        #self.merchant_secretkey = "yBJxy6LjM2TmcPGu+GaJrHtkke25fPpUX+UY6/L/1tE="
        self.merchant_secretkey = "4JFoYPuPz9p9InCv7i3bSJA87FUoh2f9ypxpu+ucu3Y="
        self.alternative_merchant_keyid = "e547c3d3-16e4-444c-9313-2a08784b906a"
        self.alternative_merchant_secretkey = "JXm4dqKYIxWofM1TIbtYY9HuYo7Cg1HPHxn29f6waRo="
        # META KEY PARAMETERS
        self.use_metakey = False
        self.portfolio_id = ''
        # CONNECTION TIMEOUT PARAMETER
        self.timeout = 1000
        # LOG PARAMETERS
        self.enable_log = True
        self.log_file_name = "cybs"
        self.log_maximum_size = 10487560
        self.log_directory = os.path.join(os.getcwd(), "Logs")
        self.log_level = "Debug"
        self.enable_masking = False
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.log_date_format = "%Y-%m-%d %H:%M:%S"
        # PROXY PARAMETERS
        #self.proxy_address = "userproxy.com"
        #self.proxy_port = ""

    # Assigning the configuration properties in the configuration dictionary
    def get_configuration(self):
        configuration_dictionary = ({})
        configuration_dictionary["authentication_type"] = self.authentication_type
        configuration_dictionary["merchantid"] = self.merchantid
        configuration_dictionary["run_environment"] = self.run_environment
        configuration_dictionary["request_json_path"] = self.request_json_path
        configuration_dictionary["key_alias"] = self.key_alias
        configuration_dictionary["key_password"] = self.key_pass
        configuration_dictionary["key_file_name"] = self.key_file_name
        configuration_dictionary["keys_directory"] = self.keys_directory
        configuration_dictionary["merchant_keyid"] = self.merchant_keyid
        configuration_dictionary["merchant_secretkey"] = self.merchant_secretkey
        configuration_dictionary["use_metakey"] = self.use_metakey
        configuration_dictionary["portfolio_id"] = self.portfolio_id
        configuration_dictionary["timeout"] = self.timeout
        log_config = LogConfiguration()
        log_config.set_enable_log(self.enable_log)
        log_config.set_log_directory(self.log_directory)
        log_config.set_log_file_name(self.log_file_name)
        log_config.set_log_maximum_size(self.log_maximum_size)
        log_config.set_log_level(self.log_level)
        log_config.set_enable_masking(self.enable_masking)
        log_config.set_log_format(self.log_format)
        log_config.set_log_date_format(self.log_date_format)
        configuration_dictionary["log_config"] = log_config
        #configuration_dictionary["proxy_address"] = self.proxy_address
        #configuration_dictionary["proxy_port"] = self.proxy_port
        return configuration_dictionary

    def get_alternative_configuration(self):
        configuration_dictionary = ({})
        configuration_dictionary["authentication_type"] = self.authentication_type
        configuration_dictionary["merchantid"] = self.alternative_merchantid
        configuration_dictionary["run_environment"] = self.run_environment
        configuration_dictionary["request_json_path"] = self.request_json_path
        configuration_dictionary["key_alias"] = self.alternative_key_alias
        configuration_dictionary["key_password"] = self.alternative_key_pass
        configuration_dictionary["key_file_name"] = self.alternative_key_file_name
        configuration_dictionary["keys_directory"] = self.keys_directory
        configuration_dictionary["merchant_keyid"] = self.alternative_merchant_keyid
        configuration_dictionary["merchant_secretkey"] = self.alternative_merchant_secretkey
        configuration_dictionary["use_metakey"] = self.use_metakey
        configuration_dictionary["portfolio_id"] = self.portfolio_id
        configuration_dictionary["timeout"] = self.timeout
        log_config = LogConfiguration()
        log_config.set_enable_log(self.enable_log)
        log_config.set_log_directory(self.log_directory)
        log_config.set_log_file_name(self.log_file_name)
        log_config.set_log_maximum_size(self.log_maximum_size)
        log_config.set_log_level(self.log_level)
        log_config.set_enable_masking(self.enable_masking)
        log_config.set_log_format(self.log_format)
        log_config.set_log_date_format(self.log_date_format)
        configuration_dictionary["log_config"] = log_config
        #configuration_dictionary["proxy_address"] = self.proxy_address
        #configuration_dictionary["proxy_port"] = self.proxy_port
        return configuration_dictionary