# SweetSwap AI - MVP Testing Guide

## Quick Start Checklist

### ✅ Step 1: Load Seed Data
```powershell
# From project root with venv activated
python -m backend.app.seed_data
```

You should see:
```
✅ Successfully loaded 30 substitutions into database!
   Original drinks: 60
   Substitutions: 30
```

Verify in Supabase: Check the `drinks` and `substitutions` tables have data.

---

### ✅ Step 2: Start Backend API
```powershell
# From project root with venv activated
uvicorn app.main:app --reload --app-dir backend
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Test the API:**
1. Open browser: http://localhost:8000/docs (FastAPI auto-generated docs)
2. Or test with curl:
   ```powershell
   curl http://localhost:8000/health
   # Should return: {"status":"ok"}
   
   curl -X POST http://localhost:8000/substitute -H "Content-Type: application/json" -d "{\"drink_name\": \"Mango Boba Tea\"}"
   ```

---

### ✅ Step 3: Test Database Lookup (Seeded Data)
Try these drinks that are in your seed data:
- `Mango Boba Tea`
- `Starbucks Caramel Frappuccino`
- `Matcha Latte`
- `Thai Iced Tea`

**Expected behavior:**
- Fast response (from database)
- `source: "manual"` in response
- Sugar/caffeine deltas should be populated

---

### ✅ Step 4: Test LLM Fallback (New Drinks)
Try a drink NOT in your seed data:
- `Blueberry Smoothie`
- `Pineapple Coconut Drink`
- `Espresso Shot`

**Expected behavior:**
- Slower response (Gemini API call)
- `source: "llm"` in response
- New substitution saved to database
- Check Supabase - you should see new rows in `drinks` and `substitutions` tables

**Troubleshooting Gemini:**
- If you get fallback responses, check:
  1. `GEMINI_API_KEY` is set in `.env`
  2. API key is valid
  3. Check console for error messages

---

### ✅ Step 5: Test Nutrition API Integration
1. Make sure `NUTRITION_API_KEY` (USDA) is in `.env`
2. Try a drink with `include_nutrition: true`
3. Check backend logs - you should see USDA API calls

**Note:** USDA API might not have all drinks. That's okay - the system will still work with estimated values.

---

### ✅ Step 6: Start Streamlit Frontend
```powershell
# In a NEW terminal (keep backend running)
# From project root with venv activated
streamlit run frontend/app.py
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

**Test the UI:**
1. Enter "Mango Boba Tea" → Should show instant result from DB
2. Enter a new drink → Should show Gemini-generated substitution
3. Check the nutrition comparison cards
4. Try the example buttons in sidebar

---

## End-to-End Test Flow

### Test Case 1: Database Hit
1. Frontend: Enter "Starbucks Caramel Frappuccino"
2. **Expected:** Fast response, shows "Mango Green Tea w/ Stevia" (or similar from seed)
3. **Verify:** Response has `source: "manual"`

### Test Case 2: LLM Fallback
1. Frontend: Enter "Watermelon Slushie" (not in seed)
2. **Expected:** Slower response, shows AI-generated substitute
3. **Verify:** 
   - Response has `source: "llm"`
   - Check Supabase - new drink and substitution rows created
   - Try same drink again → should now be instant (cached in DB)

### Test Case 3: Nutrition Comparison
1. Enter any drink with nutrition data
2. **Expected:** Sugar reduction and caffeine change cards display
3. **Verify:** Numbers make sense (negative sugar delta = good!)

---

## Common Issues & Fixes

### ❌ "Could not connect to backend API"
- **Fix:** Make sure `uvicorn` is running on port 8000
- Check: `http://localhost:8000/health` works in browser

### ❌ "ImportError" or module not found
- **Fix:** Make sure venv is activated: `.\.venv\Scripts\activate`
- Reinstall: `pip install -r backend\requirements.txt`

### ❌ Gemini returns fallback responses
- **Fix:** Check `.env` has `GEMINI_API_KEY=your_key_here`
- Test API key: Try calling Gemini directly in Python console

### ❌ Database connection errors
- **Fix:** Verify Supabase connection string in `.env`
- Test: Run `python -m backend.app.db_init` again

### ❌ No data in Supabase after seed
- **Fix:** Check `seed_data.py` ran without errors
- Manually check: Supabase Table Editor → `drinks` table should have rows

---

## Next Steps After MVP Testing

1. **Expand seed data:** Add more drinks to `data/seed_substitutions.csv`
2. **Improve Gemini prompts:** Tweak `backend/app/services/llm.py` for better responses
3. **Add feedback system:** Store 👍/👎 in database
4. **Build scraper:** Start with one cafe menu in `scrapers/`
5. **Add Redis caching:** Cache frequent lookups for even faster responses

---

## API Endpoints Reference

- `GET /health` - Health check
- `POST /substitute` - Get substitution
  ```json
  {
    "drink_name": "Mango Boba Tea",
    "include_nutrition": true
  }
  ```
- `GET /substitute/{id}` - Get substitution by ID

---

## Success Criteria ✅

Your MVP is working when:
- ✅ Seeded drinks return instant results
- ✅ New drinks trigger Gemini and get saved
- ✅ Frontend displays substitutions with nutrition comparison
- ✅ All data persists in Supabase
- ✅ You can demo "Mango Boba Tea → substitute" end-to-end

**You're ready to put this on your resume!** 🎉

