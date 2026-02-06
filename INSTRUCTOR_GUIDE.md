# 👨‍🏫 CueStat Instructor Guide

Welcome! This guide explains how to use CueStat with your students, including the new **auto-loading Google Sheets feature** that makes sharing data seamless.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Auto-Loading Google Sheets (NEW!)](#auto-loading-google-sheets-new)
3. [Setting Up Your Course](#setting-up-your-course)
4. [Classroom Activities](#classroom-activities)
5. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Accessing CueStat

1. Deploy CueStat to your school's server or use a cloud platform like Streamlit Cloud
2. Get the URL of your CueStat instance (e.g., `https://cuestat.streamlit.app`)
3. Share this URL with your students
4. Students can bookmark it or access it from your course website

### Setting Permissions

- CueStat doesn't require login (students can use it immediately)
- No data is stored on the server (all work is session-based)
- Each student's session is private and independent

---

## 🔗 Auto-Loading Google Sheets (NEW!)

This is the **easiest way** to distribute data to your students. Instead of having them download files or copy URLs, students can click a link and the data loads instantly.

### Step 1: Prepare Your Google Sheet

1. Create a Google Sheet with your data (or use an existing one)
2. Make sure your data has:
   - Clear column headers in the first row
   - Numeric or text data in the columns
   - No empty rows in the middle of your data

**Example Google Sheet:**
```
Name       | Test Score | Grade
-----------|------------|-------
Alice      | 95         | A
Bob        | 87         | B
Charlie    | 92         | A
Diana      | 88         | B
```

### Step 2: Publish the Sheet as CSV

1. Open your Google Sheet in a web browser
2. Click **File** menu
3. Select **Share** → **Publish to web**
4. In the dialog that appears:
   - Choose "Entire Document" (or select a specific sheet)
   - For the export format, select **"Comma-separated values (.csv)"**
   - Click **Publish** and confirm

5. Copy the published CSV link (it will be shown in the dialog)
   - The link should look like: `https://docs.google.com/spreadsheets/d/e/2PACX-1vS...&output=csv`

### Step 3: Create the Auto-Loading Link

Create a shareable link that automatically loads your data. The format is:

```
https://[YOUR-CUESTAT-URL]?sheets_url=[CSV-LINK]
```

**Replace these:**
- `[YOUR-CUESTAT-URL]` = Your CueStat app URL (e.g., `https://cuestat.streamlit.app`)
- `[CSV-LINK]` = The Google Sheets CSV link you copied in Step 2

**Complete example:**
```
https://cuestat.streamlit.app?sheets_url=https://docs.google.com/spreadsheets/d/e/2PACX-1vS123ABC...&output=csv
```

### Step 4: Share with Students

Share the auto-loading link with your students via:
- **Email** - "Click here to load today's data"
- **Learning Management System (Canvas, Blackboard, etc.)** - Add as a clickable link
- **Course Website** - Post the link on your syllabus or assignments page
- **Discussion Forum** - Post in announcements

**Example message to students:**
```
📊 Statistical Analysis Assignment #3

Click the link below to load today's dataset:
[Auto-loading link here]

The data will load automatically when you click. 
Then complete the analysis tasks listed below:
1. Calculate descriptive statistics
2. Create a histogram
3. Perform a hypothesis test
...
```

### Step 5: Students Click and Analyze

When students click the auto-loading link:
1. CueStat opens in their browser
2. The data loads automatically
3. They see a preview of the data
4. They can immediately start analyzing!

**No downloads needed. No manual URL entry. Just click and go!**

---

## 🎓 Setting Up Your Course

### First Day of Class

1. **Create a bookmark page** with the CueStat link
2. **Send an email** to students with:
   - The CueStat app URL
   - A short description of what CueStat does
   - Instructions for their first assignment

3. **Test with a sample dataset** so students get comfortable with the interface

### Creating Assignments

For each assignment that uses CueStat:

1. **Prepare your data** in Google Sheets following the format guide above
2. **Publish it as CSV** (see steps above)
3. **Create the auto-loading link**
4. **Post the link** in your assignment instructions

**Assignment template:**
```
## Assignment: Analyzing [Dataset Name]

📊 **Dataset:** [Auto-loading link here]

The data contains information about [describe the data].

### Tasks:
1. Load the data by clicking the link above
2. Calculate the mean, median, and standard deviation of [column name]
3. Create a histogram of [column name]
4. Write a summary of your findings

### Deliverable:
Submit a screenshot or PDF with:
- The summary statistics from CueStat
- The histogram visualization
- Your written summary (100-200 words)
```

---

## 🎲 Classroom Activities

### In-Class Demonstrations

1. **Display the auto-loading link** via your projector/screen share
2. **Click it together** - Show students the data loads instantly
3. **Demonstrate the analysis** using CueStat features
4. **Discuss the results** as a class

### Interactive Exercises

1. **Divide students into groups**
2. **Give each group a different dataset** (create multiple Google Sheets)
3. **Share different auto-loading links** with each group
4. **Have groups present findings** to the class

### Take-Home Assignments

1. **Email the auto-loading link** to students
2. **Students complete analysis** on their own
3. **They submit their findings** or results as screenshots

---

## 🛠️ Troubleshooting

### Issue: Link doesn't work

**Possible causes:**
- Google Sheet is not published as CSV
- URL was mistyped or cut off
- The app URL changed

**Solution:**
1. Re-publish the Google Sheet as CSV
2. Copy the full CSV link carefully
3. Recreate the auto-loading link
4. Test the link before sharing with students

### Issue: Students click link but data doesn't load

**Possible causes:**
- The Google Sheet was deleted or unpublished
- The student's internet connection is down
- Ad blocker is interfering

**Solutions:**
1. Check that the Google Sheet is still published as CSV
2. Ask student to disable ad blockers
3. Provide an alternative link to download the CSV file
4. Have them manually paste the CSV URL in the Google Sheets tab

### Issue: Data looks different than expected

**Possible causes:**
- Column headers are incorrect
- Data formatting changed when publishing
- Special characters in data

**Solution:**
1. Check the Google Sheet - verify data is correct
2. Re-export/re-publish the sheet
3. Remove any special characters or unusual formatting
4. Test the link yourself before sharing

---

## 💡 Best Practices

### Data Preparation

✅ **Do:**
- Use clear, simple column names (no spaces or special characters)
- Keep data organized with headers in the first row
- Use consistent data types (all numeric or all text in a column)
- Include 10+ data points for meaningful analysis

❌ **Don't:**
- Include merged cells or unusual formatting
- Leave blank rows in the middle of data
- Use columns with mixed data types
- Include images or charts in the Google Sheet (won't show in CSV)

### Sharing Links

✅ **Do:**
- Test the link yourself before sharing
- Use descriptive names (e.g., "Assignment 3 Data" instead of "data")
- Include clear instructions with the link
- Keep a backup of your data

❌ **Don't:**
- Unpublish a sheet after students have the link
- Share the Google Sheet edit link (publish link only)
- Change the sheet content dramatically after sharing
- Share multiple different datasets with the same link

### Course Integration

✅ **Do:**
- Provide a syllabus link to CueStat
- Include instructions in assignments
- Offer office hours for CueStat questions
- Collect student feedback on the tool

❌ **Don't:**
- Assume students know about CueStat automatically
- Forget to test links before class
- Overload students with too many datasets at once
- Use data with sensitive information

---

## 📞 Support

### For Instructors

If you encounter issues with CueStat:

1. **Check the documentation** - See [README.md](README.md) for technical details
2. **Test with sample data** - Start simple, then make it more complex
3. **Review the Accessibility documentation** - See [ADA_COMPLIANCE_REVIEW_FINAL.md](ADA_COMPLIANCE_REVIEW_FINAL.md)

### For Students

Provide students with:
- This guide's student section (or the [STUDENT_USER_MANUAL.md](STUDENT_USER_MANUAL.md))
- Your email for questions
- Office hours for in-person help
- Link to CueStat documentation

---

## 🔄 Advanced Tips

### Creating Multiple Dataset Versions

For different course sections or years:
1. Create separate Google Sheets for each section
2. Prepare each sheet and get the CSV link
3. Create different auto-loading links for each
4. Email or post the appropriate link to each section

### Updating Data Between Assignments

1. Edit the original Google Sheet
2. **Don't** republish it - the URL stays the same
3. Update the published content automatically updates with the same link
4. Students using old links will see updated data

### Combining with Other Tools

CueStat auto-loading links work well with:
- **LMS systems** (Canvas, Blackboard) - Embed as a link in assignments
- **Google Classroom** - Post the link in assignments
- **Course websites** - Link from your syllabus or schedule
- **Email** - Send links in announcements or assignment instructions

---

**Version:** 1.0  
**Last Updated:** February 2026  
**Created for:** CueStat Educational Statistics Tool
