# 📊 CueStat - Interactive Statistical Analysis Tool

**CueStat** is a comprehensive, accessible statistical analysis application designed for educational use. Built with Streamlit, it provides an intuitive interface for performing statistical calculations, creating visualizations, and exploring statistical concepts through interactive simulations.

[![WCAG 2.1 Level AA Compliant](https://img.shields.io/badge/WCAG%202.1-Level%20AA-green.svg)](ADA_COMPLIANCE_REVIEW_FINAL.md)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red.svg)](https://streamlit.io/)

## 🎯 Purpose

CueStat serves as an **educational statistics platform** that enables students and instructors to:
- Perform comprehensive statistical analyses without programming knowledge
- Visualize probability distributions and statistical concepts
- Explore statistical principles through interactive simulations
- Generate publication-ready tables and charts
- Learn through hands-on experimentation with real and simulated data

## ✨ Key Features

### 📥 Data Input
- **File Upload**: Support for CSV, Excel files
- **Google Sheets**: Direct import from published Google Sheets with **automatic link loading**
  - Share a Google Sheet with one click using auto-loading links
  - Students click a link and data loads instantly—no manual URL entry needed
- **Manual Entry**: Built-in spreadsheet-style data editor
- **Single Dataframe Architecture**: Simplified workflow with one active dataset

#### 🔗 Auto-Loading Google Sheets (NEW!)
Teachers can now share Google Sheets data with students via a single auto-loading link:

1. **Publish your Google Sheet** as CSV in Google Sheets (File → Share → Publish to web, select CSV format)
2. **Create an auto-loading link** by appending the published URL as a query parameter:
   ```
   https://your-cuestat-url.com?sheets_url=<your-published-sheet-csv-url>
   ```
3. **Share the link** with students—when they click it, data loads automatically!

**Example use case**: A teacher publishes their class dataset as a Google Sheet and shares the auto-loading link in the syllabus. Students click once and the data is ready for analysis—no need to download files or paste URLs.

### 📈 Descriptive Statistics
- Comprehensive summary statistics (mean, median, mode, std, variance, quartiles, etc.)
- Histogram and box plot visualizations
- Outlier detection and analysis
- Combined results table with all selected columns

### 📊 Probability Distributions
Interactive calculators for:
- **Normal Distribution**: Z-scores, probabilities, and quantiles
- **t-Distribution**: Degrees of freedom and critical values
- **Chi-Square Distribution**: Right-tail probabilities
- **F-Distribution**: Two-sided probability calculations
- **Binomial Distribution**: Success probability and cumulative distributions

### 📋 Tables
- **Frequency Tables**: One-way frequency distributions
- **Two-Way Tables**: Cross-tabulation with row/column/total percentages
- **Contingency Tables**: Chi-square tests for independence

### 🎲 Interactive Simulations
- **Central Limit Theorem**: Demonstrates sampling distribution convergence
- **Confidence Intervals**: Visualizes coverage and variability
- **Binomial Distribution**: Interactive probability mass function exploration
- **t vs Normal Distribution**: Compares t-distribution to standard normal across degrees of freedom
- **F-Statistic Explorer**: Illustrates within-group vs between-group variation and ANOVA concepts

### 🔬 Statistical Inference
- **Confidence Intervals**: t-intervals for population means
- **Hypothesis Testing**: One-sample, two-sample, paired t-tests, proportion tests, chi-square tests

## ♿ Accessibility

CueStat is **WCAG 2.1 Level AA compliant** with:
- ✅ Full keyboard navigation support
- ✅ Screen reader compatibility (NVDA, JAWS, VoiceOver)
- ✅ High contrast mode support
- ✅ Clear focus indicators
- ✅ Comprehensive alternative text for visualizations
- ✅ Responsive design for all devices
- ✅ 97.6% compliance score

See [ADA Compliance Review](ADA_COMPLIANCE_REVIEW_FINAL.md) for detailed accessibility documentation.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/profegabi40/CompuStats.git
   cd CompuStats
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

   **Quick restart on port 8053 (recommended for this workspace):**
   ```bash
   ./restart_streamlit.sh
   ```

4. **Access the app**
   - Open your browser to `http://localhost:8501` (default)
   - If using `./restart_streamlit.sh`, use `http://localhost:8053`
   - The app should launch automatically

## 📦 Dependencies

Core libraries:
- `streamlit` - Web application framework
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `scipy` - Scientific computing and statistical functions
- `matplotlib` - Plotting and visualization
- `openpyxl` - Excel file support
- `st-aggrid` - Interactive data grids

See [requirements.txt](requirements.txt) for complete list.

## 📖 Usage

1. **Select a Tab** from the sidebar:
   - Data: Import or manually enter your data
   - Descriptive Statistics: Analyze your data
   - Probability Distributions: Calculate probabilities
   - Tables: Create frequency and contingency tables
   - Plots: Generate visualizations
   - Confidence Intervals: Construct interval estimates
   - Hypothesis Testing: Perform statistical tests
   - Simulations: Explore statistical concepts interactively

2. **Load Your Data**:
   - Upload a CSV/Excel file, or
   - Paste data into the built-in editor

3. **Choose Your Analysis**:
   - Select columns to analyze
   - Configure parameters
   - View results and visualizations

4. **Explore Simulations**:
   - Adjust parameters with interactive sliders
   - Observe real-time updates
   - Read accessibility descriptions for all plots

## 🎓 Educational Focus

CueStat is designed with **Universal Design for Learning (UDL)** principles:
- **Multiple Representations**: Visual plots + text descriptions + tables
- **Interactive Exploration**: Hands-on parameter manipulation
- **Immediate Feedback**: Real-time calculation updates
- **Scaffolded Learning**: Step-by-step workflows with guidance
- **Clear Communication**: Actionable error messages and help tooltips

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

### Accessibility Guidelines
When contributing, please ensure:
- All new visualizations include descriptive captions
- Form inputs have labels and help text
- Keyboard navigation works for new features
- Screen readers can access all content

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **profegabi40** - Initial development and accessibility implementation

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Statistical functions from [SciPy](https://scipy.org/)
- Accessibility testing with WAVE, axe DevTools, and Lighthouse
- Color palette designed for WCAG contrast compliance

## 📧 Contact

For questions, feedback, or accessibility concerns:
- Open an issue on GitHub
- Tag with appropriate labels (bug, enhancement, accessibility)

## 🗺️ Roadmap

Future enhancements:
- [ ] Additional probability distributions (Poisson, Exponential)
- [ ] Regression analysis (Linear, Multiple)
- [ ] ANOVA (One-way, Two-way)
- [ ] Non-parametric tests (Mann-Whitney, Kruskal-Wallis)
- [ ] Data export functionality
- [ ] Saved analysis templates
- [ ] Multi-language support

---

**Version**: 1.0  
**Last Updated**: December 16, 2025  
**Accessibility Compliance**: WCAG 2.1 Level AA ✓
