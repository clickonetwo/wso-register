from .wso_data import GroupData, SubmitterData
from .physical_group import (
    execute_physical_group_change,
    execute_temporary_virtual_group_change,
)

SUBMITTER_DATA = SubmitterData(name="Dan B (D26 Web Admin)", phone="510-926-0499")
TUESDAY_GROUP_DATA = GroupData(
    name="Albany-Berkeley Tuesday Night AFG",
    listing_page="https://al-anonbythebay.org/meeting-berkeley-albany-tuesday-night/",
    wso_id=645,
    day_of_week=2,
    start_hour=20,
    start_minute=0,
    duration=90,
    repeat_type="weekly",
    repeat_index=0,
    public_email="al.anon.group.645@gmail.com",
    online_platform="Zoom",
)

# execute_physical_group_change(SUBMITTER_DATA, TUESDAY_GROUP_DATA)
execute_temporary_virtual_group_change(SUBMITTER_DATA, TUESDAY_GROUP_DATA)
