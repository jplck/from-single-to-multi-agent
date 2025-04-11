from semantic_kernel.functions import kernel_function
import pytz
from datetime import datetime

class ChefPlugin:

    @kernel_function
    async def get_weather(self, city: str) -> str:
        """Gets a statement about the current weathr in the city defined in the parameter"""
        print("executing get_weather")
        return f"The weather in {city} is 73 degrees and Sunny."
    
    @kernel_function    
    async def get_medical_history(self, username: str) -> str:
        "Get the medical history for a given username with known allergies and food restrictions."
        print("executing get_medical_history")
        return f"{username} has an allergy to peanuts and eggs."
    
    @kernel_function    
    async def get_available_incredients(self, location: str) -> str:
        "Get the available incredients for a given location."
        print("executing get_available_incredients")
        return f"Available incredients in {location} are: eggs, milk, bread, peanuts, beer, wine, salmon, spinache, oil and butter."
    
    @kernel_function  
    def get_current_username(self) -> str:
        "Get the username of the current user."
        print("executing get_current_username")
        return "Dennis"
    
    @kernel_function  
    def get_current_location_of_user(self, username: str) -> str:
        "Get the current timezone location of the user for a given username."
        print("executing get_current_location")
        print(username)
        if "Dennis" in username:
            return "Europe/Berlin"
        else:
            return "America/New_York"
    
    @kernel_function  
    def get_current_time(self, location: str) -> str:
        "Get the current time in the given location. The pytz is used to get the timezone for that location. Location names should be in a format like America/Seattle, Asia/Bangkok, Europe/London. Anything in Germany should be Europe/Berlin"
        try:
            print("get current time for location: ", location)
            timezone = pytz.timezone(location)
            # Get the current time in the timezone
            now = datetime.now(timezone)
            current_time = now.strftime("%I:%M:%S %p")
            return current_time
        except Exception as e:
            print("Error: ", e)
            return "Sorry, I couldn't find the timezone for that location."