import time
import pandas as pd
import numpy as np
from datetime import datetime

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    CITY_DATA['new york'] = CITY_DATA['ny'] = CITY_DATA['new york city']
    CITY_DATA['wa'] = CITY_DATA['washington']
    while True:
        city = input('Which city would you like to check? (Chicago, New York, or Washington)\n').lower()

        # Check for invalid user input
        if city.lower() not in ('chicago', 'new york city', 'new york', 'washington', 'ny', 'wa'):
            print('Please enter a city from the list')
        else:
            break

        # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month would you like to see? (January, February, March, April, May, June) or would you'
                      ' rather have them all?\n').lower()

        # Check for invalid user input
        if month.lower() not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print('Please enter a month from (January to June)')
        else:
            break

        # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day would you like to see? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday)'
                    ' or all days?\n').lower()

        # Check for invalid user input
        if day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print('Please choose a day from the list given')
        else:
            break
    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df = pd.DataFrame(df)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) + 1
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month, day of week, and hour
    most_common_month = df['month'].mode()[0]
    most_common_day = df['day_of_week'].mode()[0]
    popular_hour = df['hour'].mode()[0]
    print('Most common month: "{}" while the most popular day is: "{}" and most popular hour: "{}"'
          .format(most_common_month, most_common_day, popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display the count of used start station
    print('The count of used Start Station: ', df['Start Station'].count())

    # display most commonly used start station
    most_popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = df['Start Station'].value_counts().max()
    print('The most popular Start Station: "{}" with a count of: {}'.format(most_popular_start_station,
                                                                            popular_start_station_count))

    # display most commonly used end station
    most_popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = df['End Station'].value_counts().max()
    print('The most popular End Station is: "{}" with a count of: {}'.format(most_popular_end_station,
                                                                             popular_end_station_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = np.sum(df['Trip Duration'])

    print('The total time traveled: ', total_travel_time)

    # display average travel time
    avg_travel_time = np.average(df['Trip Duration'])
    print('and the average time traveled: ', avg_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display total of user types
    total_user_types = df['User Type'].count()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print('The total number of users: "{} users" divided into two categories:'.format(total_user_types))
    for user, val in count_user_types.items():
        print(user, val)

    print('-' * 40)

    # Display counts of gender
    while 'Gender' in df.columns:
        count_gender = df['Gender'].value_counts()
        for name, val in count_gender.items():
            print('The total number of {} subscribers: {}'.format(name, val))
        if 'Male' > 'Female':
            print('*You can see that male subscribers are more than female subscribers*')
        else:
            print('*Female subscribers are more than male subscribers*')
        print('-' * 40)

        # Display earliest, most recent, and most common year of birth
        popular_year_of_birth = int(df['Birth Year'].mode()[0])
        oldest_year_of_birth = df['Birth Year'].min()
        youngest_year_of_birth = df['Birth Year'].max()

        current_year = datetime.now().year
        popular_age = current_year - popular_year_of_birth
        youngest_age = current_year - youngest_year_of_birth
        oldest_age = current_year - oldest_year_of_birth

        print('The youngest age: ', int(youngest_age))

        if oldest_age > 90:
            print('The oldest year is over 90')
        else:
            print('The oldest age: ', int(oldest_age))

        print('The most popular age: ', popular_age)

        # Calculating the average age:

        break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def request_data(df):
    # ask user to show some data upon request
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?\n").lower()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_display = input("Do you wish to continue?: ").lower()
        if view_display == 'no':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        request_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
