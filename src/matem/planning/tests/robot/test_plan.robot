# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s matem.planning -t test_plan.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src matem.planning.testing.MATEM_PLANNING_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_plan.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Plan
  Given a logged-in site administrator
    and an add plan form
   When I type 'My Plan' into the title field
    and I submit the form
   Then a plan with the title 'My Plan' has been created

Scenario: As a site administrator I can view a Plan
  Given a logged-in site administrator
    and a plan 'My Plan'
   When I go to the plan view
   Then I can see the plan title 'My Plan'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add plan form
  Go To  ${PLONE_URL}/++add++plan

a plan 'My Plan'
  Create content  type=plan  id=my-plan  title=My Plan


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the plan view
  Go To  ${PLONE_URL}/my-plan
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a plan with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the plan title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
