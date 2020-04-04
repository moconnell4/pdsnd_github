import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    i = True
    while i == True:
        city = input('Enter the city you would like data for (Chicago, Washington, New York City):\n').lower()
        if city in CITY_DATA:
            print('\nThank you\n')
            break
        else:
            print('That\'s not a valid city. Please choose from Chicago, New York City, or Washington.\n')
            continue
    # get user input for month (all, january, february, ... , june)
    i = True
    while i == True:
        month = input('Enter the month you would like data for (January, February, March, April, May, June, or all):\n').lower()
        if month in months:
            print('\nThank you\n')
            break
        else:
            print('That\'s not a valid month or there is no data for that month. Accepted months are January to June. If you would like all months, please input "all".\n')
            continue
    # get user input for day of week (all, monday, tuesday, ... sunday)
    i = True
    while i == True:
        day = input('Enter the day of the week you would like data for (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all):\n').lower()
        if day in days:
            print('\nThank you\nPlease wait for the results...')
            break
        else:
            print('That\'s not a valid day of the week. If you would like all days, please input "all".\n')
            continue

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
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_month = df['month'].mode()[0]
    most_month = months[most_month].title()
    print('Most common month: ', most_month)
    
    # display the most common day of week
    most_dow = df['day_of_week'].mode()[0]
    print('Most common day of the week: ', most_dow)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('Most common start hour: ', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print('Most common start station: ', most_start_station)

    # display most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    print('Most common end station: ', most_end_station)

    # create column of start and end station
    df['start_end'] = df['Start Station'] + ' to ' + df['End Station']
    # display most frequent combination of start station and end station trip
    most_start_end = df['start_end'].mode()[0]
    print('Most frequent combination of start station and end station trip: ', most_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = np.sum(df['Trip Duration'])
    print('Total travel time: ', total_travel)

    # display mean travel time
    mean_travel = np.mean(df['Trip Duration'])
    print('Mean of travel time: ', mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user = df['User Type'].value_counts()
    print('Counts of each user type: \n', count_user.to_string())

    # Ignore Gender and Birth Year if city chosen was Washington
    if city == 'washington':
        print('\nWashington does not report gender or birth year')
    else:
        # Display counts of gender
        count_gender = df['Gender'].dropna().value_counts()
        print('\nCounts of each Gender: \n', count_gender.to_string(), '\nNote: only subscribers record gender.')

        # Display earliest, most recent, and most common year of birth
        earliest_yob = int(np.min(df['Birth Year']))
        recent_yob = int(np.max(df['Birth Year']))
        common_yob = int(df['Birth Year'].dropna().mode()[0])
        print('\nEarliest year of birth: ', earliest_yob, '\nMost recent year of birth: ', recent_yob, '\nMost common year of birth: ', common_yob)
        


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
    
        # Display 5 lines of the filtered raw data until user specifies to stop
        n = 0
        while True:
            raw = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            if raw.lower() == 'yes':
                print(df.iloc[n], '\n\n', df.iloc[n+1], '\n\n', df.iloc[n+2], '\n\n', df.iloc[n+3], '\n\n', df.iloc[n+4], '\n')
                n += 5
                continue
            else:
                break
        # Ask if user would like start again
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
