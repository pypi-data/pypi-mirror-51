"""
DB Utils functions for the project
"""
import sys
from os.path import dirname as opd, realpath as opr
import os
import time
import sqlite3

basedir = opd(opd(opd(opr(__file__))))
sys.path.append(basedir)

from sharkradar.Config.Config import Config

def createTableIfNotExists():
    """
    Creates the SERVICE_RD, SERVICE_LOGS table in SQLite3 file mode, if table doesn't exist
    Columns of Table
            KEYS:            		VALUES:
               ---------        	-------------
              i) ip 			  	ip address associated with micro-service
             ii) port			  	port associated with micro-service
            iii) service_name	  	unique name of the micro-service
             iv) status			  	status (up/down) sent from the micro-service
              v) mem_usage		  	Current memory usage
             vi) cpu_usage		  	Current CPU usage
            vii) network_throughput Current network throughput
       viii) req_active 		No. of requests currently being processed by
                                                            the instance
             ix) success_rate 		Fraction of requests successfully served
              x) health_interval  	The time interval specified by the micro-service
                                                            at which it will send health report to service
                                                            R/D continuously
             xi) status             Status of the discovery log
            xii) retry_id           Retry ID in discovery log
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS SERVICE_RD
         (SERVICE_NAME  TEXT    NOT NULL,
         IP            TEXT     NOT NULL,
         PORT          TEXT NOT NULL,
         MEM_USAGE     	REAL NOT NULL,
         CPU_USAGE      REAL NOT NULL,
         NW_TPUT_BW_RATIO REAL NOT NULL,
         REQ_ACTIVE_RATIO REAL NOT NULL,
         SUCCESS_RATE REAL NOT NULL,
         TIME_STAMP     BIGINT NOT NULL,
         HEALTH_INTERVAL BIGINT NOT NULL);''')
    conn.execute('''CREATE TABLE IF NOT EXISTS SERVICE_LOGS
         (SERVICE_NAME  TEXT    NOT NULL,
         IP            TEXT     NOT NULL,
         PORT          TEXT NOT NULL,
         MEM_USAGE      REAL NOT NULL,
         CPU_USAGE      REAL NOT NULL,
         NW_TPUT_BW_RATIO REAL NOT NULL,
         REQ_ACTIVE_RATIO REAL NOT NULL,
         SUCCESS_RATE REAL NOT NULL,
         TIME_STAMP     BIGINT NOT NULL,
         HEALTH_INTERVAL BIGINT NOT NULL);''')
    conn.execute('''CREATE TABLE IF NOT EXISTS DISCOVERY_LOGS
         (SERVICE_NAME  TEXT    NOT NULL,
         IP            TEXT     NOT NULL,
         PORT          TEXT NOT NULL,
         TIME_STAMP     BIGINT NOT NULL,
         STATUS         TEXT NOT NULL,
         RETRY_ID       TEXT NOT NULL);''')
    conn.commit()
    conn.close()


def findServiceByNameAndIpAndPort(service_name, ip, port):
    """
    Find services by service name, IP address and port number

    @params:service_name: A string, representing the service name
    @params:ip: IP address of the service
    @params:port : Port number of the service
    @return: List of the query results from DB
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    response = conn.execute(
        """SELECT * FROM SERVICE_RD WHERE SERVICE_NAME = ? AND IP = ? AND PORT = ?""",
        (service_name,
         ip,
         port)).fetchall()
    conn.close()
    return response


def findServiceByName(service_name):
    """
    Find services by service name

    @params:service_name: A string, representing the service name
    @return: List of the query results from DB
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    service_instances = conn.execute(
        """SELECT * from SERVICE_RD WHERE SERVICE_NAME = ?""",
        (service_name,
         )).fetchall()
    conn.close()
    return service_instances

def getAllService():
    """
    Find all services at current time

    @return: List of the query results from DB
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    service_instances = conn.execute(
        """SELECT * from SERVICE_RD""").fetchall()
    conn.close()
    return service_instances

