from datetime import datetime

from Yummy.models import OpeningTime


def today_opening_time(All_restaurant):
    all_opening_times = []
    for restaurant in All_restaurant:
        filtered_restaurant = OpeningTime.objects.filter(restaurant=restaurant).values_list('weekday', 'from_hour',
                                                                                            'restaurant__name')
        today = datetime.now().strftime('%A')
        for value_list in filtered_restaurant:
            if value_list[0] == today:
                # print(f'{value_list[2]} => {value_list[1]} => {today}')
                all_opening_times.append(value_list[1])
                break
    return all_opening_times

def get_opening_times(opening_time):
    list_of_opening_time = []

    for i in range(7):
        weekday_dic = {
            'day': None,
            'from_hour': None,
            'to_hour': None
        }
        if opening_time[i][1] != None:  # if Restaurant is not closed
            weekday_dic['from_hour'] = opening_time[i][1]
            weekday_dic['to_hour'] = opening_time[i][2]
        else:
            weekday_dic['from_hour'] = None
            weekday_dic['to_hour'] = None
        weekday_dic['day'] = opening_time[i][0]
        list_of_opening_time.append(weekday_dic)  # Append the result of checked day

    return list_of_opening_time
