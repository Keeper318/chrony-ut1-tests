import re
from datetime import datetime

import requests


def dut1(mjd: int) -> float:
    body = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:tns="urn:org.iers.datacenter.eop" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/">
        <SOAP-ENV:Body>
            <mns:readEOP xmlns:mns="urn:org.iers.datacenter.eop" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                <param xsi:type="xsd:string">UT1-UTC</param>
                <series xsi:type="xsd:string">Bulletin A</series>
                <mjd xsi:type="xsd:string">{mjd}</mjd>
            </mns:readEOP>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>"""
    response = requests.post("https://datacenter.iers.org/eris/webservice/eop/eopServer.php", data=body)
    return float(re.search("<return.*?>(.+)</return>", response.text).group(1))


input_str = input("Enter MJD or leave blank to use the current date: ").strip()
print("dUT1 =", dut1(int(input_str or (datetime.utcnow().toordinal() + 1721424 - 2400000))), "ms")
