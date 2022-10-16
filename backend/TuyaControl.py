from tuya_iot import TuyaOpenAPI, AuthType
import os
from dotenv import load_dotenv

load_dotenv()

class SwitchControl:
    def __init__(self,  ACCESS_ID = os.getenv('ACCESS_ID'), 
                        ACCESS_KEY = os.getenv('ACCESS_KEY'),
                        USERNAME = os.getenv('USERNAME'),
                        PASSWORD = os.getenv('PASSWORD')) -> None:
        self.ACCESS_ID = ACCESS_ID
        self.ACCESS_KEY = ACCESS_KEY
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.ENDPOINT = "https://openapi.tuyaus.com"	
        
        self.openapi = TuyaOpenAPI(endpoint = self.ENDPOINT, 
                      access_id= self.ACCESS_ID, 
                      access_secret= self.ACCESS_KEY,  
                      auth_type = AuthType.SMART_HOME)	
        self.openapi.connect(username= self.USERNAME, 
                password= self.PASSWORD,
                country_code= '1',
                schema="smartlife")
        self.device_states = {}
    
    def toggle_device(self, subdevice, device_id = os.getenv("DEVICE_ID")):
        """Toggle devices on or off

        Args:
            subdevice (_type_): list of devices in teh main device to toggle
            device_id (_type_, optional): device id to toggle. Defaults to os.getenv("DEVICE_ID").

        Returns:
            _type_: _description_
        """
        if type(subdevice) == str:
            subdevice = [subdevice]
        responses = {}
        for device in subdevice:
            value = self.openapi.get(f'/v1.0/iot-03/devices/{device_id}/status')
            relevant = [x['value'] for x in value['result'] if x['code'] == device]
            assert len(relevant) == 1, "Expected 1 result, got {}".format(len(relevant))
            
            commands = {'commands': [{'code':device,'value': not relevant[0]}]}      
            request = self.openapi.post(f'/v1.0/iot-03/devices/{device_id}/commands', commands)     
            responses[device] = request
        return responses