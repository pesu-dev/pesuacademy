"""This module handles the scraping of the timetable from the PESU Academy website."""

import json
import re
from datetime import datetime

import httpx

from pesuacademy import constants
from pesuacademy.models import ClassSession, Slot, Time, Timetable
from pesuacademy.util import _build_params


class _TimetablePageHandler:
    @staticmethod
    async def _get(session: httpx.AsyncClient) -> Timetable:
        """Fetches the timetable page, extracts JSON data, and reconstructs the weekly time_slots.

        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.

        Returns:
            Timetable: An object containing the reconstructed weekly time_slots.

        Raises:
            httpx.HTTPStatusError: If the request to the timetable page fails.
            ValueError: If the JSON data cannot be found or parsed.
        """
        params = _build_params(constants._PageURLParams.Timetable)
        response = await session.get(constants.PAGES_BASE_URL, params=params)
        response.raise_for_status()

        html_content = response.text
        template_data, class_data = _TimetablePageHandler._extract_json_data(html_content)
        time_slots_info, ordered_slots = _TimetablePageHandler._process_template(template_data)

        schedule_by_day = _TimetablePageHandler._build_schedule_by_day(time_slots_info, ordered_slots, class_data)
        return Timetable(days=schedule_by_day)

    @staticmethod
    def _extract_json_data(html_content: str) -> tuple[dict, dict]:
        """Extracts the JSON data from the page source into two dictionaries: template_data and class_data."""
        template_match = re.search(r"var timeTableTemplateDetailsJson=([^;]+);", html_content)
        data_match = re.search(r"var timeTableJson=([^;]+);", html_content)

        if not template_match or not data_match:
            raise ValueError("Could not find timetable JSON data in the page source.")
        # template_data holds the time slots template
        # class_data holds the actual timetable data
        template_data = json.loads(template_match.group(1))
        class_data = json.loads(data_match.group(1))
        return template_data, class_data

    @staticmethod
    def _process_template(template_data: dict) -> tuple[dict[int, dict], list[int]]:
        """Processes the template data to extract time slots and their order, including breaks."""
        time_slots_info: dict[int, dict] = {}
        ordered_slots: list[int] = []

        for slot in template_data:
            order = slot["orderedBy"]
            start_time = datetime.strptime(slot["startTime"], "%I:%M:%S %p")
            end_time = datetime.strptime(slot["endTime"], "%I:%M:%S %p")
            duration = int((end_time - start_time).total_seconds() // 60)

            # Check the status: 1 means it's a break, 0 is a class
            is_break = slot.get("timeTableTemplateDetailsStatus") == 1
            time_obj = Time(start=start_time.time(), end=end_time.time(), duration=duration)
            time_slots_info[order] = {
                "time": time_obj,
                "is_break": is_break,
            }
            if order not in ordered_slots:
                ordered_slots.append(order)

        ordered_slots.sort()
        return time_slots_info, ordered_slots

    @staticmethod
    def _build_schedule_by_day(
        time_slots_info: dict[int, dict], ordered_slots: list[int], class_data: dict
    ) -> dict[str, list[Slot]]:
        """Reconstructs the weekly time_slots based on the provided data."""
        days_map = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday"}
        schedule_by_day: dict[str, list[Slot]] = {day: [] for day in days_map.values()}

        for day_index, day_name in days_map.items():
            for slot_order in ordered_slots:
                slot_info = time_slots_info[slot_order]
                time_str = slot_info["time"]
                is_break_slot = slot_info["is_break"]

                class_session = None
                if not is_break_slot:
                    # key format: ttDivText_{day_index}_{slot_order}_1
                    # e.g., ttDivText_3_5_1 for Wednesday's 5th slot
                    key = f"ttDivText_{day_index}_{slot_order}_1"

                    if key in class_data:
                        details = class_data[key]
                        # Extract subject code and name
                        # Subject details are in the format "ttSubject_&&SubjectCode-SubjectName"
                        subject_full = details[0].split("_&&")[-1]
                        # Use regex to extract subject code and name while handling optional "(LAB)" suffix
                        # Subject code can be in the format "UE24CS151B (LAB)" or "UE24CS151B"
                        code_match = re.match(r"([A-Z0-9]+(?:\s*\(LAB\))?)\s*-\s*(.*)", subject_full)
                        if code_match:
                            subject_code, subject_name = code_match.groups()
                        else:
                            subject_code, subject_name = "N/A", subject_full
                        # Extract faculty names
                        # faculty names are in the format "ttFaculty_&&faculty Name"
                        facultys = [d.split("_&&")[-1] for d in details[1:] if "ttFaculty" in d]

                        class_session = ClassSession(code=subject_code, name=subject_name, faculty=", ".join(facultys))
                schedule_by_day[day_name].append(Slot(time=time_str, is_break=is_break_slot, session=class_session))
        return schedule_by_day
