import re
import pandas as pd

def preprocess(data):

    # NEW WhatsApp format
    # [14-08-2023, 11:21:29 PM] Name: Message

    pattern = r'\[(\d{2}-\d{2}-\d{4},\s\d{1,2}:\d{2}:\d{2}\s(?:AM|PM|am|pm))\]\s'

    messages = re.split(pattern, data)[1:]

    dates = messages[::2]
    messages = messages[1::2]

    df = pd.DataFrame({
        'date': dates,
        'user_message': messages
    })

    # convert date
    df['date'] = pd.to_datetime(
        df['date'],
        format='%d-%m-%Y, %I:%M:%S %p'
    )

    users = []
    message_list = []

    for message in df['user_message']:

        entry = re.split(r'([^:]+):\s', message)

        if len(entry) >= 3:
            users.append(entry[1])
            message_list.append(entry[2])

        else:
            users.append('Group_notification')
            message_list.append(message)

    df['user'] = users
    df['message'] = message_list

    df.drop(columns=['user_message'], inplace=True)

    # date features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # period
    period = []

    for hour in df['hour']:

        if hour == 23:
            period.append(f"{hour}-00")

        elif hour == 0:
            period.append(f"00-{hour+1}")

        else:
            period.append(f"{hour}-{hour+1}")

    df['period'] = period

    return df