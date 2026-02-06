# 🧪 Auto-Loading Feature - Testing Guide

## Quick Test Resources

### Sample Google Sheets for Testing

Here's how to create a simple test sheet to verify the auto-loading feature works:

#### Option A: Create Your Own Test Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new sheet with this data:

```
Name,Score,Grade
Alice,95,A
Bob,87,B
Charlie,92,A
Diana,88,B
Eve,79,C
```

3. Publish as CSV:
   - File → Share → Publish to web
   - Format: Comma-separated values (.csv)
   - Click Publish
   - Copy the link

4. Create auto-loading link:
   ```
   https://localhost:8501?sheets_url=[PASTE-YOUR-CSV-LINK]
   ```
   (For local testing)

5. Test it locally:
   - Run: `streamlit run streamlit_app.py`
   - Paste the link in your browser
   - Verify data loads automatically

---

## Testing Checklist

### ✅ Manual Testing Steps

- [ ] **Test 1: Local Environment**
  - [ ] Run `streamlit run streamlit_app.py`
  - [ ] Create test Google Sheet
  - [ ] Publish as CSV
  - [ ] Create auto-loading link with localhost URL
  - [ ] Click link
  - [ ] Verify data appears

- [ ] **Test 2: Streamlit Cloud**
  - [ ] Deploy app to Streamlit Cloud
  - [ ] Get the app URL
  - [ ] Create auto-loading link with Cloud URL
  - [ ] Click link from different device/browser
  - [ ] Verify it works

- [ ] **Test 3: Different URL Formats**
  - [ ] Test with `/export?format=csv` URL (modern format)
  - [ ] Test with `/pub?output=csv` URL (older format)
  - [ ] Test with regular share link (should auto-convert)

- [ ] **Test 4: Error Handling**
  - [ ] Test with empty sheet (should show error)
  - [ ] Test with invalid URL (should show error)
  - [ ] Test with deleted sheet (should show error)
  - [ ] Verify error messages are helpful

- [ ] **Test 5: Data Integrity**
  - [ ] Load data via auto-loading
  - [ ] Verify row count matches original
  - [ ] Verify column count matches original
  - [ ] Verify data values are correct
  - [ ] Verify column headers are correct

- [ ] **Test 6: Accessibility**
  - [ ] Tab through with keyboard
  - [ ] Test with screen reader (NVDA/JAWS if available)
  - [ ] Verify link text is descriptive
  - [ ] Check contrast of status messages

- [ ] **Test 7: LMS Integration**
  - [ ] Create link
  - [ ] Paste into Canvas assignment
  - [ ] Paste into Blackboard course
  - [ ] Paste into Google Classroom
  - [ ] Click and verify it opens correctly

---

## Common Issues & Solutions

### Issue: "Cannot parse Google Sheets URL"

**Cause:** URL format is incorrect or link is malformed

**Solution:**
1. Copy the CSV export link directly from Google Sheets publish dialog
2. Verify it ends with `/export?format=csv` or `/pub?output=csv`
3. Check for any extra spaces or characters

**Test:**
```
Correct: https://docs.google.com/spreadsheets/d/e/2PACX-1vS.../export?format=csv
Wrong:   https://docs.google.com/spreadsheets/d/e/2PACX-1vS... (missing /export?format=csv)
```

### Issue: "The Google Sheet appears to be empty"

**Cause:** The published sheet has no data or wasn't saved

**Solution:**
1. Go back to your Google Sheet
2. Verify data is there and properly formatted
3. Make sure first row has column headers
4. Re-publish the sheet as CSV
5. Use the new link

### Issue: Data doesn't update when I edit the sheet

**Expected Behavior:** This is normal!
- Once you publish a sheet, it creates a "snapshot" export
- Editing the original sheet doesn't change the published CSV
- If you need updated data, you must edit and re-publish the sheet

**Workaround:** 
- For frequently updated data, publish to a new link and share the new URL
- Or have students reload the page to get the latest cached version

### Issue: Browser shows "page not found" when clicking auto-loading link

**Cause:** Your CueStat app URL might be wrong in the link

**Solution:**
1. Verify your CueStat app is running and accessible
2. Double-check the URL format (http vs https, correct domain)
3. Make sure there are no typos in the URL
4. Test the base CueStat URL first (without `?sheets_url=...` parameter)

---

## Performance Expectations

### Load Times

- **Sheet loads automatically**: 1-3 seconds
- **Data preview appears**: 2-5 seconds
- **Ready for analysis**: 5-10 seconds total

*Times may vary depending on internet speed and sheet size*

### Sheet Size Limits

- ✅ **Recommended**: Up to 10,000 rows × 20 columns
- ⚠️ **Acceptable**: Up to 50,000 rows × 50 columns
- ❌ **Too large**: Millions of rows (use database instead)

---

## Browser Compatibility

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome | ✅ Excellent | Fully supported |
| Firefox | ✅ Excellent | Fully supported |
| Safari | ✅ Good | Fully supported |
| Edge | ✅ Excellent | Fully supported |
| IE 11 | ❌ Not supported | Use modern browser |
| Mobile Safari | ✅ Good | Touch-friendly |
| Mobile Chrome | ✅ Good | Touch-friendly |

---

## Verification Checklist for Deployment

Before deploying to production, verify:

- [ ] Code has no syntax errors
- [ ] All imports are available
- [ ] Feature works in local environment
- [ ] Feature works in staging/cloud environment
- [ ] Links are shareable and work from external devices
- [ ] Error messages are user-friendly
- [ ] Accessibility is maintained
- [ ] Documentation is up to date
- [ ] Students and instructors understand how to use it
- [ ] Support staff knows how to troubleshoot it

---

## Getting Help

If tests fail:

1. **Check the error message** - It often tells you what's wrong
2. **Review INSTRUCTOR_GUIDE.md** - Step-by-step troubleshooting
3. **Verify Google Sheet settings** - Make sure it's published as CSV
4. **Test the CSV link directly** - Copy the link and open in browser
5. **Check the browser console** - Press F12, see if there are errors

---

**Good luck with testing!** 🎓

If you encounter any issues, refer to the troubleshooting sections in [INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md).