def updateServiceByAll(
        current_time_stamp,
        health_interval,
        mem_usage,
        cpu_usage,
        nw_tput_bw_ratio,
        req_active_ratio,
        success_rate,
        service_name,
        ip,
        port):
    """
    Update services details

    @params:current_time_stamp: Current time stamp
    @params:health_interval: Health interval frequency in secs, the maximum threshold after which
                            if health status is not received, the service will be de-registered
    @params:mem_usage: Memory usage in % of service
    @params:cpu_usage: CPU usage in % of service
    @params:nw_tput_bw_ratio: Ratio of current network throughput with maximum capacity (bandwidth) in %
    @params:req_active_ratio: Ratio of current requests being handled with maximum requests limit in %
    @param:success_rate: Ratio of successful response by total requests in %
    @params:service_name: A string, representing the service name
    @params:ip: IP address of the service
    @params:port : Port number of the service
    @return: Total number of rows updated
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """UPDATE SERVICE_RD SET  TIME_STAMP = ?, HEALTH_INTERVAL = ?, MEM_USAGE = ?, CPU_USAGE = ?, NW_TPUT_BW_RATIO = ?, REQ_ACTIVE_RATIO = ?, SUCCESS_RATE = ?  WHERE SERVICE_NAME = ? AND IP = ? AND PORT = ?""",
        (current_time_stamp,
         health_interval,
         mem_usage,
         cpu_usage,
         nw_tput_bw_ratio,
         req_active_ratio,
         success_rate,
         service_name,
         ip,
         port))
    conn.commit()
    total_changes = conn.total_changes
    conn.close()
    return total_changes


def insertServiceByAll(
        service_name,
        ip,
        port,
        current_time_stamp,
        health_interval,
        mem_usage,
        cpu_usage,
        nw_tput_bw_ratio,
        req_active_ratio,
        success_rate):
    """
    Insert services details

    @params:service_name: A string, representing the service name
    @params:ip: IP address of the service
    @params:port : Port number of the service
    @params:current_time_stamp: Current time stamp
    @params:health_interval: Health interval frequency in secs, the maximum threshold after which
                            if health status is not received, the service will be de-registered
    @params:mem_usage: Memory usage in % of service
    @params:cpu_usage: CPU usage in % of service
    @params:nw_tput_bw_ratio: Ratio of current network throughput with maximum capacity (bandwidth) in %
    @params:req_active_ratio: Ratio of current requests being handled with maximum requests limit in %
    @param:success_rate: Ratio of successful response by total requests in %
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO SERVICE_RD (SERVICE_NAME, IP, PORT, TIME_STAMP, HEALTH_INTERVAL, MEM_USAGE, CPU_USAGE, NW_TPUT_BW_RATIO, REQ_ACTIVE_RATIO, SUCCESS_RATE) \
						VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (service_name,
         ip,
         port,
         current_time_stamp,
         health_interval,
         mem_usage,
         cpu_usage,
         nw_tput_bw_ratio,
         req_active_ratio,
         success_rate))
    conn.commit()
    conn.close()

def insertServiceByAllPersist(
        service_name,
        ip,
        port,
        current_time_stamp,
        health_interval,
        mem_usage,
        cpu_usage,
        nw_tput_bw_ratio,
        req_active_ratio,
        success_rate):
    """
    Insert services details persistant

    @params:service_name: A string, representing the service name
    @params:ip: IP address of the service
    @params:port : Port number of the service
    @params:current_time_stamp: Current time stamp
    @params:health_interval: Health interval frequency in secs, the maximum threshold after which
                            if health status is not received, the service will be de-registered
    @params:mem_usage: Memory usage in % of service
    @params:cpu_usage: CPU usage in % of service
    @params:nw_tput_bw_ratio: Ratio of current network throughput with maximum capacity (bandwidth) in %
    @params:req_active_ratio: Ratio of current requests being handled with maximum requests limit in %
    @param:success_rate: Ratio of successful response by total requests in %
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO SERVICE_LOGS (SERVICE_NAME, IP, PORT, TIME_STAMP, HEALTH_INTERVAL, MEM_USAGE, CPU_USAGE, NW_TPUT_BW_RATIO, REQ_ACTIVE_RATIO, SUCCESS_RATE) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (service_name,
         ip,
         port,
         current_time_stamp,
         health_interval,
         mem_usage,
         cpu_usage,
         nw_tput_bw_ratio,
         req_active_ratio,
         success_rate))
    conn.commit()
    conn.close()

def getServicePersist(limit=250):
    """
    Fetch service log records by limit
    
    @params:limit: latest n records
    @return: List of the query results from DB
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    service_instances = conn.execute(
        """SELECT * from SERVICE_LOGS ORDER BY TIME_STAMP DESC LIMIT ?""",
        (limit,)).fetchall()
    conn.close()
    return service_instances

