import streamlit as st
import sys
import os

sys.path.insert(0,os.path.dirname(__file__))
from holiday_countdown import getCountryCode,get_holidays,format_results, gui_formatter

st.title("Holiday Countdown ⏳")
countryName = st.text_input("Country Name")
year = st.text_input("Year")

if st.button("Get Holidays"):
    if countryName and year:
        response = getCountryCode(countryName)
        if response["success"]:
            countryCode = response["data"]
            holidayList = get_holidays(countryCode,year)
            final = gui_formatter(holidayList)

            if "error" in final:
                st.warning(final["error"])
            else:
                col1, col2 = st.columns([3,1])
                for holiday in final["holidays"]:
                    if holiday["isToday"]:
                            st.balloons()
                            st.success(f"🎉 {holiday['name']} is TODAY! 🎉")
                    else:
                            col1, col2 = st.columns([3,1])
                            with col1:
                                if holiday["name"] != holiday["localName"]:
                                      st.header(f"🎉 {holiday['name']}")
                                      st.caption(f"Local Name: {holiday["localName"]}")
                                else:
                                     st.header(f"🎉 {holiday['name']}")
                            with col2:
                                 st.metric("Countdown",f"{holiday['countdown']} days")
                            with st.expander("Details"):
                                st.write(f"📍**Local Name:** {holiday["localName"]}")
                                st.write(f"📅 **Date:** {holiday['date'].strftime('%B %d, %Y')}")
                                st.write(f"🌍 **Global Holiday:** {'Yes' if holiday['global'] else 'No'}")
                                st.write(f"🏷️ **Type:** {', '.join(holiday['types'])}")
                            
                            st.divider()  # Visual separator between holidays

            #st.write(countryName,countryCode,year)
            #st.write(final)

    else:
        st.warning("Please enter both country and year!")