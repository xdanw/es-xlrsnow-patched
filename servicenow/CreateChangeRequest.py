#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

# This is the original CreateChangeRequest.py, with the following patches: 
# update to use     import servicenow.client.ServiceNowClient
# added taskid      snClient.create_record( tableName, content, getCurrentTask().getId() )

import sys, string, time, traceback
import com.xhaus.jyson.JysonCodec as json
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

def NoneToEmpty(text):
    return '' if text is  None else text

if servicenowServer is None:
    print "No server provided."
    sys.exit(1)

if tableName is None:
    print "No tableName provided."
    sys.exit(1)

if shortDescription is None:
    print "No shortDescription provided."
    sys.exit(1)

if comments is None:
    print "No comments provided."
    sys.exit(1)

if configurationItem is None:
   print "No Configuration Item provided"
   sys.exit(1)

if assignmentGroup is None:
   print "No Assignment Group provided"
   sys.exit(1)

if assignTo is None:
   print "No Assigned To provided"
   sys.exit(1)

if plannedStartDateTime is None:
   print "No Planned Start DateTime provided"
   sys.exit(1)

if plannedEndDateTime is None:
   print "No Planned End DateTime provided"
   sys.exit(1)

if environment is None:
    print "No Environment provided"
    sys.exit(1)

if changeCoordinator is None:
    print "No Change Coordinator provided"
    sys.exit(1)

if categorym is None:
    print "No Category provided"
    sys.exit(1)

if implementationPlan is None:
    print "No Implementation Plan provided"
    sys.exit(1)

if testPlan is None:
    print "No Test Plan provided"
    sys.exit(1)

if backoutPlan is None:
    print "No Backout Plan provided"
    sys.exit(1)

if changeType is None:
    print "No Change Type provided"
    sys.exit(1)

if changePlan is None:
    print "No Change Plan provided"
    sys.exit(1)

snClient = ServiceNowClient.create_client(servicenowServer, username, password)

content = """
{
  "short_description"   : "%s"
, "comments"            : "%s"
, "cmdb_ci"             : "%s"
, "assignment_group"    : "%s"
, "assigned_to"         : "%s"
, "start_date"          : "%s"
, "end_date"            : "%s"
, "u_environment"       : "%s"
, "u_change_coordinator"       : "%s"
, "category"       : "%s"
, "implementation_plan"       : "%s"
, "test_plan"       : "%s"
, "backout_plan"       : "%s"
, "type"       : "%s"
, "change_plan"  : "%s"
}
""" % ( 
  shortDescription
, comments
, NoneToEmpty(configurationItem)
, NoneToEmpty(assignmentGroup)
, NoneToEmpty(assignTo)
, plannedStartDateTime
, plannedEndDateTime
, environment
, changeCoordinator
, categorym
, implementationPlan
, testPlan
, backoutPlan
, changeType
, changePlan
)

print "Sending content %s" % content

try:
    data = snClient.create_record( tableName, content, getCurrentTask().getId() )
    sysId = data["sys_id"]
    Ticket = data["number"]
    print "Created %s in Service Now." % (sysId)
    print "Created %s in Service Now." % (Ticket)
    print "\n"
    print snClient.print_record( data )
except Exception, e:
    exc_info = sys.exc_info()
    traceback.print_exception( *exc_info )
    print e
    print snClient.print_error( e )
    print "Failed to create record in Service Now"
    sys.exit(1)