def insertDiscoveryPersist(
        service_name,
        ip,
        port,
        current_time_stamp,
        status,
        retryid):
    """
    Insert discovery details persistant

    @params:service_name: A string, representing the service name
    @params:ip: IP address of the service
    @params:port : Port number of the service
    @params:current_time_stamp: Current time stamp
    @params:status: Status of the service 
    @params:retryid: Retry ID for the discovery log
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO DISCOVERY_LOGS (SERVICE_NAME, IP, PORT, TIME_STAMP, STATUS, RETRY_ID) \
                        VALUES (?, ?, ?, ?, ?, ?)""",
        (service_name,
         ip,
         port,
         current_time_stamp,
         status,
         retryid))
    conn.commit()
    conn.close()

def getDiscoveryPersist(limit=250):
    """
    Fetch service log records by limit
    
    @params:limit: latest n records
    @return: List of the query results from DB
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    service_instances = conn.execute(
        """SELECT * from DISCOVERY_LOGS ORDER BY TIME_STAMP DESC LIMIT ?""",
        (limit,)).fetchall()
    conn.close()
    return service_instances

def updateDiscoveryPersist(
        status,
        retryid):
    """
    Update discovery details persistant

    @params:service_name: A string, representing the service name
    @params:ip: IP address of the service
    @params:port : Port number of the service
    @params:current_time_stamp: Current time stamp
    @params:status: Status of the service 
    @params:retryid: Retry ID for the discovery log
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """UPDATE DISCOVERY_LOGS SET STATUS = ? WHERE RETRY_ID = ?""",
        (status,
         retryid))
    conn.commit()
    conn.close()

def getLatestRecordsDiscoveryLogs(service_name, ip, port, latest_records):
    """ Fetch latest n records from discovery logs corresponding to 
        service name, IP and port

        @params:service_name: A string representing service name
        @params:ip: IP address
        @params:port: Port numbers
        @params:latest_records: Limit 
        @return: List of records in ordered by desc timestamp
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    discovery_instances = conn.execute(
        """SELECT STATUS FROM DISCOVERY_LOGS WHERE SERVICE_NAME = ? AND IP = ? AND PORT = ? ORDER BY TIME_STAMP DESC LIMIT ?""",
        (service_name,
         ip,
         port,
         latest_records)).fetchall()
    conn.close()
    return discovery_instances

def deleteServiceByNameAndIpAndPort(service_name, ip, port):
    """
    Delete services by service name, Ip and port

    @params:service_name: A string, representing the service name
    @params:ip: IP Address of the service
    @params:port: Port number of the service
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """DELETE FROM SERVICE_RD WHERE SERVICE_NAME = ? AND IP = ? AND PORT = ?""",
        (service_name,
         ip,
         port))
    conn.commit()
    conn.close()


def deleteServiceByNameAndTimestampDifferenceWithHealthInterval(service_name):
    """
    Find services by service name, based on services who are declared dead

    Dead -> Services who haven't sent health status post their health interval

    @params:service_name: A string, representing the service name
    """
    DB_PATH = Config.getDbPath()
    conn = sqlite3.connect(DB_PATH)
    current_time_epoch = time.time()
    conn.execute(
        """DELETE FROM SERVICE_RD WHERE SERVICE_NAME  = ? AND ?  - TIME_STAMP > HEALTH_INTERVAL""",
        (service_name,
         current_time_epoch))
    conn.commit()
    conn.close()
