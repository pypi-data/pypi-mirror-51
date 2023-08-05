import random, time
from matialvarezs_request_handler import utils as matialvarezs_request_handler_utils


def get_delay_schedule(total_time_sleep, lower_boundary=1, upper_boundary=10, **options):
    delay_schedule = list()
    if total_time_sleep == 0:
        delay_schedule.append(0)

    # print("total time sleep", total_time_sleep)
    if total_time_sleep > 0:
        if options.get('time_in_minutes', False) is True:
            total_time_sleep = total_time_sleep * 60

        while True:
            random_time = random.randint(lower_boundary, upper_boundary)
            # print("antes de append sum(delay_schedule) + random_time",sum(delay_schedule) + random_time)
            if sum(delay_schedule) + random_time > total_time_sleep:
                continue
            else:
                # print("agrego numero")
                delay_schedule.append(random_time)
            # if sum(delay_schedule) + random_time > total_time_sleep:
            #     continue
            # print("despues de append sum(delay_schedule) + random_time", sum(delay_schedule) + random_time)
            if sum(delay_schedule) == total_time_sleep:
                break

    if options.get("debug", False):
        print("total time sleep", total_time_sleep)
        print(delay_schedule)
    return delay_schedule


def time_sleep(total_time_sleep, **options):
    delay_schedule = get_delay_schedule(total_time_sleep, **options)  # list()
    # if options.get('time_in_minutes',False) is True:
    #     total_time_sleep = total_time_sleep*60
    # while sum(delay_schedule) < total_time_sleep:
    #     delay_schedule.append(random.randint(1, 10))

    print(delay_schedule)
    for delay in delay_schedule:
        time.sleep(delay)


def should_stop(url):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    #results = requests.get(headers=headers, url=url).json()
    results = matialvarezs_request_handler_utils.send_get_and_get_response(url,headers=headers).json()
    # print("results:",results,results['stop'])
    return eval(results['stop'])


def time_sleep_with_stop_url(total_time_sleep, url, lower_boundary=1, upper_boundary=10, **options):
    delay_schedule = get_delay_schedule(total_time_sleep, lower_boundary, upper_boundary, **options)
    # delay_schedule = list()
    # if options.get('time_in_minutes', False) is True:
    #     total_time_sleep = total_time_sleep * 60
    #
    # while sum(delay_schedule) < total_time_sleep:
    #     delay_schedule.append(random.randint(lower_boundary, upper_boundary))
    # if options.get("debug", False):
    #     print("total time sleep", total_time_sleep)
    #     print(delay_schedule)
    for delay in delay_schedule:
        # print("should_stop(url)",should_stop(url))
        # print("current delay",delay)
        # stop_sleep = False
        stop_sleep = should_stop(url)
        # print("stop_sleep",stop_sleep, type(stop_sleep))
        if stop_sleep:
            # print("DETENCION DESDE URL")
            return None
        else:
            # print("ESPERO EL TIEMPO TIME-SLEEP")
            time.sleep(delay)
    return delay_schedule
