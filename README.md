# EECSE6765-Intelligent-Shopping-Cart
This project is implemented on three platforms:
1. A embedded system (we used Raspberry Pi 3b+) running python code
2. A mobile application (simulated by web application frame) running JavaScript
3. A variaty of AWS services

To use code in this repository, you need:
1. Peripheral embedded system hardware: weight sensor HX711, Raspberry Pi camera, RFID reader PN532
2. Paste these three lambda functions to your own AWS account. Fetch and checkout are triggered by API gateway, and image is triggered by S3.
3. Create API gateway, and create your own API key. (We have deleted the API key in source code for safety reasons)
4. Paste your API key into the apiGatewaybot functions.
5. Build the mobile application and download it to your phone

Demo video and detailed project information is available on https://iotcolumbia2019llha.weebly.com
