import streamlit as st
from holiday_countdown import getCountryCode,get_holidays,format_results

st.title("Holiday Countdown ⏳")
countryName = st.text_input("Country Name")
year = st.text_input("Year")

if st.button("Get Holidays"):
    if countryName and year:
        response = getCountryCode(countryName)
        if response["success"]:
            countryCode = response["data"]
            holidayList = get_holidays(countryCode,year)
            final = format_results(holidayList)
            #st.write(countryName,countryCode,year)
            st.write(final)

    else:
        st.warning("Please enter both country and year!")