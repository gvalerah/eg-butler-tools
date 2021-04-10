# ======================================================================
# Butler Request States Constants definitions
# source file name: request_states.py
# Static Header File. 
# GLVH 2020-10-11
# ----------------------------------------------------------------------
"""
# Request States

These are used to followup Request State upon all workflow stages

*The current Solution implies:*

A Provisioning Request can be:

State       | Description
----------- | -----------
REQUEST     |
  Created   | Created by Requestor, on this stage it can be modified by
            | requestor, once finished and las saved it will be Requested
  Requested | Can be edited for approver only, he can Review it 
            | (Modify request). 
            | Approved request as is or modified, or reject it. 
            | Rejected is a final state.
  Approved  | Once approved, request is handled by Butler Core and will be 
            | changing states until completed (Provisioned) or *-Error, 
            | these are final states.
NUTANIX     |
  Pending   | Approved requests are submited by Butler-Core to Nutanix
            | hipervisor, if succesfull VM creation will be reported as
            | Pending provisioning. On Error its a final state
  Completed | Once provisioned NUTANIX-Completed s the state. Or Error
            | NUTANIX-Error is also a final state.
MONITOR     |
  Completed | All Nutanix Completed VMs are required to be monitored
            | by EG-Monitor, Pending or Completed states are valid, on
            | Error a MONITOR-Error state is setup. This is not a 
            | final nor fatal state, a warning should be raised
COLLECTOR   |
  Completed | As last stage VM need to be populated with request VM CC
            | This is a funal and succesful stage.
            | Nutanix-Complete+Collector-Complete => Request_Provisioned
            | Final successfull state.
"""
# REQUEST
REQUEST_Created     = 0x000002
REQUEST_Requested   = 0x000004
REQUEST_Reviewed    = 0x000008
REQUEST_Approved    = 0x000010
REQUEST_Rejected    = 0x000020
REQUEST_Provisioned = 0x000040
# NUTANIX
NUTANIX_Pending     = 0x000080
NUTANIX_Completed   = 0x000100
NUTANIX_Error       = 0x000200
# MONITOR
MONITOR_Pending     = 0x000400
MONITOR_Completed   = 0x000800
MONITOR_Error       = 0x001000
# COLLECTOR
COLLECTOR_Completed = 0x002000
COLLECTOR_Error     = 0x004000
RESERVED_Reserved   = 0x008000

# Next function code need to be deleted prior production release
def test_request_states():
    print(f'REQUEST Created             = { REQUEST_Created }')
    print(f'REQUEST Created             = { REQUEST_Requested }')
    status = REQUEST_Created | REQUEST_Requested
    print(f'REQUEST status              = { status                       }')
    #    print(f'Is REQUEST                  = { status & REQUEST             }')
    print(f'Is REQUEST_Created          = { status & REQUEST_Created     }')
    print(f'Is REQUEST_Reqested         = { status & REQUEST_Requested   }')
    print(f'Is REQUEST_Reviewed         = { status & REQUEST_Reviewed    }')
    print(f'Is REQUEST_Approved         = { status & REQUEST_Approved    }')
    print(f'Is REQUEST_Rejected         = { status & REQUEST_Rejected    }')
    print(f'Is REQUEST_Provisioned      = { status & REQUEST_Provisioned }')
    #    print(f'Is NUTANIX                  = { status & NUTANIX             }')
    print(f'Is NUTANIX_Pending          = { status & NUTANIX_Pending     }')
    print(f'Is NUTANIX_Completed        = { status & NUTANIX_Completed   }')
    print(f'Is NUTANIX_Error            = { status & NUTANIX_Error       }')
    #    print(f'Is MONITOR                  = { status & MONITOR             }')
    print(f'Is MONITOR_Pending          = { status & MONITOR_Pending     }')
    print(f'Is MONITOR_Completed        = { status & MONITOR_Completed   }')
    print(f'Is MONITOR_Error            = { status & MONITOR_Error       }')
    #    print(f'Is COLLECTOR                = { status & COLLECTOR           }')
    print(f'Is COLLECTOR_Completed      = { status & COLLECTOR_Completed }')
    print(f'Is COLLECTOR_Error          = { status & COLLECTOR_Error     }')
    print(f'Is RESERVED_Reserved        = { status & RESERVED_Reserved   }')

    if (status & REQUEST_Created): print('is a REQUEST already Created')
    if (status & REQUEST_Requested): print('is a REQUEST already Requested')
    if (status & NUTANIX_Pending): print('is a NUTANIX VM  Pending')

# ----------------------------------------------------------------------
