"""
LearnSphere AI: Multi-Subject Course and Track State Management
Provides centralized utilities for retrieving and selecting active subjects and courses.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from database.db import get_all_courses, get_course_by_code, get_course_by_id, get_all_subjects


def get_active_course() -> Dict[str, Any]:
    """Retrieves the currently active course record from session state, defaulting to python."""
    query_track = st.query_params.get("track")
    if query_track and "active_course_code" not in st.session_state:
        st.session_state["active_course_code"] = query_track

    code = st.session_state.get("active_course_code", "python")
    course = get_course_by_code(code)
    if not course:
        all_courses = get_all_courses(active_only=True)
        if all_courses:
            course = all_courses[0]
            st.session_state["active_course_code"] = course["code"]
        else:
            return {
                "id": 1,
                "code": "python",
                "name": "Python Fundamentals",
                "subject_name": "Programming",
                "subject_code": "programming",
                "description": "Core algorithmic thinking and procedural syntax."
            }
    return course


def set_active_course(code: str) -> None:
    """Updates the active course in session state."""
    st.session_state["active_course_code"] = code


def set_active_course_by_id(course_id: int) -> Optional[Dict[str, Any]]:
    """Updates the active course in session state using course ID."""
    course = get_course_by_id(course_id)
    if course:
        st.session_state["active_course_code"] = course["code"]
        return course
    return None


def get_available_tracks() -> List[Dict[str, Any]]:
    """Returns list of active courses."""
    return get_all_courses(active_only=True)


def render_course_selector(key: str = "track_selector", label: str = "Curriculum Track", on_change_rerun: bool = True) -> Dict[str, Any]:
    """Renders a standard compact track selector dropdown synced with session state."""
    courses = get_available_tracks()
    if not courses:
        return get_active_course()

    course_labels = [f"{c['name']} ({c['subject_name']})" for c in courses]
    active_course = get_active_course()

    default_idx = 0
    for idx, c in enumerate(courses):
        if c["code"] == active_course["code"]:
            default_idx = idx
            break

    widget_key = f"{key}_{active_course['code']}"

    selected_label = st.selectbox(
        label,
        course_labels,
        index=default_idx,
        key=widget_key,
        label_visibility="collapsed"
    )

    selected_course = courses[course_labels.index(selected_label)]
    if selected_course["code"] != active_course["code"]:
        set_active_course(selected_course["code"])
        if on_change_rerun:
            st.rerun()

    return selected_course

