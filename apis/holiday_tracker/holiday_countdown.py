import requests
import urllib.request
import json
from datetime import datetime

def getCountryCode(countryName):
    noDataCodes = [204,404]
    accessCodes = [401,403]
    badRequests = [500,502,503]
    url = f"https://restcountries.com/v3.1/name/{countryName}"
    results = requests.get(url)
    statusCode = results.status_code
    try: 
        statusCode = results.status_code
        if statusCode == 200:
            data = results.json()
            for name in data:
                countryCode = name["cca2"]
            return {"success": True, "data": countryCode}
        elif statusCode in noDataCodes:
            return {"success": False,"error": "No data found. Check year and country code!"}
        elif statusCode in badRequests:
            return {"success": False, "error": "Server error"}
        elif statusCode in accessCodes:
            return {"success": False, "error": "Access denied"}
        else:
            return {"success": False, "error": {statusCode}}
        

    except requests.exceptions.JSONDecodeError:
        return("Couldn't parse JSON response")
    except requests.exceptions.RequestException as e:
        return(f"Network Error: {e}")

    



def get_holidays(countryCode, year):
    noDataCodes = [204,404]
    accessCodes = [401,403]
    badRequests = [500,502,503]
    url = "https://date.nager.at/api/v3/PublicHolidays/"+f"{year}/"+f"{countryCode}"
    results = requests.get(url)
    try: 
        statusCode = results.status_code
        if statusCode == 200:
            return {"success": True, "data": results.json()}
        elif statusCode in noDataCodes:
            return {"success": False,"error": "No data found. Check year and country code!"}
        elif statusCode in badRequests:
            return {"success": False, "error": "Server error"}
        elif statusCode in accessCodes:
            return {"success": False, "error": "Access denied"}
        else:
            return {"success": False, "error": {statusCode}}
    except requests.exceptions.JSONDecodeError:
        return("Couldn't parse JSON response")
    except requests.exceptions.RequestException as e:
        return(f"Network Error: {e}")

def format_results(holiday_data):
    if not holiday_data["success"]:
        return holiday_data["error"]
    
    data = holiday_data["data"]
    today = datetime.now().date()
    results = []
    foundFutureHoliday = False
    for holiday in data:
            holidayDate = datetime.strptime(holiday["date"], "%Y-%m-%d").date()
            holidayName = holiday["name"]
            holidayType = holiday["types"]
            globalHoliday = holiday["global"]
            offSegment = holiday["types"]
            localName = holiday["localName"]
            if holidayDate > today:
                foundFutureHoliday = True
                countdown = (holidayDate - today).days
                if holidayName not in localName:
                    results_string = f"- {holidayName} ({localName}) is in {countdown} days on {holidayDate}\n"
                else:  
                    results_string = f"- {holidayName} is in {countdown} days on {holidayDate}\n"
                results_string += f"Global: {globalHoliday} | Type: {offSegment}\n"
                results.append(results_string)
            elif holidayDate == today:
                foundFutureHoliday = True
                results.append(f"🎉 {holidayName} also known as {localName} is today!🎉")
    if not foundFutureHoliday:
            return f"All holidays have passed for this year"
            
    return "\n".join(results)

def gui_formatter(holiday_data):
    if not holiday_data["success"]:
        return holiday_data["error"]
    data = holiday_data["data"]
    today = datetime.now().date()
    results = []
    foundFutureHoliday = False
    for holiday in data:
            holidayDate = datetime.strptime(holiday["date"], "%Y-%m-%d").date()
            holidayName = holiday["name"]
            holidayType = holiday["types"]
            globalHoliday = holiday["global"]
            offSegment = holiday["types"]
            localName = holiday["localName"]
            if holidayDate >= today:
                countdown = (holidayDate - today).days
                foundFutureHoliday = True
                results.append({
                        "name": holiday["name"],
                        "localName": holiday["localName"],
                        "date": holidayDate,
                        "countdown": countdown,
                        "global": holiday["global"],
                        "types": holiday["types"],
                        "isToday": holidayDate == today
                    })
    if not foundFutureHoliday:
        return {"Error": "All holidays have passed for this year"}
    return {"success": True, "holidays": results}

        