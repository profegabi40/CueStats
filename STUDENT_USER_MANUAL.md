# 📚 CueStat Student User Manual

**Welcome to CueStat!** This guide will help you learn how to use CueStat for your statistics assignments and explorations. CueStat is designed to make statistical analysis easy and accessible for everyone.

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Understanding the Interface](#understanding-the-interface)
3. [Working with Data](#working-with-data)
4. [Descriptive Statistics](#descriptive-statistics)
5. [Probability Distributions](#probability-distributions)
6. [Creating Tables](#creating-tables)
7. [Making Plots](#making-plots)
8. [Confidence Intervals](#confidence-intervals)
9. [Hypothesis Testing](#hypothesis-testing)
10. [Interactive Simulations](#interactive-simulations)
11. [Tips & Troubleshooting](#tips--troubleshooting)
12. [Accessibility Features](#accessibility-features)

---

## 🚀 Getting Started

### What is CueStat?

CueStat is an interactive statistical analysis tool that helps you:
- Analyze data without writing code
- Create professional charts and tables
- Learn statistics through interactive simulations
- Perform hypothesis tests and confidence interval calculations

### Accessing CueStat

Your instructor will provide you with a link to access CueStat. When you open the link:
1. The app will load in your web browser
2. You'll see "CueStat: STAT C1000 Analysis Tool" at the top
3. A sidebar on the left shows different sections (tabs)
4. The main area is where you'll work with your data and see results

### First Steps

1. **Look at the sidebar** on the left side of the screen
2. **Click on "Data"** to start - this is where you'll enter or upload your data
3. Follow along with the sections below to learn each feature

---

## 🖥️ Understanding the Interface

### The Sidebar

The sidebar contains all the main sections (tabs) of CueStat:

- **📥 Data** - Enter or upload your data
- **📊 Descriptive Statistics** - Get summaries of your data (mean, median, standard deviation, etc.)
- **📈 Probability Distributions** - Calculate probabilities for various distributions
- **📋 Tables** - Create frequency tables and cross-tabulations
- **📉 Plots** - Make histograms, boxplots, and other visualizations
- **🔍 Confidence Intervals** - Calculate interval estimates
- **🧪 Hypothesis Testing** - Perform statistical tests
- **🎲 Simulations** - Explore statistical concepts interactively

### The Main Area

This is where you'll:
- Enter or view your data
- See calculation results
- View charts and tables
- Adjust settings for your analyses

---

## 📥 Working with Data

### Option 1: Upload a File

1. Click on **"Data"** in the sidebar
2. Look for the **"Upload Data"** section
3. Click **"Browse files"** or drag and drop your file
4. Supported formats:
   - **CSV files** (.csv)
   - **Excel files** (.xlsx, .xls)

**Tips:**
- Make sure your file has column headers in the first row
- Keep column names simple (no special characters)
- Each column should contain one variable

### Option 2: Manual Data Entry

If you don't have a file, you can type your data directly:

1. Click on **"Data"** in the sidebar
2. Scroll to **"Manual Data Entry"**
3. Click **"Add Column"** to create a new column
4. Type a name for your column (e.g., "Test Scores")
5. Choose the data type:
   - **Numeric** - for numbers (test scores, heights, etc.)
   - **Text** - for categories (gender, major, etc.)
6. Click **"Add rows"** to add more data entry rows
7. Type your data into the cells

**Example:**
```
Column Name: Test_Scores
Data Type: Numeric
Values: 85, 92, 78, 88, 95, 82
```

### Option 3: Auto-Loading from Google Sheets (Easiest!)

Your instructor can share data with you using a special link that automatically loads the data:

**If your instructor gives you a CueStat link with data:**
1. Click the link your instructor provided
2. The data will load automatically—no typing or uploading needed!
3. You'll see a preview of the data
4. You're ready to analyze!

**How it works:**
- Your instructor publishes their Google Sheet as CSV
- They create a special link that includes the sheet
- You click the link and the app loads the data instantly
- This is the fastest way to get started with an assignment!

**Example link:**
```
https://cuestat.streamlit.app?sheets_url=https://docs.google.com/spreadsheets/...
```

When you click this link, the data appears automatically!

### Viewing Your Data

Once you've loaded or entered data:
- You'll see a preview table showing your data
- Column names are shown at the top in bold
- You can scroll if you have lots of data

---

## 📊 Descriptive Statistics

Descriptive statistics help you summarize and understand your data.

### How to Use

1. Click **"Descriptive Statistics"** in the sidebar
2. You'll see a dropdown menu: **"Select columns to analyze"**
3. Click on the dropdown and select one or more columns
4. The results will appear immediately

### What You'll See

For each column you selected, you'll see:

**Summary Statistics:**
- **Count** - Number of data points
- **Mean** - Average value
- **Median** - Middle value
- **Mode** - Most frequent value
- **Std** - Standard deviation (how spread out the data is)
- **Variance** - Another measure of spread
- **Min** - Smallest value
- **Max** - Largest value
- **Range** - Difference between max and min
- **Q1, Q2, Q3** - Quartiles (25th, 50th, 75th percentiles)
- **IQR** - Interquartile range (Q3 - Q1)
- **Skewness** - Whether data is skewed left or right
- **Kurtosis** - How "peaked" the distribution is

**Visualizations:**
- **Histogram** - Shows the distribution of your data
- **Box Plot** - Shows median, quartiles, and outliers

### Understanding the Results

**Example:** If you're analyzing test scores:
- **Mean = 85** means the average score is 85
- **Median = 87** means half the scores are below 87
- **Std = 8.5** means most scores are within 8.5 points of the average
- **Outliers** - Any unusual values will be flagged

---

## 📈 Probability Distributions

Use this section to calculate probabilities for different statistical distributions.

### Normal Distribution

The normal distribution (bell curve) is used for many real-world data.

**What you can calculate:**
1. **Probability from Z-score** - "What's the probability of getting a z-score less than 1.5?"
2. **Z-score from Probability** - "What z-score corresponds to the 95th percentile?"
3. **Probability between two Z-scores** - "What's the probability between z = -1 and z = 1?"

**How to use:**
1. Click **"Probability Distributions"** in sidebar
2. Select **"Normal Distribution"**
3. Choose what you want to calculate
4. Enter your values
5. Click **"Calculate"**
6. See the result and a visual representation

**Example:** Finding the probability of z < 1.96:
- Select "P(Z < z)"
- Enter z = 1.96
- Result: 0.975 (97.5%)

### t-Distribution

Used when working with small samples or when population standard deviation is unknown.

**Options:**
- Calculate probabilities for specific t-values
- Find critical t-values for confidence intervals
- Requires degrees of freedom (usually n - 1)

### Chi-Square Distribution

Used for categorical data analysis and variance tests.

### F-Distribution

Used for ANOVA and comparing variances.

### Binomial Distribution

Used when counting successes in a fixed number of trials.

**Example:** Coin flips
- n = 10 (number of flips)
- p = 0.5 (probability of heads)
- x = 7 (number of heads)
- Calculate: Probability of getting exactly 7 heads

---

## 📋 Creating Tables

### Frequency Tables (One-Way)

Shows how often each value appears in your data.

**How to create:**
1. Click **"Tables"** in sidebar
2. Select **"Frequency Tables"**
3. Choose a column from your data
4. You'll see:
   - Each unique value
   - How many times it appears (Count)
   - What percentage it represents

**Example:** Survey of favorite colors
```
Color    | Count | Percent
---------|-------|--------
Blue     | 15    | 30%
Red      | 12    | 24%
Green    | 23    | 46%
```

### Two-Way Tables (Cross-Tabulation)

Shows the relationship between two categorical variables.

**How to create:**
1. Click **"Tables"** in sidebar
2. Select **"Two-Way Tables"**
3. Choose:
   - **Row variable** (e.g., Gender)
   - **Column variable** (e.g., Major)
4. Select what to display:
   - **Counts** - Raw numbers
   - **Row %** - Percentages within each row
   - **Column %** - Percentages within each column
   - **Total %** - Percentage of grand total

**Example:** Gender vs Major
```
           | Science | Arts | Business | Total
-----------|---------|------|----------|------
Male       | 45      | 20   | 35       | 100
Female     | 38      | 42   | 20       | 100
Total      | 83      | 62   | 55       | 200
```

### Contingency Tables with Chi-Square Test

Tests if two categorical variables are independent.

**How to use:**
1. Create a two-way table (as above)
2. Look for the **Chi-Square Test Results**:
   - **Chi-square statistic** - Measure of association
   - **p-value** - If less than 0.05, variables are related
   - **Degrees of freedom** - Depends on table size

---

## 📉 Making Plots

Visualizations help you see patterns in your data.

### Histograms

Shows the distribution of numerical data.

**How to create:**
1. Click **"Plots"** in sidebar
2. Select **"Histogram"**
3. Choose a numeric column
4. Adjust the number of bins (bars) if needed
5. The histogram appears below

**What to look for:**
- **Shape** - Is it bell-shaped, skewed, or uniform?
- **Center** - Where is the middle of the data?
- **Spread** - How wide is the distribution?
- **Outliers** - Any bars far from the rest?

### Box Plots

Shows median, quartiles, and outliers.

**How to create:**
1. Click **"Plots"** in sidebar
2. Select **"Box Plot"**
3. Choose a numeric column
4. The box plot appears

**Understanding the box plot:**
- **Box** - Contains middle 50% of data (Q1 to Q3)
- **Line in box** - Median
- **Whiskers** - Extend to min/max (within 1.5×IQR)
- **Dots** - Outliers beyond whiskers

### Scatter Plots

Shows relationship between two numeric variables.

**How to create:**
1. Choose "Scatter Plot"
2. Select X-axis variable
3. Select Y-axis variable
4. Look for patterns (linear, curved, no pattern)

---

## 🔍 Confidence Intervals

Confidence intervals give you a range where the true population parameter likely falls.

### One-Sample t-Interval

Estimates the population mean from your sample.

**How to calculate:**
1. Click **"Confidence Intervals"** in sidebar
2. Select **"One-Sample t-Interval"**
3. Choose:
   - **Column** with your data
   - **Confidence level** (usually 95%)
4. Click **"Calculate"**

**Results you'll see:**
- **Sample mean** - Average of your data
- **Confidence interval** - Range (e.g., 82.5 to 87.5)
- **Margin of error** - Half the width of interval
- **Interpretation** - What it means in plain language

**Example:**
```
Sample Mean: 85
95% Confidence Interval: (82.3, 87.7)
Interpretation: We are 95% confident that the true 
population mean is between 82.3 and 87.7.
```

### Two-Sample t-Interval

Estimates the difference between two population means.

**When to use:** Comparing two groups (e.g., male vs female test scores)

### Proportion Confidence Interval

For categorical data (yes/no, success/failure).

**Example:** Estimating the proportion of students who prefer online classes

---

## 🧪 Hypothesis Testing

Tests claims about populations using sample data.

### One-Sample t-Test

Tests whether a population mean equals a specific value.

**Steps:**
1. Click **"Hypothesis Testing"** in sidebar
2. Select **"One-Sample t-Test"**
3. Enter:
   - **Column** with your data
   - **Null hypothesis value** (μ₀) - the claimed value
   - **Alternative hypothesis**:
     - **Two-sided**: μ ≠ μ₀ (different from)
     - **Left-tailed**: μ < μ₀ (less than)
     - **Right-tailed**: μ > μ₀ (greater than)
   - **Significance level** (usually α = 0.05)
4. Click **"Run Test"**

**Results:**
- **t-statistic** - How many standard errors away from null value
- **p-value** - Probability of getting these results if null is true
- **Decision**:
  - If p-value < α: **Reject null hypothesis** (significant difference)
  - If p-value ≥ α: **Fail to reject null** (not enough evidence)

**Example:**
```
Question: Is the average test score different from 80?
Null: μ = 80
Alternative: μ ≠ 80
Results:
  t = 2.34
  p-value = 0.023
  Decision: Reject null (p < 0.05)
Conclusion: The average score is significantly different from 80.
```

### Two-Sample t-Test

Compares means of two independent groups.

**Example:** Do males and females have different average test scores?

**Steps:**
1. Select "Two-Sample t-Test"
2. Choose:
   - **Group 1** column
   - **Group 2** column
3. Select alternative hypothesis
4. Run test

### Paired t-Test

Compares means of paired observations (before/after, matched pairs).

**Example:** Test scores before and after tutoring for the same students

### Proportion Tests

Tests claims about population proportions (percentages).

**Example:** Is the proportion of students who pass greater than 70%?

### Chi-Square Test for Independence

Already covered in the Tables section - tests if two categorical variables are independent.

---

## 🎲 Interactive Simulations

Simulations help you understand statistical concepts by letting you experiment and see what happens.

### Central Limit Theorem

Shows how sample means form a normal distribution, even if the original data isn't normal.

**How to use:**
1. Click **"Simulations"** in sidebar
2. Select **"Central Limit Theorem"**
3. Adjust sliders:
   - **Population distribution** - Shape of original data
   - **Sample size** (n) - How many observations per sample
   - **Number of samples** - How many samples to take
4. Watch the animation:
   - **Top plot** - Original population
   - **Bottom plot** - Distribution of sample means

**What to observe:**
- As sample size increases, distribution becomes more normal
- Larger samples = less variability in sample means

### Confidence Interval Simulation

Shows what "95% confidence" really means.

**How to use:**
1. Select "Confidence Intervals Simulation"
2. Set parameters:
   - Population mean (μ)
   - Population standard deviation (σ)
   - Sample size (n)
   - Number of intervals to create
3. Click **"Run Simulation"**

**What you'll see:**
- Multiple confidence intervals plotted
- About 95% will contain the true mean (shown in different colors)
- About 5% will miss the true mean

**Key learning:** "95% confidence" means that 95% of intervals will capture the true parameter, not that there's a 95% chance for any specific interval.

### Binomial Distribution Explorer

Visualizes probabilities for binomial experiments.

**How to use:**
1. Select "Binomial Distribution"
2. Adjust:
   - **n** - Number of trials (e.g., 10 coin flips)
   - **p** - Probability of success (e.g., 0.5 for fair coin)
3. See the probability for each possible number of successes

**Example:** 10 coin flips
- See probability of 0 heads, 1 head, 2 heads, ..., 10 heads
- Most likely outcome is around 5 heads

### t vs Normal Distribution

Compares t-distribution to normal distribution.

**How to use:**
1. Select "t vs Normal"
2. Adjust **degrees of freedom** slider
3. Observe how t-distribution changes

**What to learn:**
- With few degrees of freedom, t-distribution has fatter tails
- As df increases, t-distribution approaches normal distribution
- At df ≈ 30, they're nearly identical

### F-Statistic Explorer

Shows how ANOVA works by comparing within-group and between-group variation.

**How to use:**
1. Select "F-Statistic Explorer"
2. Adjust:
   - **Between-group variance** - How different the group means are
   - **Within-group variance** - How spread out data is within each group
3. Observe the F-statistic

**What to learn:**
- Large F-value = groups are different
- Small F-value = groups are similar
- F = (Between-group variation) / (Within-group variation)

---

## 💡 Tips & Troubleshooting

### Common Issues and Solutions

**Problem:** "No data loaded"
- **Solution:** Go to the Data tab and upload a file or enter data manually

**Problem:** "Column not found"
- **Solution:** Make sure you've selected a column from the dropdown menu

**Problem:** "Not enough data"
- **Solution:** Some tests require minimum sample sizes (usually at least 3-5 data points)

**Problem:** Numbers are showing as text
- **Solution:** In manual entry, make sure you selected "Numeric" as the data type

**Problem:** Can't see my plot
- **Solution:** Scroll down - plots appear below the settings

### Best Practices

1. **Save your data file** - Keep a backup of your data on your computer
2. **Use clear column names** - "Test_Score" is better than "X1"
3. **Check your data** - Look at the preview table to make sure data uploaded correctly
4. **Start simple** - Try descriptive statistics before advanced tests
5. **Read error messages** - They often tell you exactly what's wrong
6. **Ask for help** - If stuck, ask your instructor or classmates

### Keyboard Shortcuts

- **Tab** - Move to next field
- **Shift+Tab** - Move to previous field
- **Enter** - Submit a form or run a calculation
- **Arrow keys** - Navigate through dropdown menus

---

## ♿ Accessibility Features

CueStat is designed to be accessible to everyone.

### For Keyboard Users

- **Navigate without a mouse:** Use Tab to move between elements
- **Activate buttons:** Press Enter or Space
- **Navigate dropdowns:** Use arrow keys
- **Focus indicators:** Blue outline shows where you are

### For Screen Reader Users

- **All images have descriptions:** Charts and plots include text descriptions
- **Form labels:** Every input has a clear label
- **Landmarks:** Use headings to navigate sections
- **Alt text:** All important visual content has alternative text

**Compatible with:**
- JAWS
- NVDA
- VoiceOver
- Other major screen readers

### Visual Accessibility

- **High contrast mode:** Works with your browser's high contrast settings
- **Resizable text:** Use browser zoom (Ctrl/Cmd + Plus)
- **Clear fonts:** Easy-to-read typography
- **Color-blind friendly:** Charts don't rely solely on color

### Need Help?

If you encounter any accessibility barriers:
1. Contact your instructor
2. Report issues on GitHub
3. Include details about what's not working

---

## 📝 Example Workflow

Here's a complete example of analyzing data:

### Scenario: Analyzing Test Scores

**Step 1: Load Data**
- Go to Data tab
- Upload your "test_scores.csv" file
- Verify data appears correctly

**Step 2: Descriptive Statistics**
- Go to Descriptive Statistics tab
- Select "Test_Score" column
- Note: Mean = 85, Std = 8.5, Median = 87

**Step 3: Visualize**
- Go to Plots tab
- Create a histogram
- Observation: Data is roughly bell-shaped

**Step 4: Hypothesis Test**
- Question: Is average score different from 80?
- Go to Hypothesis Testing
- Select One-Sample t-Test
- Enter μ₀ = 80
- Choose two-sided alternative
- Results: p = 0.023, reject null
- Conclusion: Average score is significantly different from 80

**Step 5: Confidence Interval**
- Go to Confidence Intervals
- Calculate 95% CI for mean
- Result: (82.3, 87.7)
- Interpretation: We're 95% confident the true average is between 82.3 and 87.7

---

## 🎓 Learning Resources

### Statistical Concepts to Review

Before using CueStat, make sure you understand:
- **Descriptive statistics:** Mean, median, standard deviation
- **Hypothesis testing:** Null/alternative hypotheses, p-values, significance levels
- **Confidence intervals:** Margin of error, confidence level
- **Distributions:** Normal, t, chi-square, binomial

### Getting More Help

- **Your textbook** - Review relevant chapters
- **Instructor** - Ask questions in class or office hours
- **Study groups** - Work through problems with classmates
- **Online resources** - Khan Academy, StatQuest, YouTube tutorials

### Practice Problems

Try these activities to build your skills:

1. **Upload practice data** and calculate descriptive statistics
2. **Create different types of plots** to visualize data
3. **Run simulations** to see how statistical concepts work
4. **Perform hypothesis tests** with different significance levels
5. **Compare results** from different statistical methods

---

## 📞 Getting Support

### When You Need Help

**For technical issues:**
- Check this manual first
- Try refreshing the page
- Check your internet connection
- Contact your instructor

**For statistics questions:**
- Review your course materials
- Attend office hours
- Use course discussion forums
- Work with study groups

**For accessibility support:**
- Contact your instructor
- Reach out to campus disability services
- Report issues for the development team to fix

---

## 🎉 Conclusion

Congratulations! You now know how to use all the main features of CueStat. Remember:

- **Practice makes perfect** - The more you use it, the easier it gets
- **Explore freely** - You can't break anything
- **Ask questions** - Your instructor is there to help
- **Have fun** - Statistics can be interesting when you see it in action!

Good luck with your statistical analyses! 📊

---

**CueStat Version:** 1.0  
**Manual Last Updated:** December 17, 2025  
**Course:** STAT C1000

For updates and additional resources, check with your instructor or visit the CueStat repository.
