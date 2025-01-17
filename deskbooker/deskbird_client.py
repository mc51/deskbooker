import json
import logging
from datetime import datetime

import requests

from .auth import get_access_token

logging.basicConfig()
log = logging.getLogger("client")
log.setLevel(logging.DEBUG)


class DeskbirdClient:
    access_token = None
    refresh_token = None
    token_key = None
    resource_id = None
    zone_item_id = None
    workspace_id = None

    def __init__(
        self,
        refresh_token,
        token_key,
        resource_id,
        workspace_id,
        zone_item_id=None,
    ):
        self.refresh_token = refresh_token
        self.token_key = token_key
        self.resource_id = resource_id
        self.workspace_id = workspace_id
        self.zone_item_id = zone_item_id
        self.access_token = get_access_token(self.token_key, self.refresh_token)

    def set_status(
        self, date: datetime, status: str = "Mobile office"
    ) -> requests.Response:
        """Set office status for given date"""

        url = "https://app.deskbird.com/api/v1.1/officePlanning"
        start_time = end_time = date
        start_time = start_time.replace(hour=8)
        end_time = end_time.replace(hour=18)

        body = {
            "day": str(start_time.date()),
            "startTime": int(start_time.timestamp() * 1000),
            "endTime": int(end_time.timestamp() * 1000),
            "status": status,
            "bookingIds": [],
            "officeId": "cktu67xoy002s01s6eu2w428t",
            "optionId": "ckz2ht36w000sa1zr46a7ed92",
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        log.debug(f"Body: {body}")
        return requests.post(url, headers=headers, data=json.dumps(body))

    def set_zone_item_id(self, zone_name, desk_id):
        url = (
            f"https://app.deskbird.com/api/v1.1/internalWorkspaces/"
            f"{self.workspace_id}/zones?internal"
        )
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        response = json.loads(requests.get(url=url, headers=headers).text)
        log.debug(response.get("results"))
        for zone in response["results"]:
            if zone_name == zone["name"]:
                for desk in zone["availability"]["zoneItems"]:
                    if desk_id == desk["name"].split(" ")[-1]:
                        self.zone_item_id = desk["id"]
                        return
                raise KeyError(f"desk_id: {desk_id} not found in {zone_name}")
        raise KeyError(f"zone_name: {zone_name} does not exists")

    def book_desk(self, date):
        url = "https://web.deskbird.app/api/v1.1/user/bookings"
        if not self.zone_item_id:
            raise Exception("ZONE_ITEM_ID missing from environment")
        body = {
            "internal": True,
            "isAnonymous": False,
            "isDayPass": True,
            "resourceId": self.resource_id,
            "zoneItemId": self.zone_item_id,
            "workspaceId": self.workspace_id,
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        start_time = end_time = date
        start_time = start_time.replace(hour=8)
        end_time = end_time.replace(hour=18)
        body["bookingStartTime"] = int(start_time.timestamp() * 1000)
        body["bookingEndTime"] = int(end_time.timestamp() * 1000)

        return requests.post(url, headers=headers, data=json.dumps(body))

    def get_bookings(self, limit=10):
        url = (
            "https://app.deskbird.com/api/v1.1/user/bookings"
            f"?upcoming=true&skip=0&limit={limit}"
        )
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        return requests.get(url, headers=headers)

    def checkin(self):
        url = (
            f"https://app.deskbird.com/api/v1.1/workspaces/"
            f"{self.workspace_id}/checkIn"
        )
        body = {
            "isInternal": True,
            "resourceId": self.resource_id,
            "workspaceId": self.workspace_id,
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        bookings = json.loads(self.get_bookings().text)
        for booking in bookings["results"]:
            is_today = (
                datetime.fromtimestamp(int(booking["bookingStartTime"] / 1000)).date()
                == datetime.today().date()
            )
            if is_today:
                if booking["checkInStatus"] == "checkedIn":
                    print(
                        f"Already checked in to {booking['zoneItemName']}"
                        f" in {booking['resource']['name']}!"
                    )
                    return
                else:
                    body["bookingId"] = booking["id"]
                    response = requests.post(
                        url, headers=headers, data=json.dumps(body)
                    )
                    print("Checked in!")
                    return response
        print("You don't have any valid bookings")
