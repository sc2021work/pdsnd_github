import time
import pandas as pd
import numpy as np

# Program bikeshare.py is used to query bicycle sharing data
# from 3 large cities and compute varying statistics about
# the trips and users.
# Month selection for the current files is limited to January
# thru June.

CITY_DATA = { 'chicago': 'chicago.csv',
              'new_york_city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to choose analysis and filtering critieria (city, month, day of week).
    Args: 
        None
    Returns:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day   - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print("\nHello! Let\'s explore some US bikeshare data!\n")
    
    # Request city, default to Chicago
    
    cities={"1":"chicago","2":"new_york_city","3":"washington"}
    city_val=input('Please choose city -- Enter 1, 2 or 3 <default 1>:\n1: Chicago\n2: New York City\n3: Washington\n>').strip()
    if city_val in cities.keys():
       city=cities.get(city_val)
    else:
       city=cities.get("1")
    print("City selected: {}\n".format(city.title().replace('_',' ')))  
    
    # Request filtering choice
    
    filter_flag=input("Would you like to filter the data y or n? Enter y or n <default n>\n>").upper().strip()
   
    if (filter_flag == 'Y'):         
       # If filtering selected, request month and/or day
       print("Filtering selected...\n")  
 
       # Request month January thru June, default to "all"
    
       months={"1":"january","2":"february","3":"march","4":"april","5":"may","6":"june"}    
       month_val=input("Please choose month -- Enter 1-6 <default all months JAN-JUN>:\n1: JAN    4: APR\n2: FEB    5: MAY\n3: MAR    6: JUN\n>").strip()
       if month_val in months.keys():
          month=months.get(month_val)
       else:
          month="all"
       print("Month selected: {}\n".format(month.capitalize()))  
    
       # Request day (Monday thru Sunday, default to "all")

       days={"1":"monday","2":"tuesday","3":"wednesday","4":"thursday","5":"friday","6":"saturday","7":"sunday"}
       day_val=input("Please choose day of week -- Enter 1-7 <default all>:\n1: MON    4: THU    7: SUN\n2: TUE    5: FRI \n3: WED    6: SAT\n>").strip()
       if day_val in days.keys():
          day=days.get(day_val)
       else:
          day="all"
       print("Day selected: {}\n".format(day.capitalize()))     
    else:
       # If filtering not selected, default month and day to "all"
       month="all"
       day="all"  
       print("Filtering NOT selected...\n")      
    

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day, if applicable.

    Args:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day   - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """ 
    try:
       # Read the csv file
       df = pd.read_csv(CITY_DATA[city])

       # Convert the Start Time column to datetime
       df['Start Time'] = pd.to_datetime(df['Start Time'])
    
       # Extract month, day of week and hour from Start Time to create new columns
       df['month'] = df['Start Time'].dt.month
       df['day_of_week'] = df['Start Time'].dt.weekday_name
       df['hour'] = df['Start Time'].dt.hour

       # Filter by month, if applicable
       if month != 'all':
           # Use the index of the months list to get the corresponding int
           months = ['january', 'february', 'march', 'april', 'may', 'june']
           month = months.index(month) + 1

           # Filter by month to create the new dataframe
           df = df[df['month'] == month]

       # Filter by day of week if applicable
       if day != 'all':
           # Filter by day of week to create the new dataframe
           df = df[df['day_of_week'] == day.title()]
                
    except Exception as e:
       print("Exception occurred reading/filtering city data: {}".format(e))         
       df=pd.DataFrame()
        
    return df


def time_stats(df):
    """
    Displays statistics on the  most frequent times of travel.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        None
    """ 
    
    try: 
       print("\n"+"-"*47)
       print("Calculating Most Frequent Times of Travel...\n")
       start_time = time.time()
   
       # Display the most common month
       freq_month=df['month'].mode()[0]
       freq_month_cnt=df['month'].value_counts()[freq_month]
       print("Month: {}\nCount: ({})".format(freq_month, freq_month_cnt))

       # Display the most common day of week
       freq_day=df['day_of_week'].mode()[0]
       freq_day_cnt=df['day_of_week'].value_counts()[freq_day]
       print("\nDay:   {}\nCount: ({})".format(freq_day, freq_day_cnt))

       # Display the most common start hour
       freq_hr=df['hour'].mode()[0]
       freq_hr_cnt=df['hour'].value_counts()[freq_hr]
       print("\nHour:  {}\nCount: ({})".format(freq_hr, freq_hr_cnt))

       print("\nExecution time %.3f seconds" % (time.time() - start_time))
       print("-"*47)
    except Exception as e:
       print("Exception occurred calculating statistics for most frequent times of travel: {}".format(e)) 

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        None
    """ 
    
    try: 
       print("Calculating Most Popular Stations and Trip...\n")
       start_time = time.time()

       # Display most commonly used start station
       start_stat=df['Start Station'].mode()[0]
       start_stat_cnt=df['Start Station'].value_counts()[start_stat]
       print("Start Station: {}\nCount: ({})".format(start_stat, start_stat_cnt))
        
       # Display most commonly used end station
       end_stat=df['End Station'].mode()[0]
       end_stat_cnt=df['End Station'].value_counts()[end_stat]
       print("\nEnd Station:   {}\nCount: ({})".format(end_stat, end_stat_cnt))
    
       # Display most frequent combination of start station and end station trip   
       trip=(df['Start Station']+"|"+df['End Station']).mode()[0]
       trip_start=trip.split('|')[0]
       trip_end=trip.split('|')[1]
       trip_cnt=len(df.loc[(df['Start Station']==trip_start) & (df['End Station']==trip_end),['End Station']])
       print("\nTrip:          {}\n               To\n               {}\nCount:         ({})".format(trip_start, trip_end,trip_cnt))    

       print("\nExecution Time %.3f seconds" % (time.time() - start_time))
       print("-"*47)        
    except Exception as e:
       print("Exception occurred calculating statistics for popular stations and trip: {}".format(e))  
    
def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip durations.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        None
    """ 
    
    try:   
       print("Calculating Trip Duration...\n")
       start_time = time.time()

       # Display total travel time
       travel_sum_secs=df['Trip Duration'].sum()
       print("Total Travel Time:   {} seconds".format(travel_sum_secs))
      
       # Display average travel time
       travel_avg_secs=df['Trip Duration'].mean()
       print("Average Travel Time: %.2f seconds" %(travel_avg_secs))

       print("\nExecution Time %.3f seconds" % (time.time() - start_time))
       print("-"*47)        
    except Exception as e:
       print("Exception occurred calculating statistics for total and average trip duration: {}".format(e))  

def user_stats(df):
    
    """
    Displays gender and birth year statistics on bikeshare users, if available.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        None
    """ 
    
    try:    
       print("Calculating User Stats...\n")
       start_time = time.time()

       # Display user types and counts
       user_types=df['User Type'].value_counts() 
       print("User Type Counts:")
       print(user_types)
       df['User Type'].value_counts()

    # Display gender counts
       if 'Gender' in df:
           gender_count=df['Gender'].value_counts()
           print("\nGender Counts:") ## {}".format(df['Gender'].value_counts()))
           print(gender_count)
       else:
           print("\n*** Gender information NOT available in the dataset ***")
            
       # Display birth year counts
       if 'Birth Year' in df:        
          # TO DO: Display earliest, most recent, and most common year of birth
          print("\nEarliest Birth Year:    {}".format(int(df['Birth Year'].min())))
          print("Latest Birth Year:      {}".format(int(df['Birth Year'].max())))
          print("Most Common Birth Year: {}".format(int(df['Birth Year'].mode()[0])))
          print("\nExecution Time %.3f seconds" % (time.time() - start_time))
       else:
          print("\n*** Birth year information NOT available in the dataset ***")
       print("-"*47)    
    except Exception as e:
       print("Exception occurred calculating statistics for user type, gender, birth year: {}".format(e))  
    
def raw_data(df):    
    """
    Views raw data, 5 records at a time.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        None
    """ 
    
    try:    
        raw_flag=True
        start_index=0
        while raw_flag:
            if (start_index==0):
               raw_flag=input("Would you like to see raw data? Enter y or n <default n>\n").lower().strip()
            else:
               raw_flag=input("More raw data? Enter y or n <default n>\n").lower().strip() 
            
            if (raw_flag != 'yes') and (raw_flag != 'y'):
               break
            else:
               if (start_index+4 < len(df)):
                  print(df[start_index:start_index+5])           
                  start_index+=5
               else:
                  print(df[start_index:len(df)])
                  break
    except Exception as e:
       print("Exception occurred viewing raw data: {}".format(e))  
    
def main():
    """
    Main function for controlling the query and statistic computations for
    the bicycle shareing data from 3 large cities.

    Args:
        None
    Returns:
        None
    """ 
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if (len(df) > 0):
           print("*"*35)
           print('Calculating Statistics for:\n     City:  {}\n     Month: {}\n       Day: {}'.format(city.title().replace('_',' '),month.title(),day.title()))
           print("*"*35)
           time_stats(df)
           station_stats(df)
           trip_duration_stats(df)
           user_stats(df)
           raw_data(df)
           restart = input("\nWould you like to restart? Enter y or n <default n>\n>").lower().strip()
        else:
           print("\n*** NO bikeshare data found for this city, please try another city ***")
           restart='y'

        if (restart != 'yes') and (restart != 'y'):
            break
    print("\nSuccessful program completion.\n")

if __name__ == "__main__":
	main()
