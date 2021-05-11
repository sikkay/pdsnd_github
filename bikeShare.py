import numpy as np
import pandas as pd
import time
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    ask_city = input(
        'Hello! Let\'s explore some US bikeshare data! Which city would you like to look at? Chicago, New York  or Washington: ').lower()
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        if ask_city not in ['washington', 'chicago', 'new york']:
            ask_city = input(
                "The available cities are Washington, New York, Chicago. Let there be space in the word New York. Please choose one of them : \n ").lower()
        else:
            print('You have chosen: ' + ask_city.title())
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input(
        'Please choose a month to filter by (January February...June :) ').lower()
    while True:
        if month not in months:
            print(
                'I do not understand please ensure you choose the first six months in the format below')
            month = input(
                'Please choose a month to filter by (All, January, February....June) ').lower()
        else:
            print('Thank you, you chose : ' + month.title())
        break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input(
        'Please choose a day to filter by (All, Sunday, Monday, ...) ').lower()
    while True:
        if day not in days:
            print(
                'I do not understand please ensure you choose a day of the week or choose all to filter entire week ')
            day = input(
                'Please choose a day to filter by (All, Sunday  , Monday ... ) ').lower()
        else:
            print('Great! you chose : ' + day.title())
            break

    print('-'*40)
    return ask_city, month, day
def load_data(ask_city, month, day):
    if ask_city == 'new york':
        df = pd.read_csv('new_york_city.csv')
    else:
        df = pd.read_csv(CITY_DATA[ask_city])
    # print(df.columns)
   # Loads data for the specified city and filters by month and day if applicable.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['new_month'] = df['Start Time'].dt.month
   # df['time'] = df['Start Time'].dt.time
    df['hour'] = df['Start Time'].dt.hour
    df['new_day'] = df['Start Time'].dt.day
    if month != 'all':
        month = months.index(month)
        df = df[df['new_month'] == month]
        #print('month ', df)
   # else:
        # df = df[df['month'] == [0, 1, 2, 3, 4, 5]]
        # print('all ', df)
    if day != 'all':
        day = days.index(day)
        day_data = df[df['new_day'] == day]
        # print('day ', df)
        #print('filtered ', day_data)
    return df
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    popular_month = df['new_month'].mode()[0]
    # print(popular_month)
    popular_day = df['new_day'].mode()[0]
    popular_hour = df['hour'].mode()[0]
    print('\nCalculating The Most Frequent Times of Travel...\n')
    # printing a pandas variable should be followed by , cause I tried + it failed
    start_time = time.time()
    # TO DO: display the most common month
    print('The most popular month is , ', popular_month)
    # TO DO: display the most common day of week
    print('The most popular day is , ', popular_day)
    # TO DO: display the most common start hour
    print('The most popular hour is , ',  popular_hour, '\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return popular_month, popular_day
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('The total trip duration is, ', total_duration)
    # display mean travel time
    avg_duration = df['Trip Duration'].mean()
    print('The average trip duration is, ', avg_duration)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    start_station = df['Start Station'].mode().values[0]
    print('The most popular station start station \n', start_station)
    # display most commonly used end station
    end_station = df['End Station'].mode().values[0]
    print('\n The most popular station end station \n', end_station)
    # display most frequent combination of start station and end station trip
    pop_combo = df.groupby(
        ['Start Station',  'End Station']).size().nlargest(1)
    print('\n This is the route most people take \n', pop_combo)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df
def user_stats(df, ask_city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # print(df.columns)
    # Display counts of user types
    # .value shows data in a column
    # print(df['User Type'].values)
    # value_counts will group and count each group
    cust_count = df['User Type'].value_counts()
    print('The groups of customers are: ')
    print(cust_count)
    # Display counts of gender
    if ask_city != 'washington':
        gen_count = df['Gender'].value_counts()
        print('\nThe gender types are:  ')
        print(gen_count)
    # Display earliest, most recent, and most common year of birth
    if ask_city != 'washington':
        if 'Birth Year' != 'Nan':
            pop_year = df['Birth Year'].mode()[0]
            earliest = df['Birth Year'].min()
            recent = df['Birth Year'].max()
            print('\n')
            print('The most popular birth year is, ', pop_year)
            print('The earliest birth year is, ', earliest)
            print('The most recent birth year is, ', recent)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def display_data(df):
    """Display 5 rows data of individual trip data if requested."""
    row_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no: ").lower()
    start_loc = 0
    while True:
        if row_data != 'no':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_data = input("Would you like to continue? yes or no: ").lower()
        if view_data.lower() != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
    main()
