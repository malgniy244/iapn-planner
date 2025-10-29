import streamlit as st
import json
import pandas as pd
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Event & Travel Budget Planner",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .cost-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .cost-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    .cost-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .cost-secondary {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.3rem;
    }
    .event-card {
        background: #f8f9fa;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }
    .day-column {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        min-height: 400px;
    }
    .category-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.3rem;
    }
    .category-venue { background: #dbeafe; color: #1e40af; }
    .category-food { background: #fce7f3; color: #be185d; }
    .category-travel { background: #dcfce7; color: #166534; }
    .category-entertainment { background: #fef3c7; color: #92400e; }
    .category-accommodation { background: #e9d5ff; color: #6b21a8; }
    .category-other { background: #f3f4f6; color: #374151; }
    .save-indicator {
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .save-indicator.saved {
        background: #d1fae5;
        color: #065f46;
    }
    .save-indicator.unsaved {
        background: #fef3c7;
        color: #92400e;
    }
</style>
""", unsafe_allow_html=True)

# Categories
CATEGORIES = {
    "venue": "Venue",
    "food": "Food & Beverage",
    "travel": "Travel & Transport",
    "entertainment": "Entertainment",
    "accommodation": "Accommodation",
    "other": "Other"
}

# Data file path
DATA_FILE = "plan_data.json"

# Initialize session state with IAPN data if not exists
def init_session_state():
    if 'initialized' not in st.session_state:
        # Load IAPN 2027 data
        default_data = {
            "eventTitle": "IAPN 2027 May 21-24",
            "eventDescription": "",
            "attendees": 100,
            "currency": "HKD",
            "events": [
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
            ],
            "days": [
                {"id": "day1", "label": "Day 1", "notes": ""},
                {"id": "day2", "label": "Day 2", "notes": "Murray Conference->Star Ferry Lunch->Sai Kung Seafood Dinner"},
                {"id": "day3", "label": "Day 3", "notes": "Macau Day Trip->Lunch in Macau-> Come BackBBQ\n"},
                {"id": "day4", "label": "Day 4", "notes": "Conference->Dim Sum->Gala"}
            ],
            "schedule": {
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
            },
            "nextId": 23,
            "nextDayId": 5
        }
        
        # Try to load from file, otherwise use default
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        st.session_state[key] = value
            except:
                for key, value in default_data.items():
                    st.session_state[key] = value
        else:
            for key, value in default_data.items():
                st.session_state[key] = value
        
        st.session_state.initialized = True
        st.session_state.last_saved = datetime.now()
        st.session_state.has_unsaved = False

# Save data to file
def save_data():
    data = {
        "eventTitle": st.session_state.eventTitle,
        "eventDescription": st.session_state.eventDescription,
        "attendees": st.session_state.attendees,
        "currency": st.session_state.currency,
        "events": st.session_state.events,
        "days": st.session_state.days,
        "schedule": st.session_state.schedule,
        "nextId": st.session_state.nextId,
        "nextDayId": st.session_state.nextDayId,
        "savedAt": datetime.now().isoformat()
    }
    
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    st.session_state.last_saved = datetime.now()
    st.session_state.has_unsaved = False

# Calculate event cost
def calculate_event_cost(event, attendees):
    per_person_total = event['perPersonCost'] * attendees
    return max(per_person_total, event['minimumCost'])

# Calculate total budget
def calculate_total_budget():
    total = 0
    for day_events in st.session_state.schedule.values():
        for event in day_events:
            total += calculate_event_cost(event, st.session_state.attendees)
    return total

# Format currency
def format_currency(amount, currency):
    if currency == 'HKD':
        return f"HK${int(amount):,}"
    else:
        usd = amount / 7.8
        return f"US${usd:,.2f}"

def format_dual_currency(amount, currency):
    if currency == 'HKD':
        primary = f"HK${int(amount):,}"
        secondary = f"≈ US${(amount / 7.8):,.2f}"
    else:
        usd = amount / 7.8
        primary = f"US${usd:,.2f}"
        secondary = f"≈ HK${int(amount):,}"
    return primary, secondary

# Initialize
init_session_state()

# Auto-save on any change
if st.session_state.get('has_unsaved', False):
    save_data()

# Header
st.markdown('<div class="main-header">🎯 Event & Travel Budget Planner</div>', unsafe_allow_html=True)

# Title and description
col1, col2 = st.columns([3, 1])
with col1:
    event_title = st.text_input("Event/Trip Name", value=st.session_state.eventTitle, key="title_input")
    if event_title != st.session_state.eventTitle:
        st.session_state.eventTitle = event_title
        st.session_state.has_unsaved = True
        st.rerun()
    
    event_desc = st.text_area("Description", value=st.session_state.eventDescription, height=80, key="desc_input")
    if event_desc != st.session_state.eventDescription:
        st.session_state.eventDescription = event_desc
        st.session_state.has_unsaved = True
        st.rerun()

with col2:
    st.write("") # Spacing
    attendees = st.number_input("Attendees", min_value=1, value=st.session_state.attendees, key="attendees_input")
    if attendees != st.session_state.attendees:
        st.session_state.attendees = attendees
        st.session_state.has_unsaved = True
        st.rerun()
    
    col_hkd, col_usd = st.columns(2)
    with col_hkd:
        if st.button("HKD", use_container_width=True, type="primary" if st.session_state.currency == "HKD" else "secondary"):
            st.session_state.currency = "HKD"
            st.session_state.has_unsaved = True
            st.rerun()
    with col_usd:
        if st.button("USD", use_container_width=True, type="primary" if st.session_state.currency == "USD" else "secondary"):
            st.session_state.currency = "USD"
            st.session_state.has_unsaved = True
            st.rerun()

# Save status indicator
if st.session_state.has_unsaved:
    st.markdown('<div class="save-indicator unsaved">⚠️ Saving changes...</div>', unsafe_allow_html=True)
else:
    last_saved_str = st.session_state.last_saved.strftime("%I:%M:%S %p")
    st.markdown(f'<div class="save-indicator saved">✓ Auto-saved at {last_saved_str}</div>', unsafe_allow_html=True)

# Cost summary
total_budget = calculate_total_budget()
per_person = total_budget / st.session_state.attendees if st.session_state.attendees > 0 else 0
scheduled_count = sum(len(events) for events in st.session_state.schedule.values())

col1, col2, col3 = st.columns(3)
with col1:
    primary, secondary = format_dual_currency(total_budget, st.session_state.currency)
    st.markdown(f"""
    <div class="cost-card">
        <div class="cost-label">Total Budget</div>
        <div class="cost-value">{primary}</div>
        <div class="cost-secondary">{secondary}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    primary, secondary = format_dual_currency(per_person, st.session_state.currency)
    st.markdown(f"""
    <div class="cost-card">
        <div class="cost-label">Per Person Cost</div>
        <div class="cost-value">{primary}</div>
        <div class="cost-secondary">{secondary}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="cost-card">
        <div class="cost-label">Events Scheduled</div>
        <div class="cost-value">{scheduled_count}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main content - Sidebar and Schedule
left_col, right_col = st.columns([1, 3])

with left_col:
    st.subheader("📋 Event Library")
    
    # Add event button
    if st.button("➕ Add New Event", use_container_width=True):
        st.session_state.show_add_event = True
    
    # Display events
    for event in st.session_state.events:
        with st.container():
            st.markdown(f'<div class="event-card">', unsafe_allow_html=True)
            st.markdown(f"**{event['name']}**")
            if event.get('category'):
                st.markdown(f'<span class="category-badge category-{event["category"]}">{CATEGORIES.get(event["category"], "Other")}</span>', unsafe_allow_html=True)
            if event.get('description'):
                st.caption(event['description'])
            if event.get('duration'):
                st.caption(f"⏱️ {event['duration']}")
            
            cost_text = ""
            if event['perPersonCost'] > 0:
                cost_text += f"{format_currency(event['perPersonCost'], st.session_state.currency)}/person "
            if event['minimumCost'] > 0:
                cost_text += f"Min: {format_currency(event['minimumCost'], st.session_state.currency)}"
            if cost_text:
                st.caption(f"💰 {cost_text}")
            
            col_edit, col_del = st.columns(2)
            with col_edit:
                if st.button("✏️", key=f"edit_{event['id']}", use_container_width=True):
                    st.session_state.editing_event = event
            with col_del:
                if st.button("🗑️", key=f"del_{event['id']}", use_container_width=True):
                    st.session_state.events = [e for e in st.session_state.events if e['id'] != event['id']]
                    # Remove from schedule too
                    for day_id in st.session_state.schedule:
                        st.session_state.schedule[day_id] = [e for e in st.session_state.schedule[day_id] if e['id'] != event['id']]
                    st.session_state.has_unsaved = True
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Export buttons
    if st.button("📤 Export Schedule CSV", use_container_width=True):
        # Create CSV export
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
    
    # Display days in columns
    num_days = len(st.session_state.days)
    cols_per_row = min(4, num_days)
    
    for i in range(0, num_days, cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < num_days:
                day = st.session_state.days[i + j]
                with col:
                    st.markdown(f'<div class="day-column">', unsafe_allow_html=True)
                    
                    # Day header with edit and remove
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
                            with st.container():
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
                    else:
                        st.caption("Drop events here")
                    
                    # Add event to this day
                    if day['id'] in st.session_state.schedule:
                        available_events = [e for e in st.session_state.events 
                                          if e not in st.session_state.schedule[day['id']]]
                        if available_events:
                            event_names = ["Select event to add..."] + [e['name'] for e in available_events]
                            selected = st.selectbox(
                                "Add event",
                                event_names,
                                key=f"add_to_{day['id']}",
                                label_visibility="collapsed"
                            )
                            if selected != "Select event to add...":
                                event_to_add = next(e for e in available_events if e['name'] == selected)
                                st.session_state.schedule[day['id']].append(event_to_add)
                                st.session_state.has_unsaved = True
                                st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption(f"💾 Data automatically saved to {DATA_FILE} | Share this app URL with your team for collaboration!")
