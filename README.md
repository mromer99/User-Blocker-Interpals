# User Blocker for Interpals.com

# Introduction

As we know that Social networking Websites like, Instagram, Facebook, Interpals and many more help us to connect with people from around the word despite the huge travel Distance. But this also brings another Problem: Unnecessary contacts which makes us loose the Overview in our Message Box. With my Tool, you can Block users by adjusting the time. For example if you had contacts, who you don't want to see any contacs you didn't write since 4 years, you can let the tool block all of them.

TL;dr, This project automates the process of blocking and deleting old conversations on Interpals using Selenium WebDriver. The script logs into Interpals, navigates to the messages page, loads older conversations, and blocks/deletes users based on a specified time range or if their accounts no longer exist.


## Features
- Logs into Interpals with provided credentials.
- Loads older conversations until no more are available.
- Filters and lists users based on an given time range.
- Identifies and lists all inactive users regardless of timestamp.
- Blocks and deletes users based on the filtered list.

## Requirements

- Python 3.x
- Selenium
- Firefox WebDriver (geckodriver)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mromer99/interpals-user-blocker.git
   cd interpals-user-blocker
   ```
2. **Install the required Python packages:**
```bash
pip install selenium
```

3. **Download and install geckodriver:** 
Follow the instructions for your operating system from the [geckodriver GitHub releases page](https://github.com/mozilla/geckodriver/releases).

4. **Update the script with your Interpals login credentials:** 
Open blocker.py and replace `your_email` and `your_password` with your Interpals email and password.

## Usage

1.**Adjust the time frame on the code for yourself:**
```python
# Function to check if the timestamp is within the range
def is_within_range(timestamp):
    match = re.match(r'(\d+)\s+(day|month)s?\s+ago', timestamp)
    if match:
        value, unit = int(match.group(1)), match.group(2)
        if unit == 'day':
            return 24 <= value <= 31
        elif unit == 'month':
            return 1 <= value <= 1
    return False
```
2. **Run the Script:**
```bash
python3 blocker.py
```
3. **Output:**
- The script will print the accounts that will be blocked, including their timestamp, username, city, and age.
- It will also list all inactive users regardless of timestamp.

## Example Output
```yaml
No more 'Load older conversations' button found or an error occurred.
Found 193 messages with timestamps.
Found 35 messages within the desired time range.
Accounts to be blocked:
Timestamp: 22 days ago, Username: domi876, City: Jupiter, Age:  25
...
Inactive accounts:
Timestamp: 22 days ago, Username: Inactive User
...
All inactive accounts:
Timestamp: 22 days ago, Username: Inactive User
...
```

## License
This project is licensed under the MIT License.
   


