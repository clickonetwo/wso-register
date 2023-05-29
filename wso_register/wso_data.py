from dataclasses import dataclass


@dataclass(kw_only=True)
class SubmitterData:
    name: str
    phone: str
    email: str = "webadmin@alanonbythebay.org"

    def wso_phone(self) -> (str, str):
        digits = "".join(filter(str.isdigit, self.phone))
        if not digits:
            return "", ""
        return digits[0:3], digits[3:]


@dataclass(kw_only=True)
class GroupData:
    name: str
    listing_page: str

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
    location_instructions: str = ""

    # online meetings
    online_platform: str | None = None
    online_url: str | None = None
    online_meeting_id: str | None = None
    online_meeting_password: str | None = None

    # public information
    language: str | None = None
    public_email: str = ""
    participant_types: set[str] | None = None
    members_only: bool = False
    options: set[str] | None = None

    # CMA information
    cma_first_name: str = ""
    cma_last_name: str = ""
    cma_street_address_1: str = ""
    cma_street_address_2: str = ""
    cma_city: str = ""
    cma_state: str = ""
    cma_zip: str = ""
    cma_country: str = ""
    cma_phone: str = ""
    cma_email: str = ""

    # GR information
    gr_first_name: str = ""
    gr_last_name: str = ""
    gr_street_address_1: str = ""
    gr_street_address_2: str = ""
    gr_city: str = ""
    gr_state: str = ""
    gr_zip: str = ""
    gr_country: str = ""
    gr_phone: str = ""
    gr_email: str = ""
    gr_comment: str = ""

    def meeting_type(self) -> str:
        if not self.physical_location:
            return "Online only"
        elif not self.online_platform:
            return "In-person only"
        else:
            return "both In-person and Online"

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
        return wso_day, str(wso_hour), str(wso_minute), wso_am_pm

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

    def wso_location(self) -> str:
        result_lines: [str] = []
        if self.physical_location and self.location_instructions:
            result_lines.append(self.location_instructions)
        if self.listing_page:
            result_lines.append(f"See {self.listing_page} for complete information.")
        return "\n".join(result_lines)

    def has_cma(self) -> bool:
        return (
            self.cma_first_name
            and self.cma_last_name
            and self.cma_street_address_1
            and self.cma_city
            and self.cma_state
            and self.cma_zip
            and self.wso_cma_phone()[1]
            and self.cma_email
            and True
        )

    def wso_cma_country(self) -> str:
        if not self.address_country:
            return "United States"
        if self.address_country == "Canada":
            return "Canada"
        if self.address_country == "Bermuda":
            return "Bermuda"
        return "United States"

    def wso_cma_phone(self) -> (str, str):
        digits = "".join(filter(str.isdigit, self.cma_phone))
        return digits[0:3], digits[3:]

    def has_gr(self) -> bool:
        return (
            self.gr_first_name
            and self.gr_last_name
            and self.gr_street_address_1
            and self.gr_city
            and self.gr_state
            and self.gr_zip
            and True
        )

    def wso_gr_country(self) -> str:
        if not self.address_country:
            return "United States"
        if self.address_country == "Canada":
            return "Canada"
        if self.address_country == "Bermuda":
            return "Bermuda"
        return "United States"

    def wso_gr_phone(self) -> (str, str):
        digits = "".join(filter(str.isdigit, self.gr_phone))
        if not digits:
            return "", ""
        return digits[0:3], digits[3:]
