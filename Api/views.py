from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import influxdb_client
import random
import time
from influxdb_client.client.write_api import SYNCHRONOUS
from rest_framework.decorators import api_view

# configuration of influxdb
bucket = 'TimeDataProject'
org = 'TECHstile' 
token = "xSZb3jJZP8oHNsEjUKLOLNhEveJiNDfqkmhLuDgBTD6b2_XpWNvWX8QFzjz5P91BNiIyWEJf7QFGgj7-Cam4RQ=="
url = "http://localhost:8086"
client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)


@api_view(['GET'])
def readData(request):
    bucket = 'TimeDataProject'
    org = 'TECHstile'
    token = "xSZb3jJZP8oHNsEjUKLOLNhEveJiNDfqkmhLuDgBTD6b2_XpWNvWX8QFzjz5P91BNiIyWEJf7QFGgj7-Cam4RQ=="
    url = "http://localhost:8086"
    client = influxdb_client.InfluxDBClient(
        url=url,

        token=token,
        org=org
    )
    print("connection Done!")
    query_api = client.query_api()
    query = f'from(bucket: "{bucket}") \
    |> range(start: -1h) \
    |> filter(fn: (r) => r._measurement == "data1" and r._field == "temperature")'
    result = query_api.query(org=org, query=query)
    data = []
    for table in result:
        for row in table.records:
            time = row.values["_time"]
            temperature = row.values["_value"]
            measured_in = row.values["measured_in"]
            data_point = {
                "time": time,
                "temperature": temperature,
                "measured in": measured_in
            }
            data.append(data_point)

    return JsonResponse(data, safe=False)

# write small data


def writeData(request):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    userInput = int(input("Give Temp:"))
    c = influxdb_client.Point("data1").tag(
        "measured_in", "Celsius").field("temperature", userInput)

    f = influxdb_client.Point("data1").tag(
        "measured_in", "Fahrenheit").field("temperature", userInput)
    # for point in data_points:
    write_api.write(bucket=bucket, org=org, record=c)
    write_api.write(bucket=bucket, org=org, record=f)
    print('Data inserted Successfully')

# write bulk data simultaneously


def randomData(request):
    for i in range(0, 2):
        data = int(random.uniform(5, 100))
        write_api = client.write_api(write_options=SYNCHRONOUS)
        c = influxdb_client.Point("data1").tag(
            "measured_in", "Celsius").field("temperature", data)
        fahren = int((data*9)/5 + 32)
        f = influxdb_client.Point("data1").tag(
            "measured_in", "Fahrenheit").field("temperature", fahren)
        write_api.write(bucket=bucket, org=org, record=c)
        write_api.write(bucket=bucket, org=org, record=f)

        print("Inserted Successfully")
        time.sleep(1)

    return HttpResponse(status=204)
