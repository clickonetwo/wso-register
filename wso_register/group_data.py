from dataclasses import dataclass, field


@dataclass(kw_only=True)
class GroupData:
    name: str

    # schedule
    day_of_week: int  # Sunday = 0
    start_hour: int  # 24-hour clock
    start_minute: int  # normalized to quarter-hour for WSO
    duration: int  # minutes
    repeat_type: str = "weekly"  # one of weekly, monthly
    repeat_index: int = 0  # weekly spacing (0, 1, ...), or which week of the month

    # wso registration info
    wso_id: int | None = None
    district: int = 26
    area: str = "California North"
    active: bool = True

    # physical meetings
    physical_location: str | None = None
    address_street_1: str = ""
    address_street_2: str = ""
    address_city: str | None = None
    address_state: str | None = None
    address_zip: str | None = None
    address_country: str | None = None

    # online meetings
    online_location: str | None = None
    online_url: str | None = None
    online_zoom_id: str | None = None
    online_zoom_password: str | None = None

    # contact and attendee information
    language: str | None = None
    public_email: str = ""
    participant_types: set[str] | None = None
    members_only: bool = False
    options: set[str] | None = None

    def meeting_type(self) -> str:
        if not self.physical_location:
            return "Online-only"
        elif not self.online_location:
            return "Physical-only"
        else:
            return "Hybrid"

    def wso_language(self, is_restricted: bool = True) -> str:
        if not self.language:
            return "English"
        if self.language.lower() == "spanish":
            return "Spanish"
        if self.language.lower() == "french":
            return "French"
        if is_restricted:
            return "English"
        return self.language

    def wso_meeting_place(self) -> str:
        if not self.physical_location:
            return "Currently meeting online only, see link for details"
        else:
            return self.physical_location

    def wso_city(self) -> str:
        if not self.address_city:
            return "Berkeley"
        return self.address_city

    def wso_state(self) -> str:
        if not self.address_state:
            return "California"
        return self.address_state

    def wso_zip(self) -> str:
        if not self.address_zip:
            return "94707"
        return self.address_zip

    def wso_country(self) -> str:
        if not self.address_country:
            return "United States"
        if self.address_country == "Canada":
            return "Canada"
        if self.address_country == "Bermuda":
            return "Bermuda"
        return "United States"

    def wso_participant_type(self) -> str | None:
        if not self.participant_types:
            return None
        wso_types = {
            "parent": "Parents of Alcoholics",
            "aca": "Adult Children",
            "youth": "Young Adults",
            "poc": "People of Color",
            "women": "Women",
            "men": "Men",
            "lgbtqia+": "LGBTQIA+",
        }
        for pt in self.participant_types:
            if wso_pt := wso_types.get(pt.lower()):
                return wso_pt
        return None

    def wso_attendees(self) -> str:
        if self.members_only:
            return "Families and Friends only"
        return "Families, Friends, and Observers welcome"

    def wso_schedule(self) -> (str, str, str, str):
        wso_days = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        wso_day = wso_days[self.day_of_week % 8]
        wso_hour = self.start_hour % 12 if (self.start_hour % 12) != 0 else 12
        wso_am_pm = "AM" if (self.start_hour % 24) < 12 else "PM"
        wso_minute = self.start_minute % 60
        if wso_minute < 15:
            wso_minute = 0
        elif wso_minute < 30:
            wso_minute = 15
        elif wso_minute < 45:
            wso_minute = 30
        else:
            wso_minute = 45
        return (wso_day, str(wso_hour), str(wso_minute), wso_am_pm)

    def wso_options(self) -> set[str]:
        if not self.options:
            return set()
        wso_options = {
            "intro": "Introductory",
            "institution": "Limited Access",
            "fragrance-free": "Fragrance Free",
            "ada": "Handicap Access",
            "child-care": "Child Care",
            "asl": "Sign Language",
            "smoking": "Smoking Permitted",
            "beginner": "Beginners",
        }
        result = set()
        for option in self.options:
            if wso_option := wso_options.get(option.lower()):
                result.add(wso_option)
        return result

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**dict)
