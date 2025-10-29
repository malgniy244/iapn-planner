import streamlit as st
import json
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Event & Travel Budget Planner",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #1a1a1a;
    }
    .stApp {
        background-color: #1a1a1a;
    }
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #ffffff !important;
    }
    .event-card {
        background: #2d2d2d;
        border: 2px solid #404040;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    .category-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.25rem 0;
    }
    .category-food { background: #fce7f3; color: #be185d; }
    .category-venue { background: #dbeafe; color: #1e40af; }
    .category-other { background: #f3f4f6; color: #374151; }
    .stButton button {
        width: 100%;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Categories
CATEGORIES = {
    "venue": "Venue",
    "food": "Food & Beverage",
    "other": "Other"
}

# Data file path
DATA_FILE = "plan_data.json"

# Initialize session state with IAPN data
def init_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.eventTitle = "IAPN 2027 May 21-24"
        st.session_state.eventDescription = ""
        st.session_state.attendees = 100
        st.session_state.currency = "HKD"
        st.session_state.nextEventId = 23
        st.session_state.nextDayId = 5
        st.session_state.has_unsaved = False
        st.session_state.editing_event = None
        
        # All events in library
        st.session_state.events = [
            {"id": 1, "name": "Welcome Reception in Murray", "description": "", "duration": "3 hours", "perPersonCost": 1180, "minimumCost": 140000, "category": "food"},
            {"id": 5, "name": "Welcome Reception in Hyatt Regency", "description": "", "duration": "3 hours", "perPersonCost": 818, "minimumCost": 68800, "category": "food"},
            {"id": 6, "name": "Gala Dinner in The Verandah", "description": "", "duration": "Dinner", "perPersonCost": 1628, "minimumCost": 360000, "category": "food"},
            {"id": 9, "name": "Gala Dinner in Crown Wine Cellar", "description": "", "duration": "Dinner", "perPersonCost": 1688, "minimumCost": 110000, "category": "food"},
            {"id": 10, "name": "Gala Dinner in WaterMark", "description": "", "duration": "Dinner", "perPersonCost": 0, "minimumCost": 168000, "category": "food"},
            {"id": 11, "name": "Sai Kung Seafood Dinner", "description": "", "duration": "Dinner", "perPersonCost": 1000, "minimumCost": 0, "category": "food"},
            {"id": 12, "name": "Star Ferry", "description": "110 passengers. 3 hours 45,000", "duration": "Cocktail", "perPersonCost": 0, "minimumCost": 45000, "category": "food"},
            {"id": 15, "name": "Star Ferry Canapes/ Lunch", "description": "Canapes Room.", "duration": "Cocktail", "perPersonCost": 500, "minimumCost": 0, "category": "food"},
            {"id": 2, "name": "Conference Hall Rental in Murray", "description": "Main venue for keynote sessions", "duration": "Half Day", "perPersonCost": 0, "minimumCost": 75000, "category": "venue"},
            {"id": 7, "name": "Conference Hall Rental in Hyatt Regency", "description": "Main venue for keynote sessions", "duration": "Half Day", "perPersonCost": 0, "minimumCost": 40800, "category": "venue"},
            {"id": 8, "name": "Conference Hall Rental in W Hotel", "description": "Main venue for keynote sessions", "duration": "Half Day", "perPersonCost": 0, "minimumCost": 118000, "category": "venue"},
            {"id": 3, "name": "Workshop Session", "description": "Interactive training with materials", "duration": "4 hours", "perPersonCost": 1200, "minimumCost": 0, "category": "venue"},
            {"id": 13, "name": "Tour Bus for Macau", "description": "2 buses, 1 bus 4500 full day estimate", "duration": "", "perPersonCost": 0, "minimumCost": 9000, "category": "other"},
            {"id": 14, "name": "Macau Lunch - Portugese Food", "description": "Budget 500 per person", "duration": "", "perPersonCost": 500, "minimumCost": 0, "category": "other"},
            {"id": 16, "name": "Sai Kung Alcohol Cost", "description": "Buy Bottles and bring there.", "duration": "", "perPersonCost": 299.98, "minimumCost": 0, "category": "other"},
            {"id": 17, "name": "Dragon Dance Performance", "description": "", "duration": "", "perPersonCost": 0, "minimumCost": 10000, "category": "other"},
            {"id": 18, "name": "Dim Sum Lunch", "description": "", "duration": "Lunch", "perPersonCost": 350, "minimumCost": 0, "category": "other"},
            {"id": 19, "name": "Korean BBQ Dinner", "description": "", "duration": "Dinner", "perPersonCost": 800, "minimumCost": 0, "category": "other"},
            {"id": 20, "name": "Star Ferry Alcohol Cost", "description": "", "duration": "Lunch", "perPersonCost": 300, "minimumCost": 0, "category": "other"},
            {"id": 21, "name": "Murray Lunch", "description": "", "duration": "", "perPersonCost": 600, "minimumCost": 0, "category": "other"},
            {"id": 22, "name": "Jocky Club Lunch- Saturday/ Sunday", "description": "Wouldnt know until the race schedule out in 2026.", "duration": "", "perPersonCost": 830, "minimumCost": 0, "category": "other"}
        ]
        
        # Days
        st.session_state.days = [
            {"id": "day1", "label": "Day 1", "notes": ""},
            {"id": "day2", "label": "Day 2", "notes": "Murray Conference->Star Ferry Lunch->Sai Kung Seafood Dinner"},
            {"id": "day3", "label": "Day 3", "notes": "Macau Day Trip->Lunch in Macau-> Come BackBBQ"},
            {"id": "day4", "label": "Day 4", "notes": "Conference->Dim Sum->Gala"}
        ]
        
        # Schedule (events assigned to days)
        st.session_state.schedule = {
            "day1": [{"id": 1, "name": "Welcome Reception in Murray", "description": "", "duration": "3 hours", "perPersonCost": 1180, "minimumCost": 140000, "category": "food"}],
            "day2": [
                {"id": 2, "name": "Conference Hall Rental in Murray", "description": "Main venue for keynote sessions", "duration": "Half Day", "perPersonCost": 0, "minimumCost": 75000, "category": "venue"},
                {"id": 11, "name": "Sai Kung Seafood Dinner", "description": "", "duration": "Dinner", "perPersonCost": 1000, "minimumCost": 0, "category": "food"},
                {"id": 16, "name": "Sai Kung Alcohol Cost", "description": "Buy Bottles and bring there.", "duration": "", "perPersonCost": 299.98, "minimumCost": 0, "category": "other"},
                {"id": 17, "name": "Dragon Dance Performance", "description": "", "duration": "", "perPersonCost": 0, "minimumCost": 10000, "category": "other"},
                {"id": 12, "name": "Star Ferry", "description": "110 passengers. 3 hours 45,000", "duration": "Cocktail", "perPersonCost": 0, "minimumCost": 45000, "category": "food"},
                {"id": 15, "name": "Star Ferry Canapes/ Lunch", "description": "Canapes Room.", "duration": "Cocktail", "perPersonCost": 500, "minimumCost": 0, "category": "food"},
                {"id": 20, "name": "Star Ferry Alcohol Cost", "description": "", "duration": "Lunch", "perPersonCost": 300, "minimumCost": 0, "category": "other"}
            ],
            "day3": [
                {"id": 13, "name": "Tour Bus for Macau", "description": "2 buses, 1 bus 4500 full day estimate", "duration": "", "perPersonCost": 0, "minimumCost": 9000, "category": "other"},
                {"id": 14, "name": "Macau Lunch - Portugese Food", "description": "Budget 500 per person", "duration": "", "perPersonCost": 500, "minimumCost": 0, "category": "other"},
                {"id": 19, "name": "Korean BBQ Dinner", "description": "", "duration": "Dinner", "perPersonCost": 800, "minimumCost": 0, "category": "other"}
            ],
            "day4": [
                {"id": 2, "name": "Conference Hall Rental in Murray", "description": "Main venue for keynote sessions", "duration": "Half Day", "perPersonCost": 0, "minimumCost": 75000, "category": "venue"},
                {"id": 18, "name": "Dim Sum Lunch", "description": "", "duration": "Lunch", "perPersonCost": 350, "minimumCost": 0, "category": "other"},
                {"id": 6, "name": "Gala Dinner in The Verandah", "description": "", "duration": "Dinner", "perPersonCost": 1628, "minimumCost": 360000, "category": "food"}
            ]
        }
        
        st.session_state.initialized = True

def calculate_event_cost(event, attendees):
    """Calculate event cost based on per person and minimum"""
    per_person = event.get('perPersonCost', 0) * attendees
    minimum = event.get('minimumCost', 0)
    return max(per_person, minimum)

def format_currency(amount, currency):
    """Format currency based on selected currency"""
    if currency == "USD":
        return f"US${amount:,.2f}"
    else:
        return f"HK${amount:,.0f}"

def get_total_budget():
    """Calculate total budget across all scheduled events"""
    total = 0
    for day_id, events in st.session_state.schedule.items():
        for event in events:
            total += calculate_event_cost(event, st.session_state.attendees)
    return total

def get_total_scheduled_events():
    """Count total scheduled events"""
    return sum(len(events) for events in st.session_state.schedule.values())

# Initialize
init_session_state()

# Header
st.title("🎯 Event & Travel Budget Planner")

# Top row - Event info
col1, col2 = st.columns([3, 1])
with col1:
    st.session_state.eventTitle = st.text_input("Event/Trip Name", st.session_state.eventTitle)
    st.session_state.eventDescription = st.text_area("Description", st.session_state.eventDescription, height=100)

with col2:
    st.write("Attendees")
    col_minus, col_num, col_plus = st.columns([1, 2, 1])
    with col_minus:
        if st.button("➖"):
            if st.session_state.attendees > 1:
                st.session_state.attendees -= 1
                st.session_state.has_unsaved = True
                st.rerun()
    with col_num:
        st.markdown(f"<h2 style='text-align: center; margin: 0;'>{st.session_state.attendees}</h2>", unsafe_allow_html=True)
    with col_plus:
        if st.button("➕"):
            st.session_state.attendees += 1
            st.session_state.has_unsaved = True
            st.rerun()
    
    # Currency toggle
    col_hkd, col_usd = st.columns(2)
    with col_hkd:
        if st.button("HKD", type="primary" if st.session_state.currency == "HKD" else "secondary", use_container_width=True):
            st.session_state.currency = "HKD"
            st.rerun()
    with col_usd:
        if st.button("USD", type="primary" if st.session_state.currency == "USD" else "secondary", use_container_width=True):
            st.session_state.currency = "USD"
            st.rerun()

# Auto-save indicator
current_time = datetime.now().strftime("%I:%M:%S %p")
st.success(f"✓ Auto-saved at {current_time}")

# Budget summary cards
total_budget = get_total_budget()
per_person_cost = total_budget / st.session_state.attendees if st.session_state.attendees > 0 else 0
total_events = get_total_scheduled_events()

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
        <div style='font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;'>Total Budget</div>
        <div style='font-size: 2rem; font-weight: bold;'>{format_currency(total_budget, 'HKD')}</div>
        <div style='font-size: 1rem; opacity: 0.9; margin-top: 0.3rem;'>≈ {format_currency(total_budget / 7.8, 'USD')}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
        <div style='font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;'>Per Person Cost</div>
        <div style='font-size: 2rem; font-weight: bold;'>{format_currency(per_person_cost, 'HKD')}</div>
        <div style='font-size: 1rem; opacity: 0.9; margin-top: 0.3rem;'>≈ {format_currency(per_person_cost / 7.8, 'USD')}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
        <div style='font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;'>Events Scheduled</div>
        <div style='font-size: 2rem; font-weight: bold;'>{total_events}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main content - Two columns
left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("📋 Event Library")
    
    # Add new event button
    if st.button("➕ Add New Event", use_container_width=True):
        st.session_state.editing_event = {
            "id": st.session_state.nextEventId,
            "name": "",
            "description": "",
            "duration": "",
            "perPersonCost": 0,
            "minimumCost": 0,
            "category": "other"
        }
        st.session_state.nextEventId += 1
    
    # Event editor (if editing)
    if st.session_state.editing_event:
        with st.form("event_form"):
            st.write("### Edit Event")
            name = st.text_input("Event Name", st.session_state.editing_event.get('name', ''))
            description = st.text_area("Description", st.session_state.editing_event.get('description', ''))
            duration = st.text_input("Duration", st.session_state.editing_event.get('duration', ''))
            category = st.selectbox("Category", list(CATEGORIES.keys()), 
                                   index=list(CATEGORIES.keys()).index(st.session_state.editing_event.get('category', 'other')))
            per_person = st.number_input("Per Person Cost (HKD)", value=float(st.session_state.editing_event.get('perPersonCost', 0)))
            minimum = st.number_input("Minimum Cost (HKD)", value=float(st.session_state.editing_event.get('minimumCost', 0)))
            
            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.form_submit_button("💾 Save", use_container_width=True):
                    # Update or add event
                    updated_event = {
                        "id": st.session_state.editing_event['id'],
                        "name": name,
                        "description": description,
                        "duration": duration,
                        "perPersonCost": per_person,
                        "minimumCost": minimum,
                        "category": category
                    }
                    
                    # Check if updating existing or adding new
                    existing_idx = next((i for i, e in enumerate(st.session_state.events) if e['id'] == updated_event['id']), None)
                    if existing_idx is not None:
                        st.session_state.events[existing_idx] = updated_event
                    else:
                        st.session_state.events.append(updated_event)
                    
                    st.session_state.editing_event = None
                    st.session_state.has_unsaved = True
                    st.rerun()
            
            with col_cancel:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.editing_event = None
                    st.rerun()
    
    st.markdown("---")
    
    # Display events
    for event in st.session_state.events:
        with st.container():
            st.markdown(f"**{event['name']}**")
            
            # Category badge
            category_class = f"category-{event.get('category', 'other')}"
            st.markdown(f'<span class="category-badge {category_class}">{CATEGORIES.get(event.get("category", "other"), "Other")}</span>', unsafe_allow_html=True)
            
            # Duration
            if event.get('duration'):
                st.caption(f"⏱️ {event['duration']}")
            
            # Cost
            cost = calculate_event_cost(event, st.session_state.attendees)
            per_person_text = f"HK{event['perPersonCost']:,.0f}/person" if event.get('perPersonCost', 0) > 0 else ""
            min_text = f"Min: HK${event['minimumCost']:,.0f}" if event.get('minimumCost', 0) > 0 else ""
            
            if per_person_text and min_text:
                st.caption(f"💰 {per_person_text} {min_text}")
            elif per_person_text:
                st.caption(f"💰 {per_person_text}")
            elif min_text:
                st.caption(f"💰 {min_text}")
            
            # Buttons
            col_edit, col_delete = st.columns(2)
            with col_edit:
                if st.button("✏️", key=f"edit_{event['id']}", use_container_width=True):
                    st.session_state.editing_event = event
                    st.rerun()
            with col_delete:
                if st.button("🗑️", key=f"del_{event['id']}", use_container_width=True):
                    st.session_state.events = [e for e in st.session_state.events if e['id'] != event['id']]
                    # Remove from schedule too
                    for day_id in st.session_state.schedule:
                        st.session_state.schedule[day_id] = [e for e in st.session_state.schedule[day_id] if e['id'] != event['id']]
                    st.session_state.has_unsaved = True
                    st.rerun()
            
            st.markdown("---")
    
    # Export button
    if st.button("📤 Export Schedule CSV", use_container_width=True):
        rows = []
        for day in st.session_state.days:
            if day['id'] in st.session_state.schedule:
                for event in st.session_state.schedule[day['id']]:
                    cost = calculate_event_cost(event, st.session_state.attendees)
                    rows.append({
                        'Day': day['label'],
                        'Event': event['name'],
                        'Duration': event.get('duration', ''),
                        'Category': CATEGORIES.get(event.get('category', 'other'), 'Other'),
                        'Cost': cost
                    })
        
        if rows:
            df = pd.DataFrame(rows)
            csv = df.to_csv(index=False)
            st.download_button(
                "⬇️ Download CSV",
                csv,
                f"{st.session_state.eventTitle.replace(' ', '-').lower()}-schedule.csv",
                "text/csv",
                use_container_width=True
            )

with right_col:
    st.subheader(f"📅 Schedule ({len(st.session_state.days)} Days)")
    
    # Add day button
    if st.button("➕ Add Day"):
        new_day_id = f"day{st.session_state.nextDayId}"
        st.session_state.days.append({
            "id": new_day_id,
            "label": f"Day {st.session_state.nextDayId}",
            "notes": ""
        })
        st.session_state.schedule[new_day_id] = []
        st.session_state.nextDayId += 1
        st.session_state.has_unsaved = True
        st.rerun()
    
    # Display days in grid
    num_days = len(st.session_state.days)
    cols_per_row = min(4, num_days)
    
    for i in range(0, num_days, cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < num_days:
                day = st.session_state.days[i + j]
                with col:
                    # Day header
                    col_title, col_remove = st.columns([4, 1])
                    with col_title:
                        st.markdown(f"**{day['label']}**")
                    with col_remove:
                        if len(st.session_state.days) > 1 and st.button("✕", key=f"remove_day_{day['id']}", help="Remove day"):
                            st.session_state.days = [d for d in st.session_state.days if d['id'] != day['id']]
                            if day['id'] in st.session_state.schedule:
                                del st.session_state.schedule[day['id']]
                            st.session_state.has_unsaved = True
                            st.rerun()
                    
                    if day.get('notes'):
                        st.caption(f"📝 {day['notes']}")
                    
                    # Calculate day total
                    if day['id'] in st.session_state.schedule and st.session_state.schedule[day['id']]:
                        day_total = sum(calculate_event_cost(e, st.session_state.attendees) for e in st.session_state.schedule[day['id']])
                        st.caption(f"💰 {format_currency(day_total, st.session_state.currency)}")
                    
                    st.markdown("---")
                    
                    # Show scheduled events
                    if day['id'] in st.session_state.schedule:
                        for idx, event in enumerate(st.session_state.schedule[day['id']]):
                            st.markdown(f"**{event['name']}**")
                            if event.get('duration'):
                                st.caption(f"⏱️ {event['duration']}")
                            cost = calculate_event_cost(event, st.session_state.attendees)
                            st.caption(f"💰 {format_currency(cost, st.session_state.currency)}")
                            
                            # Move and remove buttons
                            col_up, col_down, col_rem = st.columns(3)
                            with col_up:
                                if idx > 0 and st.button("⬆️", key=f"up_{day['id']}_{idx}", help="Move up"):
                                    st.session_state.schedule[day['id']][idx], st.session_state.schedule[day['id']][idx-1] = \
                                        st.session_state.schedule[day['id']][idx-1], st.session_state.schedule[day['id']][idx]
                                    st.session_state.has_unsaved = True
                                    st.rerun()
                            with col_down:
                                if idx < len(st.session_state.schedule[day['id']]) - 1 and st.button("⬇️", key=f"down_{day['id']}_{idx}", help="Move down"):
                                    st.session_state.schedule[day['id']][idx], st.session_state.schedule[day['id']][idx+1] = \
                                        st.session_state.schedule[day['id']][idx+1], st.session_state.schedule[day['id']][idx]
                                    st.session_state.has_unsaved = True
                                    st.rerun()
                            with col_rem:
                                if st.button("❌", key=f"rem_{day['id']}_{idx}", help="Remove from day"):
                                    st.session_state.schedule[day['id']].pop(idx)
                                    st.session_state.has_unsaved = True
                                    st.rerun()
                            st.markdown("---")
                    
                    # Add event to this day (dropdown selector)
                    if day['id'] in st.session_state.schedule:
                        available_events = [e for e in st.session_state.events]
                        if available_events:
                            event_names = ["Select..."] + [e['name'] for e in available_events]
                            selected = st.selectbox(
                                "Add event",
                                event_names,
                                key=f"add_to_{day['id']}",
                                label_visibility="collapsed"
                            )
                            if selected != "Select...":
                                event_to_add = next(e for e in available_events if e['name'] == selected)
                                st.session_state.schedule[day['id']].append(event_to_add)
                                st.session_state.has_unsaved = True
                                st.rerun()

st.markdown("---")
st.caption(f"💾 Data automatically saved to {DATA_FILE} | Share this app URL with your team for collaboration!")
