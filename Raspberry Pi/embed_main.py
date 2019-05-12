# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# License: Public Domain\
import boto3
import time
import csv
from boto3.dynamodb.conditions import Key, Attr
import aws
from picamera import PiCamera
from time import sleep
import time
from threading import Thread
# Import the ADS1x15 module.
from digitalio import DigitalInOut
import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711
from adafruit_pn532.spi import PN532_SPI
import Adafruit_ADS1x15
import board
import busio
from busio import I2C
from board import SDA,SCL
#import Adafruit_ADXL345
#import adafruit_l3gd20
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)

weight = 0
rfid_id = ""
num = 0

pn532 = PN532_SPI(spi, cs_pin, debug=False)
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
pn532.SAM_configuration()

hx = HX711(13, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(520)
hx.reset()
price_dict = {
    "Cookie": "2000.88",
    "Apple": "2.08",
    "Water": "20.0"
}

def db_operation(userid, item, amount):
    dynamodb = aws.getResource('dynamodb', 'us-east-1')
    DYNAMO_TABLE_NAME = "shopping_cart"
    table_dynamo = dynamodb.Table(DYNAMO_TABLE_NAME)
    response = table_dynamo.scan()
    current_record = None
    for record in response['Items']:
        if (record["user_id"] == userid) and (record["item"] == item) and (record["payment"]=="unpaid"):
            current_record = record
    if (current_record == None) and (amount>0):
        response = table_dynamo.put_item(
            Item={
                'timestamp': str(time.time()),
                'user_id': userid,
                'amount': str(amount),
                'price': price_dict[item],
                'item': item,
                'payment':"unpaid"
            }
        )
        return
    elif (current_record != None) and (amount<0):
        table_dynamo.delete_item(Key={'timestamp': current_record["timestamp"]})
    elif (current_record != None) and (amount>0):
        response = table_dynamo.update_item(
            Key={
                'timestamp': current_record["timestamp"]
            },
            UpdateExpression="set amount = :a",
            ExpressionAttributeValues={
                ':a': str(float(current_record["amount"]) + float(amount))
            },
            ReturnValues="UPDATED_NEW"
        )



def s3_operation(filename, userid, amount):
    s3 = aws.getResource('s3', 'us-east-1')
    s3.Bucket('iot-bucket-llha').upload_file(filename, userid+'_'+str(amount)+'.jpg')
    
    
class WeightThread(Thread):
 
    def __init__(self):
        ''' Constructor. '''
        Thread.__init__(self)

 
    def run(self):
        global weight
        while True:
            try:
                # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
                # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
                # Comment the two lines "val = hx.get_weight(5)" and "print(val" and uncomment the three lines to see what it prints.
                #np_arr8_string = hx.get_np_arr8_string()
                #binary_string = hx.get_binary_string()
                #print(binary_string + " " + np_arr8_string
                
                # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
                # val = hx.get_weight(5)
                val = hx.read_long()
                val_out1=int(496700)-int(val)
                val_out2= int((val_out1)/21)
                weight = int((val_out1)/210)*10
        #        print(val, val_out1,val_out2,val_out3)
        
                #print(weight, 'gram')
        
                # To get weight from both channels (if you have load cells hooked up 
                # to both channel A and B), do something like this
                #val_A = hx.get_weight_A(5)
                #val_B = hx.get_weight_B(5)
                #print("A: %s  B: %s" % ( val_A, val_B )

                hx.power_down()
                hx.power_up()
                time.sleep(0.1)
            except (KeyboardInterrupt, SystemExit):
                cleanAndExit()




class RfidThread(Thread):
 
    def __init__(self):
        ''' Constructor. '''
        Thread.__init__(self)

 
    def run(self):
        global rfid_id
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            print('.', end="")
            # Try again if no card is available.
            if uid is None:
                continue
            #print('Found card with UID:', [hex(i) for i in uid])
            rfid_id = ''
            l = [str(int(i)) for i in uid]
            for c in l:
                rfid_id += c+'-'
            rfid_id = rfid_id[:-1]
            
            time.sleep(0.5)




# Create an ADS1115 ADC (16-bit) instance.

#i2c = I2C(SCL,SDA)
# Main loop.
def check_rfid(id):
    if rfid_id == '4-8-122-4-4-41-147':
        return 'Cookie'
    if rfid_id == '4-8-122-4-3-65-63':
        return 'Water'
    
    #dic = 
    #if rfid_id == ['0x4', '0x8', '0x7a', '0x4', '0x4', '0x29', '0x93']:
     #   print('asdfdasf')
    #    db_operation('thisisuserid','Cookie')     

if __name__ == "__main__":
    adc = Adafruit_ADS1x15.ADS1115(address = 0x48)
    camera = PiCamera()
    camera.rotation = 180
    #acel = Adafruit_ADXL345.ADXL345(address = 0x53)
    weightThread = WeightThread()
    rfidThread = RfidThread()
    weightThread.start()
    rfidThread.start()
    last_6_weights = [0,0,0,0,0,0]
    diff_list = [0,0,0,0,0]
    pos = 0
    time.sleep(0.5)
    stable_weight = 0
    flag = 0
    while True:

        if pos < 6:
            last_6_weights[pos] = weight
            if pos > 0:
                diff_list[pos-1] = last_6_weights[pos]-last_6_weights[pos-1]
            pos += 1
        else:
            last_6_weights.pop(0)
            last_6_weights.append(weight)
            diff_list.pop(0)
            diff_list.append(last_6_weights[-1]-last_6_weights[-2])
        
        #print('rfid:',rfid_id)
        if sum(diff_list) < 50:
            flag = 0
            print('stable')
        if abs(sum(diff_list[0:2])) < 100 and abs(sum(diff_list[3:5])) < 100 and diff_list[2] > 120:
            print('adding!!!!!!!!!!!!!!!!!!!!!!!!!!!','weight:',sum(last_6_weights[3:6])/3 - sum(last_6_weights[0:3])/3)
            if rfid_id != "":
                print('add rfid item')
                item = check_rfid(rfid_id)
                db_operation('thisisuserid',item,1)
                rfid_id = ""
            else:
                print('use camera!')
                camera.start_preview()
                sleep(3)
                camera.capture('/home/pi/cart/pic/tem.jpg')
                camera.stop_preview()
                s3_operation('/home/pi/cart/pic/tem.jpg', 'thisisuserid',
 last_6_weights[-1] - last_6_weights[0])
                
        if abs(sum(diff_list[0:2])) < 100 and abs(sum(diff_list[3:5])) < 100 and diff_list[2] < (-120):
            print('popping!!!!!!!!!!!!!!!!! waiting for rfid scanning')
            sleep(3)
            if rfid_id != "":
                print('pop rfid item')
                item = check_rfid(rfid_id)
                db_operation('thisisuserid',item,-1)
                rfid_id = ""
            else:
                print('use camera!')
                camera.start_preview()
                sleep(3)
                camera.capture('/home/pi/cart/pic/tem.jpg')
                camera.stop_preview()
                s3_operation('/home/pi/cart/pic/tem.jpg', 'thisisuserid', 
last_6_weights[-1]-last_6_weights[0])
        
        print('weight:',last_6_weights,diff_list)
        print('rfid_id:',rfid_id)
        time.sleep(0.8)
    