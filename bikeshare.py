import time
import pandas as pd
import numpy as np

#I like ham sandwiches

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = 0
    month = 0
    day = 0

    city = input('Pick the city you would like to analyze: Chicago, New York City, or Washington.\n').lower()

    while city not in ['chicago','new york city','washington']:
        city = input('Pick the city you would like to analyze: Chicago, New York City, or Washington.\n').lower()


    month = input('Enter the month you would like to analyze, or type "all" for no filter.\n').lower()
    while month not in ['january','february','march','april','may','june','all']:
            month = input('Enter the month you would like to analyze, or type "all" for no filter.\n').lower()


    day = input('Enter the day you would like to filter by, or type "all" for no filter.\n').lower()
    while day not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:
            day = input('Enter the day you would like to filter by, or type "all" for no filter.\n').lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city)
    if month != 'all':
        #Converts their given month to a number
        months = ['january','february','march','april','may','june']
        monthnum = months.index(month.lower())+1
        df['Month'] = pd.DatetimeIndex(df['Start Time']).month
        df = df[df['Month']==monthnum]

    if day != 'all':
        #Converts their given weekday to a number
        weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        daynum = weekdays.index(day.capitalize())
        df['Weekday'] = pd.DatetimeIndex(df['Start Time']).weekday
        df = df[df['Weekday']==daynum]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    df['Calc'] = pd.DatetimeIndex(df['Start Time']).month
    a = df['Calc'].mode()
    months = ['january','february','march','april','may','june']
    #Months start at January = 1, so we must adjust the index to match
    a[0] = months[a[0]-1].capitalize()
    print('The most common starting month is: {}'.format(a[0]))

    #display the most common day of week
    df['Calc'] = pd.DatetimeIndex(df['Start Time']).weekday
    a = df['Calc'].mode()
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    a[0] = weekdays[a[0]]
    print('The most common starting day is: {}'.format(a[0]))

    #  display the most common start hour
    df['Calc'] = pd.DatetimeIndex(df['Start Time']).hour
    a = df['Calc'].mode()
    print('The most common starting hour is: {}'.format(a[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #  display most commonly used start station
    a = df['Start Station'].mode()
    print('The most common start station is: {}'.format(a[0]))

    #  display most commonly used end station
    a = df['End Station'].mode()
    print('The most common end station is: {}'.format(a[0]))

    #  display most frequent combination of start station and end station trip
    trip = df['Start Station']+ ' to ' + df['End Station']
    a = trip.mode()
    print('The most common trip is: {}. Please note that these are permutations of travel stations. Going from A to B is considered different than going from B to A.'.format(a[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #  display total travel time
    df['Calc'] = pd.DatetimeIndex(df['End Time'])-pd.DatetimeIndex(df['Start Time'])
    #The datetime subtraction creates a time delta which must be converted to a string to properly display.
    a = str(df['Calc'].sum(axis=0))
    print('The total travel time is: {}'.format(a))

    #  display mean travel time
    a = df['Calc'].mean()
    def days_hours_minutes(td):
        return td.days, td.seconds//3600, (td.seconds//3600)//60, (td.seconds%3600)%60
    d, h, m, s = days_hours_minutes(a)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #  Display counts of user types
    a = df['User Type'].value_counts()
    print('Here is the count of user types: {}'.format(a))

    #  Display counts of gender
    a = df['Gender'].value_counts()
    print('Here is the count of user genders:\n Male: {}\n Female: {}'.format(a[0],a[1]))

    #  Display earliest, most recent, and most common year of birth
    a = df['Birth Year'].min()
    print('The oldest user was born in: {}'.format(int(a)))

    a = df['Birth Year'].max()
    print('The youngest user was born in: {}'.format(int(a)))

    a = df['Birth Year'].mode()
    print('The most common birth year is: {}'.format(int(a)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_prompt(df):
    """Prompts user if they would like to see raw data"""
    i = [0,5]
    while True:
        print('\n' +'-'*40)
        rawprompt = input('Would you like to read 5 more lines of raw data based on your filters? Enter yes or no.\n')
        if rawprompt.lower() == 'no':
            break
        print(df[i[0]:i[1]])
        i[0] +=5
        i[1]+=5

def main():
    while True:
        city, month, day = get_filters()
        city = CITY_DATA[city]
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_prompt(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
