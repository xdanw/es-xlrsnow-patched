#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

# This CreateChangeRequest is based on the original create_task.py (servicenow.CreateTaskNew virtual type)
# with additional fields copied from ES customization

from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null
from servicenow.markdown.markdown_logger import MarkdownLogger as mdl


class ServiceNowRecordClient(object):

    def __init__(self, task_vars):
        self.table_name = task_vars['tableName']
        self.task_vars = task_vars
        assert_not_null(task_vars['servicenowServer'], "No server provided.")
        assert_not_null(task_vars['shortDescription'], "Short description is mandatory when creating a task.")
        self.sn_client = ServiceNowClient.create_client(task_vars['servicenowServer'], task_vars['username'], task_vars['password'])
        if 'acceptanceCriteria' in self.task_vars.keys():
            assert_not_null(task_vars['acceptanceCriteria'], "Acceptance criteria are mandatory when creating a story.")

    def set_from_task_vars(self, source_name, target_object, target_name=None):
        if source_name in self.task_vars.keys() and self.task_vars[source_name]:
            if target_name is None:
                target_name = source_name
            target_object[target_name] = self.task_vars[source_name]

    # From ES 1.0.7v2 CreateChangeRequest.py
    def NoneToEmpty(text):
        return '' if text is  None else text

# Reference: 
# Original ES custom content payload = """ {
#     "short_description"   : shortDescription   <-- Already in native code.   self.set_from_task_vars('shortDescription', content, 'short_description')
#   , "comments"            : comments   <-- Already in native code.   self.set_from_task_vars('comments', content, 'comments')
#   , "cmdb_ci"             : NoneToEmpty(configurationItem) <-- ** OVERRIDE ** 
#   , "assignment_group"    : NoneToEmpty(assignmentGroup)   <-- Already in native code.   self.set_from_task_vars('assignmentGroup', content, 'assignment_group')
#   , "assigned_to"         : NoneToEmpty(assignTo)   <-- Already in native code.   self.set_from_task_vars('assignedTo', content, 'assigned_to')
#   , "start_date"          : plannedStartDateTime  <-- ** ADD ** 
#   , "end_date"            : plannedEndDateTime  <-- ** ADD ** 
#   , "u_environment"       : environment  <-- ** ADD ** 
#   , "u_change_coordinator"       : changeCoordinator  <-- ** ADD ** 
#   , "category"       : categorym  <-- ** ADD ** 
#   , "implementation_plan"       : implementationPlan  <-- ** ADD ** 
#   , "test_plan"       : testPlan  <-- ** ADD ** 
#   , "backout_plan"       : backoutPlan  <-- ** ADD ** 
#   , "type"       : changeType  <-- ** OVERRIDE ** 
#   , "change_plan"  : changePlan }   <-- ** ADD ** 

    def process_record(self):
        content = {}
        self.set_from_task_vars('shortDescription', content, 'short_description')  #   OK -- Equivalent present in ES custom payload.
        self.set_from_task_vars('description', content)  #  not in ES - but keeping for now (uncomment if SNOW says it's required, comment out if SNOW says unknown field)
        self.set_from_task_vars('assignmentGroup', content, 'assignment_group')  #   OK -- Equivalent present in ES custom payload.
        self.set_from_task_vars('assignedTo', content, 'assigned_to')  #   OK -- Equivalent present in ES custom payload.
        self.set_from_task_vars('priority', content)  #  not in ES - but keeping for now
        self.set_from_task_vars('state', content)  #  not in ES - but keeping for now
        #    (Original) self.set_from_task_vars('ciSysId', content, 'cmdb_ci')
        self.set_from_task_vars('configurationItem', content, 'cmdb_ci') # "cmdb_ci"             : NoneToEmpty(configurationItem)
        self.set_from_task_vars('comments', content, 'comments')  #   OK -- Equivalent present in ES custom payload.

        # Now here's the custom task inputs
        self.set_from_task_vars('plannedStartDateTime', content, 'start_date') # "start_date"          : plannedStartDateTime
        self.set_from_task_vars('plannedEndDateTime', content, 'end_date') # "end_date"            : plannedEndDateTime
        self.set_from_task_vars('environment', content, 'u_environment') # "u_environment"       : environment
        self.set_from_task_vars('changeCoordinator', content, 'u_change_coordinator') # "u_change_coordinator"       : changeCoordinator
        self.set_from_task_vars('categorym', content, 'category') # "category"       : categorym
        self.set_from_task_vars('implementationPlan', content, 'implementation_plan') # "implementation_plan"       : implementationPlan
        self.set_from_task_vars('testPlan', content, 'test_plan') # "test_plan"       : testPlan
        self.set_from_task_vars('backoutPlan', content, 'backout_plan') # "backout_plan"       : backoutPlan
        self.set_from_task_vars('changePlan', content, 'change_plan') # "change_plan"  : changePlan
        # Modified
        self.set_from_task_vars('changeType', content, 'type') # "type"       : changeType

        # These are not in the original, so we are removing them for now. 
        # self.set_from_task_vars('changeRequest', content, 'change_request') # only used in Create Story
        # self.set_from_task_vars('workNotes', content, 'work_notes')
        # self.set_from_task_vars('storyPoints', content, 'story_points')
        # self.set_from_task_vars('epic', content, 'epic')
        # self.set_from_task_vars('product', content)
        # self.set_from_task_vars('sprint', content)
        # self.set_from_task_vars('acceptanceCriteria', content, 'acceptance_criteria')
        #   (Original) self.set_from_task_vars('taskType', content, 'type')   # This one will be modified
        # self.set_from_task_vars('plannedHours', content, 'planned_hours')
        # self.set_from_task_vars('story', content)
        # self.set_from_task_vars('impact', content)
        # self.set_from_task_vars('urgency', content)
        
        #Also sending release info.
        content['x_xlbv_xl_release_identifier'] = str(release.id)
        content['x_xlbv_xl_release_state'] = str(release.status)

        for k, v in self.task_vars['additionalFields'].items():
            content[k] = v
            
        response = self.sn_client.create_record(self.table_name, content, getCurrentTask().getId())
        return response

    def print_links(self, sys_id, ticket, data):
        mdl.println("Created '{}' with sysId '{}' in Service Now. \n".format(ticket, sys_id))
        mdl.print_hr()
        mdl.print_header3("__Links__")
        url = '%s/%s.do?sys_id=%s' % (self.sn_client.service_now_url, self.table_name, sys_id)
        mdl.print_url("Record Form View", url)

    def process(self):
        response = self.process_record()
        sys_id = response['target_sys_id']
        data = self.sn_client.get_record(self.table_name,sys_id)
        self.print_links(sys_id, data['number'], data)
        return sys_id, data['number'], data

sysId, Ticket, data = ServiceNowRecordClient(locals()).process()
