from .group_data import GroupData
from .physical_group import execute_physical_group_change

TUESDAY_GROUP_DATA = GroupData(
    name="Albany-Berkeley Tuesday Night AFG",
    wso_id=645,
    day_of_week=2,
    start_hour=20,
    start_minute=0,
    duration=90,
    repeat_type="weekly",
    repeat_index=0,
    public_email="al.anon.group.645@gmail.com",
)

execute_physical_group_change(TUESDAY_GROUP_DATA)
