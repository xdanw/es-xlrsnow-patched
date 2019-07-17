import sys, string, time, traceback
import com.xhaus.jyson.JysonCodec as json
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

if servicenowServer is None:
    print "No server provided."
    sys.exit(1)

if tableName is None:
    print "No tableName provided."
    sys.exit(1)

if ticket is None:
    print "No Ticket provided."
    sys.exit(1)

if fieldName  is None:
    print "No Field Name provided."
    sys.exit(1)

if fieldValue  is None:
    print "No Field Value provided."
    sys.exit(1)

snClient = ServiceNowClient.create_client(servicenowServer, username, password)

query = "change_request=%s&%s=%s" % ( ticket,fieldName, fieldValue )

try:
    data = snClient.find_record( tableName, query )
    numRecords = len(data)
    print "Found %s records for %s" % (numRecords, ticket)
    data = data[0]
    sysId = data["sys_id"]
    number = data["number"]
    print "Found %s in Service Now with sysId = %s." % (ticket, sysId)
    print "\n"
    print snClient.print_record( data )
except Exception, e:
    exc_info = sys.exc_info()
    traceback.print_exception( *exc_info )
    print e
    print snClient.print_error( e )
    print "Failed to find record in Service Now"
    sys.exit(1)
