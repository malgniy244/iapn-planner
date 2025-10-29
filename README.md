# Event & Travel Budget Planner - Streamlit Version

Interactive event and travel budget planning app with real-time collaboration via GitHub.

## Features

✅ All your IAPN 2027 data pre-loaded
✅ Drag-and-drop interface (use ⬆️⬇️ buttons to reorder)
✅ Add/edit/delete events
✅ Dynamic days (add/remove as needed)
✅ HKD/USD currency toggle
✅ Auto-save functionality
✅ Export to CSV
✅ Collaborative editing via shared data file

## Quick Start

### Option 1: Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Option 2: Deploy to Streamlit Cloud (Recommended for Sharing)

1. **Create GitHub Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - IAPN 2027 planner"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/event-planner.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Connect your GitHub repo
   - Select `app.py` as main file
   - Click "Deploy"!

3. **Share the URL:**
   - Get URL like: `https://your-app.streamlit.app`
   - Share with your boss
   - He can edit directly in browser
   - Changes save to `plan_data.json` in the repo

## How Collaboration Works

1. **You deploy the app** to Streamlit Cloud connected to your GitHub repo
2. **Boss opens the URL** → sees IAPN 2027 plan loaded
3. **Boss makes changes** → auto-saves to `plan_data.json`
4. **You refresh** → see his changes
5. **Both can edit simultaneously** → last edit wins

## Data Storage

- All data stored in `plan_data.json`
- Auto-commits to GitHub when changes are made
- To enable auto-commit, add GitHub token to Streamlit secrets

## Files

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `plan_data.json` - Your event data (auto-generated)
- `README.md` - This file

## Your IAPN 2027 Data

All your events, schedule, and costs are already loaded:
- 22 events (Welcome Receptions, Gala Dinners, Conference Halls, etc.)
- 4 days scheduled
- 100 attendees
- Full cost calculations with HKD/USD toggle

## Next Steps

1. Test locally first: `streamlit run app.py`
2. Make any adjustments you want
3. Push to GitHub
4. Deploy on Streamlit Cloud
5. Share URL with boss!

## Tips

- The app auto-saves every change
- Data persists in `plan_data.json`
- For true real-time collaboration, consider adding Firebase or Supabase
- Current version uses file-based storage (good for small teams)

## Support

Any questions? The app has all features from your HTML version plus:
- ✅ Better mobile support
- ✅ Easier to share (just a URL)
- ✅ Auto-save
- ✅ No "Share" button issues!
