# 🎉 Holiday Countdown Tracker ⏲️

> Because manually googling "when is the next holiday" is so 2023

## What Does This Thing Do?

Ever find yourself desperately wondering how many days until you can sleep in guilt-free? Wonder no more! This bad boy tells you exactly how long until your next government-sanctioned day off.

**Features that'll blow your mind (or at least mildly impress you):**
- 🌍 Works for basically any country (as long as they have holidays and the internet knows about them)
- 📅 Tells you ALL upcoming holidays, not just the next one (because planning is important, Karen)
- ⚡ Has a GUI! No more sad terminal commands like it's 1995
- 🎊 Shows you which holidays are GLOBAL vs just random local ones
- ✨ Actually works (most of the time)

## How to Use This

### The Easy Way (GUI Version)
1. Run `holiday_gui.py`
2. Type a country name (like "United States" or "Canada" or "Japan")
3. Type a year (protip: use numbers, not words)
4. Smash that "Get Holidays" button
5. Marvel at the list of upcoming holidays
6. Plan your life accordingly

### The Hacker Way (Terminal Version)
If you're feeling nostalgic for the command line:
```bash
python holiday_countdown.py
```
Then follow the prompts like it's an adventure game, except less exciting.

## What You Need

- Python 3.x (because we're not animals)
- tkinter (for the GUI magic)
- requests library (for talking to the internet)
- An internet connection (shocking, I know)
- Dreams of days off

## Installation

```bash
# Clone this masterpiece
git clone [your-repo-url]

# Install the stuff
pip install requests

# Run it
python holiday_gui.py
```

## How It Works (The Nerdy Bit)

1. You tell it a country
2. It asks another API "yo what's the country code for this?"
3. That API is like "oh it's US" or whatever
4. Then it asks the holiday API "what holidays does US have?"
5. The holiday API dumps a bunch of JSON at us
6. We do some date math (complicated stuff, very impressive)
7. We show you the results in a nice window
8. You feel informed and slightly less stressed

## Known Issues

- Can't predict holidays that haven't been announced yet (we're developers, not fortune tellers)
- Won't include your company's random made-up "team building" days (sorry)
- May cause excessive excitement about upcoming three-day weekends
- Results may vary if you live in a country that doesn't believe in fun

## Future Plans (Maybe)

- [ ] Add countdown timer that updates in real-time
- [ ] Integrate with calendar apps
- [ ] Add "days until I can quit my job" calculator
- [ ] Support for made-up personal holidays
- [ ] Theme options (terminal green, anyone?)

## Contributing

Found a bug? Want to add a feature? Think my code is ugly? 
- Open an issue
- Submit a PR
- Send encouraging messages
- All of the above

## License

Do whatever you want with this. Just don't blame me if you get too excited about holidays and make poor life decisions.

## Credits

Built by someone who really, *really* likes having days off.

APIs used:
- [Nager.Date](https://date.nager.at/) - For holiday data
- [REST Countries](https://restcountries.com/) - For country code lookups

---

**Remember:** Life is short. Holidays are shorter. Use this tool wisely. ⏰🎊