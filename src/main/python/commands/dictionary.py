from .access_nat import *
from .filter import *
from .cluster import *

commands = {
    'add-rule': add_rule,
    'delete-rule': delete_rule,
    'disable-rule': disable_rule,
    'enable-rule': enable_rule,
    'clear-backups':clear_backups,
    'cleanup-rulebase':review_no_hit,
    'cleanup-disabled-rules':review_disabled,
    'filter-activity':filter_low_activity,
    'filter-target':filter_target,
    'get-interfaces': get_interfaces
}