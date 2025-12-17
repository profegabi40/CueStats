import streamlit as st
import pandas as pd
import numpy as np
import io
from scipy import stats
import matplotlib.pyplot as plt # Added for plotting
import logging
# Toggle to enable AgGrid debug prints (set to True only when debugging)
DEBUG_AGRID = False
try:
    from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
    ST_AGRID_AVAILABLE = True
except Exception:
    ST_AGRID_AVAILABLE = False
# --- Streamlit App Configuration ---
st.set_page_config(layout="wide", page_title="CueStats")
st.title("CueStats: STAT C1000 Analysis Tool")

# Inject CSS to style tables globally: solid black borders, bold headers, auto-fit columns
st.markdown("""
<style>
/* Apply to Streamlit-rendered tables and pandas Styler HTML tables */
div[data-testid="stDataFrame"] table, div[data-testid="stTable"] table, .stMarkdown table {
  border-collapse: collapse !important;
  table-layout: auto !important;
  width: auto !important;
}
.stMarkdown table th, div[data-testid="stDataFrame"] table th, div[data-testid="stTable"] table th {
  border: 2px solid black !important;
  padding: 6px !important;
  font-weight: 700 !important;
  white-space: nowrap !important;
}
.stMarkdown table td, div[data-testid="stDataFrame"] table td, div[data-testid="stTable"] table td {
  border: 1px solid black !important;
  padding: 6px !important;
  white-space: nowrap !important;
}
/* Bold row and column labels in interactive tables (st.dataframe, st.data_editor) */
div[data-testid="stDataFrame"] th, div[data-testid="stTable"] th {
  font-weight: 700 !important;
}
/* Target Streamlit's ArrowTable and other table components */
[data-testid="stDataFrame"] tbody tr th,
[data-testid="stDataFrame"] thead tr th,
[data-testid="stTable"] tbody tr th,
[data-testid="stTable"] thead tr th {
  font-weight: 700 !important;
}
/* Style st.data_editor and st.dataframe cells with solid black borders */
[data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th,
[data-testid="stTable"] td, [data-testid="stTable"] th {
  border: 1px solid black !important;
}
/* Target all table elements in data editor container */
[data-testid="stDataFrame"] table {
  border: 2px solid black !important;
  border-collapse: collapse !important;
}
[data-testid="stDataFrame"] tr {
  border: 1px solid black !important;
}
[data-testid="stDataFrame"] td, 
[data-testid="stDataFrame"] th {
  border: 1px solid black !important;
}
/* Ensure borders appear on all interactive table elements */
[role="table"] {
  border: 1px solid black !important;
}
[role="rowgroup"] {
  border: 1px solid black !important;
}
[role="row"] {
  border: 1px solid black !important;
}
[role="gridcell"], 
[role="columnheader"] {
  border: 1px solid black !important;
}
/* Focus indicators for keyboard navigation */
button:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible {
  outline: 3px solid #0173B2 !important;
  outline-offset: 2px !important;
  box-shadow: 0 0 0 3px rgba(1, 115, 178, 0.25) !important;
}
/* Skip to content link */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #0173B2;
  color: white;
  padding: 8px;
  text-decoration: none;
  z-index: 100;
}
.skip-link:focus {
  top: 0;
}
/* Fix ARIA attributes on Streamlit-generated iframes */
/* Remove invalid ARIA attributes from iframes in sidebar and main menu */
.stSidebar iframe,
#MainMenu iframe {
  /* Ensure iframes have proper title for accessibility */
}
/* Add title attribute via CSS pseudo-elements won't work, so we ensure via JS */
/* Hide iframes that don't need to be exposed to screen readers */
.stSidebar iframe[src*="about:blank"],
#MainMenu iframe[src*="about:blank"] {
  display: none !important;
}
/* Fix contrast issues for Streamlit emotion-cache elements */
/* Ensure WCAG 2 AA compliance (4.5:1 for normal text, 3:1 for large text) */
.st-emotion-cache-1sct1q3,
[class*="st-emotion-cache"] {
  color: #000000 !important; /* Black text for maximum contrast */
}
/* If element is on dark background, ensure white text */
.st-emotion-cache-1sct1q3[style*="background"],
[class*="st-emotion-cache"][style*="background: rgb(14, 17, 23)"],
[class*="st-emotion-cache"][style*="background:#0e1117"],
[class*="st-emotion-cache"][style*="background-color:#0e1117"],
[class*="st-emotion-cache"][style*="background-color: rgb(14, 17, 23)"] {
  color: #FFFFFF !important; /* White text on dark backgrounds */
}
/* Ensure links and interactive elements have sufficient contrast */
.st-emotion-cache-1sct1q3 a,
[class*="st-emotion-cache"] a {
  color: #0173B2 !important; /* Accessible blue - passes WCAG AA */
  text-decoration: underline !important;
}
/* Ensure button text has proper contrast */
.st-emotion-cache-1sct1q3 button,
[class*="st-emotion-cache"] button {
  color: #000000 !important;
  background-color: #FFFFFF !important;
  border: 2px solid #000000 !important;
}
.st-emotion-cache-1sct1q3 button:hover,
[class*="st-emotion-cache"] button:hover {
  background-color: #0173B2 !important;
  color: #FFFFFF !important;
  border-color: #0173B2 !important;
}
/* Fix any low contrast text in sidebar or main content */
.stSidebar .st-emotion-cache-1sct1q3,
.stSidebar [class*="st-emotion-cache"] {
  color: #262730 !important; /* Dark gray on light background - 12.63:1 ratio */
}
/* Ensure proper contrast for all text elements */
.st-emotion-cache-1sct1q3 p,
.st-emotion-cache-1sct1q3 span,
.st-emotion-cache-1sct1q3 div,
[class*="st-emotion-cache"] p,
[class*="st-emotion-cache"] span {
  color: inherit !important;
}
/* Fix placeholder text contrast */
.st-emotion-cache-1sct1q3 input::placeholder,
[class*="st-emotion-cache"] input::placeholder {
  color: #6c757d !important; /* Medium gray - 4.5:1 ratio */
  opacity: 1 !important;
}
</style>
<script>
// Fix ARIA attributes on Streamlit iframes
(function() {
    // Wait for DOM to be ready
    const fixIframeAria = function() {
        // Find all iframes in sidebar and main menu
        const iframes = document.querySelectorAll('.stSidebar iframe, #MainMenu iframe');
        iframes.forEach(function(iframe) {
            // Remove invalid ARIA attributes from iframes
            iframe.removeAttribute('aria-hidden');
            iframe.removeAttribute('aria-label');
            iframe.removeAttribute('aria-labelledby');
            iframe.removeAttribute('aria-describedby');
            
            // Add proper title if missing
            if (!iframe.getAttribute('title')) {
                iframe.setAttribute('title', 'Streamlit component frame');
            }
            
            // If iframe is empty or about:blank, hide from accessibility tree
            if (iframe.src === '' || iframe.src.includes('about:blank')) {
                iframe.setAttribute('aria-hidden', 'true');
                iframe.setAttribute('tabindex', '-1');
            }
        });
    };
    
    // Run immediately
    fixIframeAria();
    
    // Also run on Streamlit reruns
    if (window.addEventListener) {
        window.addEventListener('load', fixIframeAria);
    }
    
    // Use MutationObserver to catch dynamically added iframes
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(fixIframeAria);
        observer.observe(document.body, { childList: true, subtree: true });
    }
})();

// Fix accessible names for Streamlit toolbar and menu buttons
(function() {
    const fixButtonNames = function() {
        // Fix toolbar action buttons
        const toolbarButtons = document.querySelectorAll('.stToolbarActionButton button, [data-testid="stToolbarActionButton"] button');
        toolbarButtons.forEach(function(button, index) {
            if (!button.getAttribute('aria-label') && !button.getAttribute('title')) {
                // Try to get text content
                const textContent = button.textContent.trim();
                if (textContent) {
                    button.setAttribute('aria-label', textContent);
                } else {
                    // Check for common toolbar buttons by their position/class
                    const parentDiv = button.closest('[data-testid="stToolbarActionButton"]');
                    if (parentDiv) {
                        const svgIcon = button.querySelector('svg');
                        if (svgIcon) {
                            // Common Streamlit toolbar buttons
                            if (index === 0) {
                                button.setAttribute('aria-label', 'Settings');
                            } else if (index === 1) {
                                button.setAttribute('aria-label', 'Menu options');
                            } else {
                                button.setAttribute('aria-label', 'Toolbar action ' + (index + 1));
                            }
                        }
                    }
                }
            }
        });
        
        // Fix main menu buttons
        const menuButtons = document.querySelectorAll('#MainMenu button, [data-testid="stBaseButton-header"] button, [data-testid="stBaseButton-headerNoPadding"] button');
        menuButtons.forEach(function(button) {
            if (!button.getAttribute('aria-label') && !button.getAttribute('title')) {
                const textContent = button.textContent.trim();
                if (textContent) {
                    button.setAttribute('aria-label', textContent);
                } else {
                    // Check if it's the hamburger menu button
                    const svgIcon = button.querySelector('svg');
                    if (svgIcon) {
                        const parent = button.closest('#MainMenu');
                        if (parent) {
                            button.setAttribute('aria-label', 'Open main menu');
                        }
                    }
                }
            }
            
            // Ensure button role is set
            if (!button.getAttribute('role')) {
                button.setAttribute('role', 'button');
            }
        });
        
        // Fix buttons with kind="header" or kind="headerNoPadding"
        const headerButtons = document.querySelectorAll('[kind="header"] button, [kind="headerNoPadding"] button');
        headerButtons.forEach(function(button) {
            if (!button.getAttribute('aria-label') && !button.getAttribute('title')) {
                const textContent = button.textContent.trim();
                if (textContent) {
                    button.setAttribute('aria-label', textContent);
                } else {
                    button.setAttribute('aria-label', 'Menu button');
                }
            }
        });
        
        // Fix any button within emotion-cache divs that don't have accessible names
        const emotionButtons = document.querySelectorAll('[class*="emotion-cache"] button');
        emotionButtons.forEach(function(button) {
            if (!button.getAttribute('aria-label') && !button.textContent.trim() && !button.getAttribute('title')) {
                // Check for nearby text or icons
                const ariaLabel = button.getAttribute('data-testid') || 
                                 button.closest('[data-testid]')?.getAttribute('data-testid') || 
                                 'Button';
                button.setAttribute('aria-label', ariaLabel.replace(/([A-Z])/g, ' $1').trim());
            }
        });
    };
    
    // Run immediately
    fixButtonNames();
    
    // Run on load
    if (window.addEventListener) {
        window.addEventListener('load', fixButtonNames);
    }
    
    // Monitor for dynamically added buttons
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(fixButtonNames);
        observer.observe(document.body, { childList: true, subtree: true, attributes: false });
    }
    
    // Also run on Streamlit reruns (after a short delay)
    setTimeout(fixButtonNames, 500);
    setTimeout(fixButtonNames, 1000);
})();

// Ensure every form element has a proper label
(function() {
    const fixFormLabels = function() {
        // Fix file uploader input
        const fileInputs = document.querySelectorAll('input[data-testid="stFileUploaderDropzoneInput"]');
        fileInputs.forEach(function(input) {
            // Check if it already has a label
            const inputId = input.id || 'file-upload-' + Math.random().toString(36).substr(2, 9);
            input.id = inputId;
            
            // Check if label exists
            let label = document.querySelector('label[for="' + inputId + '"]');
            if (!label) {
                // Look for nearby label text
                const container = input.closest('[data-testid="stFileUploader"]');
                if (container) {
                    const labelText = container.querySelector('label, .stFileUploader label');
                    if (labelText && labelText.textContent.trim()) {
                        // Associate existing label with input
                        labelText.setAttribute('for', inputId);
                    } else {
                        // Create a new label
                        label = document.createElement('label');
                        label.setAttribute('for', inputId);
                        label.textContent = 'Choose a file to upload';
                        label.style.position = 'absolute';
                        label.style.left = '-10000px';
                        label.style.width = '1px';
                        label.style.height = '1px';
                        label.style.overflow = 'hidden';
                        input.parentNode.insertBefore(label, input);
                    }
                }
            }
            
            // Ensure aria-label as backup
            if (!input.getAttribute('aria-label') && !input.getAttribute('aria-labelledby')) {
                const container = input.closest('[data-testid="stFileUploader"]');
                if (container) {
                    const headingText = container.querySelector('p, label, div');
                    const labelText = headingText ? headingText.textContent.trim() : 'File upload';
                    input.setAttribute('aria-label', labelText || 'Choose a file to upload');
                }
            }
        });
        
        // Fix any other unlabeled inputs
        const allInputs = document.querySelectorAll('input:not([type="hidden"])');
        allInputs.forEach(function(input) {
            // Skip if already has label association or aria-label
            if (input.getAttribute('aria-label') || 
                input.getAttribute('aria-labelledby') || 
                document.querySelector('label[for="' + input.id + '"]')) {
                return;
            }
            
            // Try to find associated label by proximity
            const parentLabel = input.closest('label');
            if (parentLabel) {
                // Input is inside a label, which is valid
                return;
            }
            
            // Look for Streamlit's label structure
            const stWidget = input.closest('[data-testid*="stText"], [data-testid*="stNumber"], [data-testid*="stSelect"]');
            if (stWidget) {
                const widgetLabel = stWidget.querySelector('label');
                if (widgetLabel && widgetLabel.textContent.trim()) {
                    // Create unique ID if needed
                    if (!input.id) {
                        input.id = 'input-' + Math.random().toString(36).substr(2, 9);
                    }
                    widgetLabel.setAttribute('for', input.id);
                } else if (!input.getAttribute('aria-label')) {
                    // Fallback: add aria-label based on context
                    const testId = stWidget.getAttribute('data-testid');
                    input.setAttribute('aria-label', testId ? testId.replace(/^st/, '').replace(/([A-Z])/g, ' $1').trim() : 'Input field');
                }
            }
        });
        
        // Fix textareas
        const textareas = document.querySelectorAll('textarea');
        textareas.forEach(function(textarea) {
            if (!textarea.getAttribute('aria-label') && 
                !textarea.getAttribute('aria-labelledby') && 
                !document.querySelector('label[for="' + textarea.id + '"]')) {
                
                const stWidget = textarea.closest('[data-testid*="stText"]');
                if (stWidget) {
                    const widgetLabel = stWidget.querySelector('label');
                    if (widgetLabel && widgetLabel.textContent.trim()) {
                        if (!textarea.id) {
                            textarea.id = 'textarea-' + Math.random().toString(36).substr(2, 9);
                        }
                        widgetLabel.setAttribute('for', textarea.id);
                    } else {
                        textarea.setAttribute('aria-label', 'Text input area');
                    }
                }
            }
        });
        
        // Fix select elements
        const selects = document.querySelectorAll('select');
        selects.forEach(function(select) {
            if (!select.getAttribute('aria-label') && 
                !select.getAttribute('aria-labelledby') && 
                !document.querySelector('label[for="' + select.id + '"]')) {
                
                const stWidget = select.closest('[data-testid*="stSelect"]');
                if (stWidget) {
                    const widgetLabel = stWidget.querySelector('label');
                    if (widgetLabel && widgetLabel.textContent.trim()) {
                        if (!select.id) {
                            select.id = 'select-' + Math.random().toString(36).substr(2, 9);
                        }
                        widgetLabel.setAttribute('for', select.id);
                    } else {
                        select.setAttribute('aria-label', 'Select option');
                    }
                }
            }
        });
    };
    
    // Run immediately
    fixFormLabels();
    
    // Run on load
    if (window.addEventListener) {
        window.addEventListener('load', fixFormLabels);
    }
    
    // Monitor for dynamically added form elements
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(fixFormLabels);
        observer.observe(document.body, { childList: true, subtree: true });
    }
    
    // Run on Streamlit reruns
    setTimeout(fixFormLabels, 500);
    setTimeout(fixFormLabels, 1000);
    setTimeout(fixFormLabels, 2000);
})();
</script>
""", unsafe_allow_html=True)


# --- Global Variables/Session State ---
# Using st.session_state for persistent data across reruns
if 'global_dataframes' not in st.session_state:
    st.session_state.global_dataframes = {}

if 'manual_entry_df' not in st.session_state:
    st.session_state.manual_entry_df = pd.DataFrame({'Column A': ['']})

# --- Helper Functions ---
def process_manual_entry_data(df):
    # Remove ALL auto-generated/internal columns (those with :: prefix)
    if isinstance(df, pd.DataFrame):
        internal_cols = [col for col in df.columns if str(col).startswith('::')]
        if internal_cols:
            df = df.drop(columns=internal_cols)

    # Convert columns to numeric where possible
    processed_df = df.copy()
    for col in processed_df.columns:
        converted_col = pd.to_numeric(processed_df[col], errors='coerce')
        # If at least some values could be converted, use the converted column
        if not converted_col.isna().all():
            processed_df[col] = converted_col.fillna(processed_df[col]) # Fill non-numeric back with original string
    return processed_df

def sanitize_manual_entry_df_state():
    """Remove any internal columns (starting with '::') from the session manual_entry_df.

    This helps prevent UI components (AgGrid / Arrow) from exposing internal ID columns.
    """
    try:
        df = st.session_state.get('manual_entry_df')
        if isinstance(df, pd.DataFrame):
            internal = [c for c in df.columns if str(c).startswith('::')]
            if internal:
                st.session_state.manual_entry_df = df.drop(columns=internal)
    except Exception:
        pass

def styled_dataframe_html(df, hide_index=False):
    """Return HTML for a pandas DataFrame with solid black borders and auto column widths.

    This uses pandas Styler and is intended to be rendered with
    `st.markdown(html, unsafe_allow_html=True)` so columns size to their contents
    and table cells have solid black borders.
    """
    try:
        # Ensure we have a DataFrame
        if not isinstance(df, (pd.DataFrame, pd.Series)):
            return str(df)
        # Convert Series to DataFrame
        if isinstance(df, pd.Series):
            df = df.to_frame()

        styler = df.style
        # Hide index if requested
        if hide_index:
            styler = styler.hide(axis='index')
        # Table attributes: allow automatic layout so columns fit their contents
        styler = styler.set_table_attributes('style="border-collapse:collapse; width:auto; table-layout:auto;"')

        # Apply consistent cell/heading styles: solid black borders and no wrapping
        table_styles = [
            {"selector": "th", "props": [("border", "2px solid black"), ("padding", "6px"), ("white-space", "nowrap"), ("font-weight", "700")]},
            {"selector": "td", "props": [("border", "1px solid black"), ("padding", "6px"), ("white-space", "nowrap")]},
        ]
        styler = styler.set_table_styles(table_styles)

        # Also set cell properties generically (fallback)
        styler = styler.set_properties(**{"border": "1px solid black", "padding": "6px", "white-space": "nowrap"})

        return styler.to_html()
    except Exception:
        try:
            return df.to_html(border=1, index=not hide_index)
        except Exception:
            return str(df)

def get_numeric_columns():
    numeric_columns = []
    if 'active_data' in st.session_state.global_dataframes:
        df = st.session_state.global_dataframes['active_data']
        for col in df.columns:
            # Check if the column can be coerced to numeric and has at least one non-NaN numeric value
            if pd.to_numeric(df[col], errors='coerce').notna().any():
                numeric_columns.append(col)
    return sorted(list(set(numeric_columns)))

def get_all_columns():
    all_cols = []
    if 'active_data' in st.session_state.global_dataframes:
        df = st.session_state.global_dataframes['active_data']
        all_cols = list(df.columns)
    return sorted(list(set(all_cols)))

def get_data_from_col_string(col_string):
    if not col_string: raise ValueError("Column string cannot be empty.")
    df = st.session_state.global_dataframes.get('active_data')
    if df is None: raise ValueError("No active dataframe found. Please load data first.")
    if col_string not in df.columns: raise ValueError(f"Column '{col_string}' not found in active dataframe.")
    data = pd.to_numeric(df[col_string], errors='coerce').dropna()
    if data.empty: raise ValueError(f"Selected column '{col_string}' contains no valid numerical data.")
    return data

def calculate_descriptive_statistics(data):
    if not isinstance(data, pd.Series): data = pd.Series(data)
    data = pd.to_numeric(data, errors='coerce').dropna()
    if data.empty: return {"Error": "Input data contains no valid numerical values after cleaning."}
    # Use OrderedDict to maintain specific order: five-number summary first
    from collections import OrderedDict
    stats_dict = OrderedDict([
        ('Min Value', data.min()),
        ('Q1 (25th Percentile)', data.quantile(0.25)),
        ('Median', data.median()),
        ('Q3 (75th Percentile)', data.quantile(0.75)),
        ('Max Value', data.max()),
        ('n', data.count()),
        ('Mean', data.mean()),
        ('Mode', list(stats.mode(data, keepdims=True).mode) if len(stats.mode(data, keepdims=True).mode) > 1 else stats.mode(data, keepdims=True).mode[0]),
        ('Standard Deviation (s)', data.std()),
        ('Variance', data.var()),
        ('Range', data.max() - data.min()),
        ('IQR', data.quantile(0.75) - data.quantile(0.25)),
        ('Skewness', data.skew()),
        ('Kurtosis', data.kurtosis())
    ])
    return stats_dict

def calculate_normal_distribution(mean, std_dev, x=None, a=None, b=None, calc_type='pdf'):
    if std_dev <=0: raise ValueError("Standard deviation must be positive.")
    dist = stats.norm(loc=mean, scale=std_dev)
    if calc_type == 'pdf':
        if x is None: raise ValueError("For PDF calculation, 'x' must be provided.")
        return dist.pdf(x)
    elif calc_type == 'cdf':
        if x is None: raise ValueError("For CDF calculation, 'x' must be provided.")
        return dist.cdf(x)
    elif calc_type == 'survival':
        if x is None: raise ValueError("For survival function calculation, 'x' must be provided.")
        return dist.sf(x)
    elif calc_type == 'interval':
        if a is None or b is None: raise ValueError("For interval calculation, 'a' and 'b' must be provided.")
        if a >= b: raise ValueError("For interval calculation, 'a' must be less than 'b'.")
        return dist.cdf(b) - dist.cdf(a)
    else: raise ValueError(f"Invalid calculation type: {calc_type}")

def calculate_binomial_distribution(n, p, k=None, a=None, b=None, calc_type='pmf'):
    if not (0 <= p <= 1): raise ValueError("Probability 'p' must be between 0 and 1.")
    if not isinstance(n, int) or n <= 0: raise ValueError("Number of trials 'n' must be a positive integer.")
    dist = stats.binom(n=n, p=p)
    if calc_type == 'pmf':
        if k is None: raise ValueError("For PMF calculation, 'k' must be provided.")
        return dist.pmf(k)
    elif calc_type == 'cdf':
        if k is None: raise ValueError("For CDF calculation, 'k' must be provided.")
        return dist.cdf(k)
    elif calc_type == 'cdf_strict':
        if k is None: raise ValueError("For CDF calculation, 'k' must be provided.")
        return dist.cdf(k - 1) if k > 0 else 0
    elif calc_type == 'survival':
        if k is None: raise ValueError("For survival function calculation, 'k' must be provided.")
        return dist.sf(k - 1)
    elif calc_type == 'survival_strict':
        if k is None: raise ValueError("For survival function calculation, 'k' must be provided.")
        return dist.sf(k)
    elif calc_type == 'interval':
        if a is None or b is None: raise ValueError("For interval calculation, 'a' and 'b' must be provided.")
        if not isinstance(a, int) or not isinstance(b, int) or a > b: raise ValueError("For interval calculation, 'a' and 'b' must be integers and a <= b.")
        return dist.cdf(b) - dist.cdf(a - 1)
    elif calc_type == 'interval_inclusive':
        if a is None or b is None: raise ValueError("For interval calculation, 'a' and 'b' must be provided.")
        if not isinstance(a, int) or not isinstance(b, int) or a > b: raise ValueError("For interval calculation, 'a' and 'b' must be integers and a <= b.")
        return dist.cdf(b) - dist.cdf(a - 1)
    else: raise ValueError(f"Invalid calculation type: {calc_type}")

def calculate_chi_square_distribution(df, x=None, a=None, b=None, calc_type='pdf'):
    if not isinstance(df, int) or df <= 0: raise ValueError("Degrees of freedom 'df' must be a positive integer.")
    dist = stats.chi2(df=df)
    if calc_type == 'pdf':
        if x is None: raise ValueError("For PDF calculation, 'x' must be provided.")
        return dist.pdf(x)
    elif calc_type in ['cdf', 'cdf_strict']:
        if x is None: raise ValueError("For CDF calculation, 'x' must be provided.")
        return dist.cdf(x)
    elif calc_type in ['survival', 'survival_strict']:
        if x is None: raise ValueError("For survival function calculation, 'x' must be provided.")
        return dist.sf(x)
    elif calc_type == 'interval':
        if a is None or b is None: raise ValueError("For interval calculation, 'a' and 'b' must be provided.")
        if a >= b: raise ValueError("For interval calculation, 'a' must be less than 'b'.")
        return dist.cdf(b) - dist.cdf(a)
    else: raise ValueError(f"Invalid calculation type: {calc_type}")

def calculate_student_t_distribution(df, x=None, a=None, b=None, calc_type='pdf'):
    if not isinstance(df, int) or df <= 0: raise ValueError("Degrees of freedom 'df' must be a positive integer.")
    dist = stats.t(df=df)
    if calc_type == 'pdf':
        if x is None: raise ValueError("For PDF calculation, 'x' must be provided.")
        return dist.pdf(x)
    elif calc_type in ['cdf', 'cdf_strict']:
        if x is None: raise ValueError("For CDF calculation, 'x' must be provided.")
        return dist.cdf(x)
    elif calc_type in ['survival', 'survival_strict']:
        if x is None: raise ValueError("For survival function calculation, 'x' must be provided.")
        return dist.sf(x)
    elif calc_type == 'interval':
        if a is None or b is None: raise ValueError("For interval calculation, 'a' and 'b' must be provided.")
        if a >= b: raise ValueError("For interval calculation, 'a' must be less than 'b'.")
        return dist.cdf(b) - dist.cdf(a)
    else: raise ValueError(f"Invalid calculation type: {calc_type}")

def calculate_f_distribution(dfn, dfd, x=None, a=None, b=None, calc_type='pdf'):
    if not isinstance(dfn, int) or dfn <= 0: raise ValueError("Numerator degrees of freedom 'dfn' must be a positive integer.")
    if not isinstance(dfd, int) or dfd <= 0: raise ValueError("Denominator degrees of freedom 'dfd' must be a positive integer.")
    dist = stats.f(dfn=dfn, dfd=dfd)
    if calc_type == 'pdf':
        if x is None: raise ValueError("For PDF calculation, 'x' must be provided.")
        return dist.pdf(x)
    elif calc_type in ['cdf', 'cdf_strict']:
        if x is None: raise ValueError("For CDF calculation, 'x' must be provided.")
        return dist.cdf(x)
    elif calc_type in ['survival', 'survival_strict']:
        if x is None: raise ValueError("For survival function calculation, 'x' must be provided.")
        return dist.sf(x)
    elif calc_type == 'interval':
        if a is None or b is None: raise ValueError("For interval calculation, 'a' and 'b' must be provided.")
        if a >= b: raise ValueError("For interval calculation, 'a' must be less than 'b'.")
        return dist.cdf(b) - dist.cdf(a)
    else: raise ValueError(f"Invalid calculation type: {calc_type}")

def plot_normal_distribution(mean, std_dev, x_min_factor=-4, x_max_factor=4, num_points=500, shade_x=None, shade_a=None, shade_b=None, calc_type=None):
    if std_dev <= 0: raise ValueError("Standard deviation must be positive.")
    x_values = np.linspace(mean + x_min_factor * std_dev, mean + x_max_factor * std_dev, num_points)
    pdf_values = stats.norm.pdf(x_values, loc=mean, scale=std_dev)
    fig, ax = plt.subplots(1, 1, figsize=(7.5, 4.5))
    # WCAG-compliant color: accessible blue
    ax.plot(x_values, pdf_values, color='#0173B2', linewidth=2, label='PDF')
    
    # Add shading based on calculation type
    if calc_type == 'cdf' and shade_x is not None:
        shade_mask = x_values <= shade_x
        # Accessible blue with hatching pattern for non-color indicators
        ax.fill_between(x_values[shade_mask], pdf_values[shade_mask], alpha=0.5, color='#0173B2', hatch='///', edgecolor='#0173B2', label=f'P(X < {shade_x})')
        # Accessible orange for contrast
        ax.axvline(shade_x, color='#DE8F05', linestyle='--', linewidth=2, label=f'x = {shade_x}')
    elif calc_type == 'survival' and shade_x is not None:
        shade_mask = x_values >= shade_x
        ax.fill_between(x_values[shade_mask], pdf_values[shade_mask], alpha=0.5, color='#0173B2', hatch='///', edgecolor='#0173B2', label=f'P(X > {shade_x})')
        ax.axvline(shade_x, color='#DE8F05', linestyle='--', linewidth=2, label=f'x = {shade_x}')
    elif calc_type == 'interval' and shade_a is not None and shade_b is not None:
        shade_mask = (x_values >= shade_a) & (x_values <= shade_b)
        ax.fill_between(x_values[shade_mask], pdf_values[shade_mask], alpha=0.5, color='#0173B2', hatch='///', edgecolor='#0173B2', label=f'P({shade_a} < X < {shade_b})')
        ax.axvline(shade_a, color='#DE8F05', linestyle='--', linewidth=2, label=f'a = {shade_a}')
        ax.axvline(shade_b, color='#DE8F05', linestyle='--', linewidth=2, label=f'b = {shade_b}')
    
    ax.set_title(f'Normal Distribution (μ={mean}, σ={std_dev})', fontsize=14)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.grid(True, alpha=0.5)
    ax.legend()
    plt.tight_layout()
    return fig

def plot_binomial_distribution(n, p, shade_k=None, shade_a=None, shade_b=None, calc_type=None):
    if not isinstance(n, int) or n <= 0: raise ValueError("Number of trials 'n' must be a positive integer.")
    if not (0 < p < 1): raise ValueError("Probability 'p' must be between 0 and 1.")
    k_values = np.arange(0, n + 1)
    pmf_values = stats.binom.pmf(k_values, n=n, p=p)
    fig, ax = plt.subplots(1, 1, figsize=(7.5, 4.5))
    
    # Plot vertical lines (stems) from 0 to pmf value
    # Use both color AND line width for accessibility (not color alone)
    for k, pmf in zip(k_values, pmf_values):
        color = '#CCCCCC'  # Accessible gray (3:1 contrast)
        linewidth = 2
        markersize = 6
        # Determine if this point should be highlighted
        is_highlighted = False
        if calc_type == 'pmf' and shade_k is not None and k == shade_k:
            is_highlighted = True
        elif calc_type == 'cdf' and shade_k is not None and k <= shade_k:
            is_highlighted = True
        elif calc_type == 'cdf_strict' and shade_k is not None and k < shade_k:
            is_highlighted = True
        elif calc_type == 'survival' and shade_k is not None and k >= shade_k:
            is_highlighted = True
        elif calc_type == 'survival_strict' and shade_k is not None and k > shade_k:
            is_highlighted = True
        elif calc_type == 'interval' and shade_a is not None and shade_b is not None and shade_a < k < shade_b:
            is_highlighted = True
        elif calc_type == 'interval_inclusive' and shade_a is not None and shade_b is not None and shade_a <= k <= shade_b:
            is_highlighted = True
        
        if is_highlighted:
            color = '#0173B2'  # Accessible blue
            linewidth = 4  # Thicker line for highlighted values
            markersize = 10  # Larger marker
        
        ax.plot([k, k], [0, pmf], color=color, linewidth=linewidth, alpha=0.9)
        ax.plot(k, pmf, 'o', color=color, markersize=markersize, alpha=0.9)
    
    ax.set_title(f'Binomial Distribution (n={n}, p={p})', fontsize=14)
    ax.set_xlabel('Number of Successes (k)', fontsize=12)
    ax.set_ylabel('Probability', fontsize=12)
    ax.set_xticks(k_values)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.5)
    plt.tight_layout()
    return fig

def plot_chi_square_distribution(df, x_max_factor=5, num_points=500, shade_x=None, shade_a=None, shade_b=None, calc_type=None):
    if not isinstance(df, int) or df <= 0: raise ValueError("Degrees of freedom 'df' must be a positive integer.")
    max_x = df + x_max_factor * np.sqrt(2 * df)
    x_values = np.linspace(0, max_x, num_points)
    pdf_values = stats.chi2.pdf(x_values, df=df)
    fig, ax = plt.subplots(1, 1, figsize=(7.5, 4.5))
    ax.plot(x_values, pdf_values, color='#0173B2', linewidth=2, label='PDF')
    
    # Add shading based on calculation type
    if calc_type in ['cdf', 'cdf_strict'] and shade_x is not None:
        shade_mask = x_values <= shade_x
        ax.fill_between(x_values[shade_mask], pdf_values[shade_mask], alpha=0.5, color='#0173B2', hatch='///', edgecolor='#0173B2', label=f'P(X < {shade_x})')
        ax.axvline(shade_x, color='#DE8F05', linestyle='--', linewidth=2, label=f'x = {shade_x}')
    elif calc_type in ['survival', 'survival_strict'] and shade_x is not None:
        shade_mask = x_values >= shade_x
        ax.fill_between(x_values[shade_mask], pdf_values[shade_mask], alpha=0.5, color='#0173B2', hatch='///', edgecolor='#0173B2', label=f'P(X > {shade_x})')
        ax.axvline(shade_x, color='#DE8F05', linestyle='--', linewidth=2, label=f'x = {shade_x}')
    elif calc_type == 'interval' and shade_a is not None and shade_b is not None:
        shade_mask = (x_values >= shade_a) & (x_values <= shade_b)
        ax.fill_between(x_values[shade_mask], pdf_values[shade_mask], alpha=0.5, color='#0173B2', hatch='///', edgecolor='#0173B2', label=f'P({shade_a} < X < {shade_b})')
        ax.axvline(shade_a, color='#DE8F05', linestyle='--', linewidth=2, label=f'a = {shade_a}')
        ax.axvline(shade_b, color='#DE8F05', linestyle='--', linewidth=2, label=f'b = {shade_b}')
    
    ax.set_title(f'Chi-square Distribution (df={df})', fontsize=14)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.grid(True, alpha=0.5)
    ax.legend()
    plt.tight_layout()
    return fig

def plot_student_t_distribution(df, x_min_factor=-5, x_max_factor=5, num_points=500, shade_x=None, shade_a=None, shade_b=None, calc_type=None):
    if not isinstance(df, int) or df <= 0: raise ValueError("Degrees of freedom 'df' must be a positive integer.")
    if df > 2: std_dev_approx = np.sqrt(df / (df - 2)); x_values = np.linspace(x_min_factor * std_dev_approx, x_max_factor * std_dev_approx, num_points)
    else: x_values = np.linspace(x_min_factor * 2, x_max_factor * 2, num_points)
    pdf_values = stats.t.pdf(x_values, df=df)
    fig, ax = plt.subplots(1, 1, figsize=(7.5, 4.5))
    ax.plot(x_values, pdf_values, color='#0173B2', linewidth=2, label='PDF')
    
    # Add shading based on calculation type
    if calc_type in ['cdf', 'cdf_strict'] and shade_x is not None:
        shade_mask = x_values <= shade_x
        ax.fill_between(x_values[shade_mask], pdf_values[shade_mask], alpha=0.5, color='#0173B2', hatch='///', edgecolor='#0173B2', label=f'P(X < {shade_x})')
        ax.axvline(shade_x, color='#DE8F05', linestyle='--', linewidth=2, label=f'x = {shade_x}')
    elif calc_type in ['survival', 'survival_strict'] and shade_x is not None:
        shade_mask = x_values >= shade_x
        ax.fill_between(x_values[shade_mask], pdf_values[shade_mask], alpha=0.5, color='#0173B2', hatch='///', edgecolor='#0173B2', label=f'P(X > {shade_x})')
        ax.axvline(shade_x, color='#DE8F05', linestyle='--', linewidth=2, label=f'x = {shade_x}')
    elif calc_type == 'interval' and shade_a is not None and shade_b is not None:
        shade_mask = (x_values >= shade_a) & (x_values <= shade_b)
        ax.fill_between(x_values[shade_mask], pdf_values[shade_mask], alpha=0.5, color='#0173B2', hatch='///', edgecolor='#0173B2', label=f'P({shade_a} < X < {shade_b})')
        ax.axvline(shade_a, color='#DE8F05', linestyle='--', linewidth=2, label=f'a = {shade_a}')
        ax.axvline(shade_b, color='#DE8F05', linestyle='--', linewidth=2, label=f'b = {shade_b}')
    
    ax.set_title(f"Student's t-Distribution (df={df})", fontsize=14)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.grid(True, alpha=0.5)
    ax.legend()
    plt.tight_layout()
    return fig

def plot_f_distribution(dfn, dfd, x_max_factor=5, num_points=500, shade_x=None, shade_a=None, shade_b=None, calc_type=None):
    if not isinstance(dfn, int) or dfn <= 0: raise ValueError("Numerator degrees of freedom 'dfn' must be a positive integer.")
    if not isinstance(dfd, int) or dfd <= 0: raise ValueError("Denominator degrees of freedom 'dfd' must be a positive integer.")
    if dfd > 2: mean_f = dfd / (dfd - 2); max_x = mean_f + x_max_factor * np.sqrt(2 * dfd**2 * (dfn + dfd - 2) / (dfn * (dfd - 2)**2 * (dfd - 4))) if dfd > 4 else mean_f + x_max_factor * 2;
    if dfd > 2 and max_x < 5: max_x = 5
    else: max_x = 10 + x_max_factor
    x_values = np.linspace(0, max_x, num_points)
    x_values = x_values[x_values >= 0]
    pdf_values = stats.f.pdf(x_values, dfn=dfn, dfd=dfd)
    fig, ax = plt.subplots(1, 1, figsize=(7.5, 4.5))
    ax.plot(x_values, pdf_values, color='#0173B2', linewidth=2, label='PDF')
    
    # Add shading based on calculation type
    if calc_type in ['cdf', 'cdf_strict'] and shade_x is not None:
        shade_mask = x_values <= shade_x
        ax.fill_between(x_values[shade_mask], pdf_values[shade_mask], alpha=0.5, color='#0173B2', hatch='///', edgecolor='#0173B2', label=f'P(X < {shade_x})')
        ax.axvline(shade_x, color='#DE8F05', linestyle='--', linewidth=2, label=f'x = {shade_x}')
    elif calc_type in ['survival', 'survival_strict'] and shade_x is not None:
        shade_mask = x_values >= shade_x
        ax.fill_between(x_values[shade_mask], pdf_values[shade_mask], alpha=0.5, color='#0173B2', hatch='///', edgecolor='#0173B2', label=f'P(X > {shade_x})')
        ax.axvline(shade_x, color='#DE8F05', linestyle='--', linewidth=2, label=f'x = {shade_x}')
    elif calc_type == 'interval' and shade_a is not None and shade_b is not None:
        shade_mask = (x_values >= shade_a) & (x_values <= shade_b)
        ax.fill_between(x_values[shade_mask], pdf_values[shade_mask], alpha=0.5, color='#0173B2', hatch='///', edgecolor='#0173B2', label=f'P({shade_a} < X < {shade_b})')
        ax.axvline(shade_a, color='#DE8F05', linestyle='--', linewidth=2, label=f'a = {shade_a}')
        ax.axvline(shade_b, color='#DE8F05', linestyle='--', linewidth=2, label=f'b = {shade_b}')
    
    ax.set_title(f'F-Distribution (df1={dfn}, df2={dfd})', fontsize=14)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.grid(True, alpha=0.5)
    ax.legend()
    plt.tight_layout()
    return fig

def plot_histogram(data, bins='auto', title='Histogram', xlabel='Value', ylabel='Frequency', use_relative=False, force_integer_bins=False):
    if data.size == 0: raise ValueError("Input data is empty.")
    if not isinstance(data, pd.Series): data = pd.Series(data)
    numeric_data = pd.to_numeric(data, errors='coerce').dropna()
    if numeric_data.empty: raise ValueError("Input data contains no valid numerical data for histogram.")
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    
    # If force_integer_bins is True, create integer bin edges while maintaining the number of bins
    if force_integer_bins and isinstance(bins, int):
        data_min, data_max = numeric_data.min(), numeric_data.max()
        # Create integer bin edges that span the data range with approximately the requested number of bins
        bin_width = max(1, int(np.ceil((data_max - data_min) / bins)))
        bin_start = int(np.floor(data_min))
        bin_end = int(np.ceil(data_max))
        # Extend by one bin width to ensure max value gets its own bin with [,) rule
        bins = np.arange(bin_start, bin_end + bin_width + 1, bin_width)
    
    # Note: matplotlib's hist() uses [,) rule for all bins EXCEPT the last one
    # To enforce strict [,) for all bins, we extend bins and ensure the last bin includes the max
    # For strict [,) intervals: [a,b) means a is included, b goes to next bin
    if use_relative:
        weights = np.ones_like(numeric_data.to_numpy()) / len(numeric_data)
        counts, bin_edges, patches = ax.hist(numeric_data.to_numpy(), bins=bins, weights=weights, edgecolor='black', alpha=0.7)
        ylabel = 'Relative Frequency'
    else:
        counts, bin_edges, patches = ax.hist(numeric_data.to_numpy(), bins=bins, edgecolor='black', alpha=0.7)
        ylabel = 'Frequency'
    
    # Set x-axis ticks to show bin edges
    ax.set_xticks(bin_edges)
    # Format bin edge labels - use integers if they are whole numbers or forced
    if len(bin_edges) > 0:
        # Check if all bin edges are close to integers
        all_near_integers = all(abs(edge - round(edge)) < 0.01 for edge in bin_edges)
        
        if force_integer_bins or all_near_integers:
            # Display as integers
            ax.set_xticklabels([f'{int(round(edge))}' for edge in bin_edges], rotation=45, ha='right')
        else:
            # Determine decimal places needed based on bin width
            bin_width = bin_edges[1] - bin_edges[0] if len(bin_edges) > 1 else 1
            if bin_width < 0.01:
                decimal_places = 4
            elif bin_width < 0.1:
                decimal_places = 3
            elif bin_width < 1:
                decimal_places = 2
            elif bin_width < 10:
                decimal_places = 1
            else:
                decimal_places = 0
            ax.set_xticklabels([f'{edge:.{decimal_places}f}' for edge in bin_edges], rotation=45, ha='right')
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    return fig

def plot_box_plot(data, title='Box Plot', ylabel='Value', horizontal=False, labels=None):
    """Plot one or more boxplots on the same grid.
    
    Args:
        data: Single Series or list of Series to plot
        title: Plot title
        ylabel: Label for value axis
        horizontal: If True, plot horizontally
        labels: List of labels for multiple boxplots (optional)
    """
    # Handle single or multiple data series
    if isinstance(data, list):
        if len(data) == 0: raise ValueError("Input data is empty.")
        data_list = []
        for d in data:
            if not isinstance(d, pd.Series): d = pd.Series(d)
            numeric_data = pd.to_numeric(d, errors='coerce').dropna()
            if not numeric_data.empty:
                data_list.append(numeric_data.to_numpy())
        if not data_list: raise ValueError("No valid numerical data found in any of the provided datasets.")
    else:
        if data.size == 0: raise ValueError("Input data is empty.")
        if not isinstance(data, pd.Series): data = pd.Series(data)
        numeric_data = pd.to_numeric(data, errors='coerce').dropna()
        if numeric_data.empty: raise ValueError("Input data contains no valid numerical data for boxplot.")
        data_list = [numeric_data.to_numpy()]
    
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.boxplot(data_list, vert=not horizontal, labels=labels)
    ax.set_title(title)
    if horizontal:
        ax.set_xlabel(ylabel)
        if labels:
            ax.set_yticks(range(1, len(labels) + 1))
            ax.set_yticklabels(labels)
        ax.grid(axis='x', alpha=0.75)
    else:
        ax.set_ylabel(ylabel)
        if labels:
            ax.set_xticks(range(1, len(labels) + 1))
            ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    return fig

def plot_bar_plot(data, title='Bar Plot of Categories', xlabel='Category', ylabel='Frequency', stacked=False, use_relative=False):
    if data.empty: raise ValueError("Input data is empty.")
    if not isinstance(data, pd.Series): data = pd.Series(data)
    categorical_data = data.dropna()
    if categorical_data.empty: raise ValueError("Input data contains no valid categorical values after cleaning.")
    counts = categorical_data.value_counts()
    if counts.empty: raise ValueError("No categories found to plot after counting.")
    
    # Convert to relative frequency if requested
    if use_relative:
        values = counts / counts.sum()
        ylabel = 'Relative Frequency'
    else:
        values = counts
        ylabel = 'Frequency'
    
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    
    if stacked:
        # Create a single stacked bar
        bottom = 0
        colors = plt.cm.Set3(range(len(counts)))
        for i, (category, count) in enumerate(counts.items()):
            height = values.iloc[i] if use_relative else count
            ax.bar(0, height, bottom=bottom, color=colors[i], edgecolor='black', label=str(category))
            bottom += height
        ax.set_xlim(-0.5, 0.5)
        ax.set_xticks([0])
        ax.set_xticklabels(['All Categories'])
        ax.legend(title=xlabel, bbox_to_anchor=(1.05, 1), loc='upper left')
    else:
        # Unstacked (grouped) bars - original behavior
        x_labels = [str(x) for x in counts.index]
        x_positions = range(len(counts))
        
        # WCAG-compliant accessible teal
        ax.bar(x_positions, values.values, color='#029E73', edgecolor='black')
        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_labels, rotation=45, ha='right')
    
    ax.set_title(title)
    ax.set_xlabel(xlabel if not stacked else 'Categories')
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    return fig

def plot_dot_plot(data, title='Dot Plot', xlabel='Value', ylabel='', dot_spacing=0.1):
    if data.size == 0: raise ValueError("Input data is empty.")
    if not isinstance(data, pd.Series): data = pd.Series(data)
    numeric_data = pd.to_numeric(data, errors='coerce').dropna()
    if numeric_data.empty: raise ValueError("Input data contains no valid numerical values after cleaning.")

    # Sort data to ensure consistent stacking order for identical values
    sorted_values = np.sort(numeric_data.to_numpy())

    # Prepare x and y coordinates for scatter plot
    plot_x = []
    plot_y = []
    # Dictionary to keep track of counts for each unique value, for stacking
    value_counts = {}

    for val in sorted_values:
        if val not in value_counts:
            value_counts[val] = 0
        plot_x.append(val)
        plot_y.append(value_counts[val] * dot_spacing)
        value_counts[val] += 1

    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.scatter(plot_x, plot_y, alpha=0.7, s=50, edgecolors='w', linewidth=0.5)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_yticks([])  # Hide y-axis ticks as they represent stacking, not a continuous variable
    ax.grid(axis='x', alpha=0.75)
    plt.tight_layout()
    return fig

def plot_scatter_plot(x_data, y_data, title='Scatter Plot', xlabel='X-axis', ylabel='Y-axis'):
    if not isinstance(x_data, pd.Series): x_data = pd.Series(x_data)
    if not isinstance(y_data, pd.Series): y_data = pd.Series(y_data)

    if x_data.empty or y_data.empty: raise ValueError("Input data (after cleaning) is empty.")
    if len(x_data) != len(y_data): raise ValueError("x_data and y_data must have the same length.")

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.scatter(x_data.to_numpy(), y_data.to_numpy(), alpha=0.7, edgecolors='w', linewidth=0.5)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    plt.tight_layout()
    return fig
def perform_linear_regression_analysis(x_data, y_data, title='Linear Regression Analysis', xlabel='X-axis', ylabel='Y-axis'):
    if x_data.empty or y_data.empty: raise ValueError("Input data is empty after cleaning.")
    if len(x_data) != len(y_data): raise ValueError("X and Y data must have the same length after cleaning.")

    # Perform linear regression
    slope, intercept, r_value, p_value, stderr = stats.linregress(x_data.to_numpy(), y_data.to_numpy())
    r_squared = r_value**2
    regression_equation = f"Predicted {ylabel} = {intercept:.4f} + {slope:.4f} * {xlabel}"

    # Plot scatter with regression line
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.scatter(x_data.to_numpy(), y_data.to_numpy(), alpha=0.7, edgecolors='w', linewidth=0.5, label='Data Points')
    ax.plot(x_data.to_numpy(), slope * x_data.to_numpy() + intercept, color='red', label='Regression Line')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    return r_value, r_squared, regression_equation, fig

def ci_mean_sigma_known(sample_mean, pop_std_dev, sample_size, confidence_level):
    if not (0 < confidence_level < 1): raise ValueError("Confidence level must be between 0 and 1.")
    if pop_std_dev <= 0: raise ValueError("Population standard deviation must be positive.")
    if sample_size <= 0: raise ValueError("Sample size must be positive.")
    alpha = 1 - confidence_level
    z_critical = stats.norm.ppf(1 - alpha / 2)
    margin_of_error = z_critical * (pop_std_dev / np.sqrt(sample_size))
    return (sample_mean - margin_of_error, sample_mean + margin_of_error)

def ci_mean_sigma_unknown(sample_mean, sample_std_dev, sample_size, confidence_level):
    if not (0 < confidence_level < 1): raise ValueError("Confidence level must be between 0 and 1.")
    if sample_std_dev <= 0: raise ValueError("Sample standard deviation must be positive.")
    if sample_size <= 1: raise ValueError("Sample size must be greater than 1 for t-distribution.")
    alpha = 1 - confidence_level
    degrees_freedom = sample_size - 1
    t_critical = stats.t.ppf(1 - alpha / 2, df=degrees_freedom)
    margin_of_error = t_critical * (sample_std_dev / np.sqrt(sample_size))
    return (sample_mean - margin_of_error, sample_mean + margin_of_error)

def ci_proportion(num_successes, num_trials, confidence_level):
    if not (0 < confidence_level < 1): raise ValueError("Confidence level must be between 0 and 1.")
    if not isinstance(num_trials, int) or num_trials <= 0: raise ValueError("Number of trials must be a positive integer.")
    if not isinstance(num_successes, int) or not (0 <= num_successes <= num_trials): raise ValueError("Number of successes must be an integer between 0 and number of trials.")
    sample_proportion = num_successes / num_trials
    alpha = 1 - confidence_level
    z_critical = stats.norm.ppf(1 - alpha / 2)
    std_error = np.sqrt((sample_proportion * (1 - sample_proportion)) / num_trials)
    margin_of_error = z_critical * std_error
    lower_bound = max(0, sample_proportion - margin_of_error)
    upper_bound = min(1, sample_proportion + margin_of_error)
    return (lower_bound, upper_bound)

def ci_diff_means_sigma_known(sample_mean1, pop_std_dev1, sample_size1, sample_mean2, pop_std_dev2, sample_size2, confidence_level):
    if not (0 < confidence_level < 1): raise ValueError("Confidence level must be between 0 and 1.")
    if pop_std_dev1 <= 0 or pop_std_dev2 <= 0: raise ValueError("Population standard deviations must be positive.")
    if sample_size1 <= 0 or sample_size2 <= 0: raise ValueError("Sample sizes must be positive.")
    alpha = 1 - confidence_level
    z_critical = stats.norm.ppf(1 - alpha / 2)
    std_error_diff = np.sqrt((pop_std_dev1**2 / sample_size1) + (pop_std_dev2**2 / sample_size2))
    margin_of_error = z_critical * std_error_diff
    difference_of_means = sample_mean1 - sample_mean2
    return (difference_of_means - margin_of_error, difference_of_means + margin_of_error)

def ci_diff_means_sigma_unknown_equal_var(sample_mean1, sample_std_dev1, sample_size1, sample_mean2, sample_std_dev2, sample_size2, confidence_level):
    if not (0 < confidence_level < 1): raise ValueError("Confidence level must be between 0 and 1.")
    if sample_std_dev1 < 0 or sample_std_dev2 < 0: raise ValueError("Sample standard deviations cannot be negative.")
    if sample_size1 <= 1 or sample_size2 <= 1: raise ValueError("Sample sizes must be greater than 1 for t-distribution.")
    alpha = 1 - confidence_level
    # Corrected pooled standard deviation formula
    pooled_std_dev = np.sqrt(((sample_size1 - 1) * sample_std_dev1**2 + (sample_size2 - 1) * sample_std_dev2**2) / (sample_size1 + sample_size2 - 2))
    degrees_freedom = sample_size1 + sample_size2 - 2
    if degrees_freedom <= 0: raise ValueError("Degrees of freedom must be positive.")
    t_critical = stats.t.ppf(1 - alpha / 2, df=degrees_freedom)
    margin_of_error = t_critical * (pooled_std_dev * np.sqrt((1 / sample_size1) + (1 / sample_size2)))
    difference_of_means = sample_mean1 - sample_mean2
    return (difference_of_means - margin_of_error, difference_of_means + margin_of_error)

def ci_diff_means_sigma_unknown_unequal_var(sample_mean1, sample_std_dev1, sample_size1, sample_mean2, sample_std_dev2, sample_size2, confidence_level):
    if not (0 < confidence_level < 1): raise ValueError("Confidence level must be between 0 and 1.")
    if sample_std_dev1 < 0 or sample_std_dev2 < 0: raise ValueError("Sample standard deviations cannot be negative.")
    if sample_size1 <= 1 or sample_size2 <= 1: raise ValueError("Sample sizes must be greater than 1 for t-distribution.")
    alpha = 1 - confidence_level
    se1_sq = (sample_std_dev1**2) / sample_size1
    se2_sq = (sample_std_dev2**2) / sample_size2
    numerator = (se1_sq + se2_sq)**2
    denominator = (se1_sq**2 / (sample_size1 - 1)) + (se2_sq**2 / (sample_size2 - 1))
    degrees_freedom = numerator / denominator
    if degrees_freedom <= 0: raise ValueError("Degrees of freedom must be positive.")
    t_critical = stats.t.ppf(1 - alpha / 2, df=degrees_freedom)
    std_error_diff = np.sqrt(se1_sq + se2_sq)
    margin_of_error = t_critical * std_error_diff
    difference_of_means = sample_mean1 - sample_mean2
    return (difference_of_means - margin_of_error, difference_of_means + margin_of_error)

def ci_diff_proportions(num_successes1, num_trials1, num_successes2, num_trials2, confidence_level):
    if not (0 < confidence_level < 1): raise ValueError("Confidence level must be between 0 and 1.")
    if not isinstance(num_trials1, int) or num_trials1 <= 0: raise ValueError("Number of trials for sample 1 must be a positive integer.")
    if not isinstance(num_successes1, int) or not (0 <= num_successes1 <= num_trials1): raise ValueError("Number of successes for sample 1 must be an integer between 0 and number of trials.")
    if not isinstance(num_trials2, int) or num_trials2 <= 0: raise ValueError("Number of trials for sample 2 must be a positive integer.")
    if not isinstance(num_successes2, int) or not (0 <= num_successes2 <= num_trials2): raise ValueError("Number of successes for sample 2 must be an integer between 0 and number of trials.")
    prop1 = num_successes1 / num_trials1
    prop2 = num_successes2 / num_trials2
    alpha = 1 - confidence_level
    z_critical = stats.norm.ppf(1 - alpha / 2)
    std_error_diff = np.sqrt(
        (prop1 * (1 - prop1) / num_trials1) +
        (prop2 * (1 - prop2) / num_trials2)
    )
    margin_of_error = z_critical * std_error_diff
    difference_of_proportions = prop1 - prop2
    lower_bound = max(-1, difference_of_proportions - margin_of_error)
    upper_bound = min(1, difference_of_proportions + margin_of_error)
    return (lower_bound, upper_bound)

def ci_paired_differences(sample1_data, sample2_data, confidence_level):
    if not (0 < confidence_level < 1): raise ValueError("Confidence level must be between 0 and 1.")
    if len(sample1_data) != len(sample2_data): raise ValueError("Samples must be of equal length for paired differences.")
    if len(sample1_data) <= 1: raise ValueError("Sample size must be greater than 1 for paired t-distribution.")
    differences = np.array(sample1_data) - np.array(sample2_data)
    diff_mean = np.mean(differences)
    diff_std = np.std(differences, ddof=1) # ddof=1 for sample standard deviation
    sample_size = len(differences)
    if diff_std <= 0 and sample_size > 1:
        if np.all(differences == differences[0]): return (diff_mean, diff_mean)
        else: raise ValueError("Calculated standard deviation of differences is non-positive but not all differences are the same.")
    alpha = 1 - confidence_level
    degrees_freedom = sample_size - 1
    t_critical = stats.t.ppf(1 - alpha / 2, df=degrees_freedom)
    margin_of_error = t_critical * (diff_std / np.sqrt(sample_size))
    return (diff_mean - margin_of_error, diff_mean + margin_of_error)

def ci_paired_differences_summary(mean_difference, std_dev_difference, sample_size_difference, confidence_level):
    if not (0 < confidence_level < 1): raise ValueError("Confidence level must be between 0 and 1.")
    if std_dev_difference <= 0: raise ValueError("Standard deviation of differences must be positive.")
    if sample_size_difference <= 1: raise ValueError("Number of pairs must be greater than 1 for paired t-distribution.")
    alpha = 1 - confidence_level
    degrees_freedom = sample_size_difference - 1
    t_critical = stats.t.ppf(1 - alpha / 2, df=degrees_freedom)
    margin_of_error = t_critical * (std_dev_difference / np.sqrt(sample_size_difference))
    return (mean_difference - margin_of_error, mean_difference + margin_of_error)

# --- Hypothesis Testing Functions ---
def _get_p_value_from_statistic(statistic, df, alternative, dist_type='t'):
    """Helper to calculate p-value based on alternative hypothesis."""
    if dist_type == 't':
        if alternative == 'two-sided':
            p_value = stats.t.sf(np.abs(statistic), df=df) * 2
        elif alternative == 'greater':
            p_value = stats.t.sf(statistic, df=df)
        elif alternative == 'less':
            p_value = stats.t.cdf(statistic, df=df)
        else:
            raise ValueError("Invalid alternative for t-test.")
    elif dist_type == 'norm': # For Z-tests
        if alternative == 'two-sided':
            p_value = stats.norm.sf(np.abs(statistic)) * 2
        elif alternative == 'greater':
            p_value = stats.norm.sf(statistic)
        elif alternative == 'less':
            p_value = stats.norm.cdf(statistic)
        else:
            raise ValueError("Invalid alternative for Z-test.")
    else:
        raise ValueError("Unsupported distribution type for p-value calculation.")
    return p_value

def one_sample_t_test(sample_data, hypothesized_mean, alternative='two-sided'):
    if len(sample_data) < 2: raise ValueError("Sample data must have at least 2 observations.")
    t_statistic, p_value = stats.ttest_1samp(a=sample_data, popmean=hypothesized_mean, alternative=alternative)
    return t_statistic, p_value

def one_sample_t_test_summary(sample_mean, sample_std_dev, sample_size, hypothesized_mean, alternative='two-sided'):
    if sample_size < 2: raise ValueError("Sample size must be at least 2.")
    t_statistic = (sample_mean - hypothesized_mean) / (sample_std_dev / np.sqrt(sample_size))
    df = sample_size - 1
    p_value = _get_p_value_from_statistic(t_statistic, df, alternative, dist_type='t')
    return t_statistic, p_value

def two_sample_t_test_independent(sample_data1, sample_data2, equal_variances=True, alternative='two-sided'):
    if len(sample_data1) < 2 or len(sample_data2) < 2: raise ValueError("Both sample data sets must have at least 2 observations.")
    t_statistic, p_value = stats.ttest_ind(a=sample_data1, b=sample_data2, equal_var=equal_variances, alternative=alternative)
    return t_statistic, p_value

def two_sample_t_test_independent_summary(sample1_mean, sample1_std_dev, sample1_size, sample2_mean, sample2_std_dev, sample2_size, equal_variances=True, alternative='two-sided'):
    if sample1_size < 2 or sample2_size < 2: raise ValueError("Sample sizes must be at least 2.")

    if equal_variances:
        # Pooled variance
        s_p_squared = ((sample1_size - 1) * sample1_std_dev**2 + (sample2_size - 1) * sample2_std_dev**2) / (sample1_size + sample2_size - 2)
        t_statistic = (sample1_mean - sample2_mean) / np.sqrt(s_p_squared * (1/sample1_size + 1/sample2_size))
        df = sample1_size + sample2_size - 2
    else:
        # Welch's t-test (unequal variances)
        se1_squared = sample1_std_dev**2 / sample1_size
        se2_squared = sample2_std_dev**2 / sample2_size
        t_statistic = (sample1_mean - sample2_mean) / np.sqrt(se1_squared + se2_squared)
        df = (se1_squared + se2_squared)**2 / ((se1_squared**2 / (sample1_size - 1)) + (se2_squared**2 / (sample2_size - 1)))

    p_value = _get_p_value_from_statistic(t_statistic, df, alternative, dist_type='t')
    return t_statistic, p_value

def paired_t_test(sample_data1, sample_data2, alternative='two-sided'):
    if len(sample_data1) != len(sample_data2): raise ValueError("Sample data must be of equal length for a paired t-test.")
    if len(sample_data1) < 2: raise ValueError("Sample data must have at least 2 observations.")
    t_statistic, p_value = stats.ttest_rel(a=sample_data1, b=sample_data2, alternative=alternative)
    return t_statistic, p_value

def paired_t_test_summary(mean_difference, std_dev_difference, sample_size_difference, alternative='two-sided'):
    if sample_size_difference < 2: raise ValueError("Number of pairs must be at least 2.")
    t_statistic = mean_difference / (std_dev_difference / np.sqrt(sample_size_difference))
    df = sample_size_difference - 1
    p_value = _get_p_value_from_statistic(t_statistic, df, alternative, dist_type='t')
    return t_statistic, p_value

def one_sample_z_test_proportion(num_successes, num_trials, hypothesized_proportion, alternative='two-sided'):
    if num_trials <= 0: raise ValueError("Number of trials must be a positive integer.")
    if not (0 <= num_successes <= num_trials): raise ValueError("Number of successes must be an integer between 0 and number of trials.")
    if not (0 <= hypothesized_proportion <= 1): raise ValueError("Hypothesized proportion must be between 0 and 1.")
    sample_proportion = num_successes / num_trials
    se_p0 = np.sqrt((hypothesized_proportion * (1 - hypothesized_proportion)) / num_trials)
    if se_p0 == 0: z_statistic = np.inf if sample_proportion != hypothesized_proportion else 0.0
    else: z_statistic = (sample_proportion - hypothesized_proportion) / se_p0
    p_value = _get_p_value_from_statistic(z_statistic, None, alternative, dist_type='norm')
    return z_statistic, p_value

def two_sample_z_test_proportion(num_successes1, num_trials1, num_successes2, num_trials2, alternative='two-sided'):
    if num_trials1 <= 0 or num_trials2 <= 0: raise ValueError("Number of trials must be positive for both samples.")
    if not (0 <= num_successes1 <= num_trials1) or not (0 <= num_successes2 <= num_trials2): raise ValueError("Number of successes must be valid for both samples.")
    prop1 = num_successes1 / num_trials1
    prop2 = num_successes2 / num_trials2
    pooled_prop = (num_successes1 + num_successes2) / (num_trials1 + num_trials2)
    se_diff_pooled = np.sqrt(pooled_prop * (1 - pooled_prop) * ((1 / num_trials1) + (1 / num_trials2)))
    if se_diff_pooled == 0: z_statistic = np.inf if prop1 != prop2 else 0.0
    else: z_statistic = (prop1 - prop2) / se_diff_pooled
    p_value = _get_p_value_from_statistic(z_statistic, None, alternative, dist_type='norm')
    return z_statistic, p_value

def chi_square_goodness_of_fit_test(observed_frequencies, expected_frequencies=None):
    observed = np.array([float(x) for x in observed_frequencies])
    if expected_frequencies is not None and len(expected_frequencies) > 0:
        expected = np.array([float(x) for x in expected_frequencies])
        if len(observed) != len(expected): raise ValueError("Observed and expected frequencies must have the same length.")
    else:
        expected = np.full_like(observed, fill_value=np.sum(observed) / len(observed), dtype=float)
    if not np.all(observed >= 0): raise ValueError("Observed frequencies must be non-negative.")
    if not np.all(expected >= 0): raise ValueError("Expected frequencies must be non-negative.")
    if np.sum(observed) == 0: raise ValueError("Sum of observed frequencies cannot be zero.")
    if np.sum(expected) == 0: raise ValueError("Sum of expected frequencies cannot be zero.")
    chi2_statistic, p_value = stats.chisquare(f_obs=observed, f_exp=expected)
    return chi2_statistic, p_value

def chi_square_test_of_independence(contingency_table):
    table = np.array(contingency_table)
    if table.ndim != 2: raise ValueError("Contingency table must be a 2D array.")
    if table.size == 0: raise ValueError("Contingency table cannot be empty.")
    if not np.all(table >= 0): raise ValueError("Frequencies in the contingency table must be non-negative.")
    chi2_statistic, p_value, degrees_freedom, expected_frequencies = stats.chi2_contingency(table)
    return chi2_statistic, p_value, degrees_freedom, expected_frequencies

def anova_f_test(*sample_data_groups):
    if len(sample_data_groups) < 2: raise ValueError("ANOVA requires at least two sample groups.")
    for i, group in enumerate(sample_data_groups):
        if not isinstance(group, (list, np.ndarray, pd.Series)) or len(group) < 2:
            raise ValueError(f"Sample group {i+1} must be an array-like object with at least 2 observations.")
    f_statistic, p_value = stats.f_oneway(*sample_data_groups)
    return f_statistic, p_value

# --- Sidebar for Navigation ---
nav_options = ["Data Input", "Visualizations", "Tables", "Descriptive Statistics", "Probability Distributions", "Confidence Intervals", "Hypothesis Testing", "Linear Regression", "Simulations", "Start New Session"]

# Check if we need to force navigation to Data Input
if st.session_state.get('_force_data_input', False):
    # Clear the flag and force navigation
    del st.session_state._force_data_input
    # Clear the navigation key so it resets
    if 'navigation_radio' in st.session_state:
        del st.session_state.navigation_radio
    selected_tab = st.sidebar.radio("Navigation", nav_options, index=0)
    # Override selected_tab to Data Input
    selected_tab = "Data Input"
else:
    selected_tab = st.sidebar.radio("Navigation", nav_options, key="navigation_radio")

# Handle Start New Session
if selected_tab == "Start New Session":
    st.header("Start New Session")
    st.warning("⚠️ This will clear all data and reset the application to its initial state.")
    st.write("**The following will be cleared:**")
    st.write("- All uploaded and manually entered data")
    st.write("- All session state and saved parameters")
    st.write("- All analysis results")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🔄 Reset Everything", type="primary", use_container_width=True):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            # Reinitialize essential session state
            st.session_state.global_dataframes = {}
            st.session_state.manual_entry_df = pd.DataFrame({'Column A': ['']})
            # Set flag to force navigation to Data Input
            st.session_state._force_data_input = True
            st.rerun()
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            # Set flag to force navigation to Data Input without clearing data
            st.session_state._force_data_input = True
            st.rerun()
    
    st.stop()  # Stop execution so no other tab content is shown

# Toggle: choose between interactive Streamlit tables or styled HTML tables
use_interactive_tables = st.sidebar.checkbox("Use interactive tables (st.dataframe)", value=False, key="use_interactive_tables")


def show_table(df, hide_index=False):
    """Display a DataFrame using either `st.dataframe` (interactive) or styled HTML.

    Respects the `use_interactive_tables` sidebar checkbox.
    """
    try:
        if use_interactive_tables:
            st.dataframe(df, hide_index=hide_index)
        else:
            st.markdown(styled_dataframe_html(df, hide_index=hide_index), unsafe_allow_html=True)
    except Exception:
        # Fallback to a simple write if both methods fail
        try:
            st.dataframe(df, hide_index=hide_index)
        except Exception:
            st.write(df)


# Compatibility helper: some Streamlit versions expose `experimental_rerun`,
# others provide `rerun`. Use a small wrapper to call whichever exists.
def safe_rerun():
    try:
        # Prefer experimental_rerun when available
        rerun_fn = getattr(st, "experimental_rerun", None)
        if callable(rerun_fn):
            rerun_fn()
            return
        # Fallback to older API
        rerun_fn = getattr(st, "rerun", None)
        if callable(rerun_fn):
            rerun_fn()
            return
    except Exception:
        try:
            logging.exception("safe_rerun failed to call Streamlit rerun function")
        except Exception:
            pass

# --- Main Content Area ---

if selected_tab == "Data Input":
    st.header("Data Input")

    # Create tabs for different input methods
    input_method = st.radio(
        "Choose Data Input Method:",
        options=["Upload File", "Google Sheets", "Manual Entry"],
        horizontal=True,
        key="data_input_method"
    )

    if input_method == "Upload File":
        st.subheader("Upload Data File")
        uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
    elif input_method == "Google Sheets":
        st.subheader("Import from Google Sheets")
        st.markdown("""
        <div role="region" aria-label="Google Sheets Import Instructions">
        <strong>Instructions for Publishing Your Google Sheet:</strong>
        <ol>
        <li>Open your Google Sheet in a web browser</li>
        <li>Click <strong>File</strong> menu, then <strong>Share</strong>, then <strong>Publish to web</strong></li>
        <li>In the dialog, choose <strong>Entire Document</strong> (or select a specific sheet)</li>
        <li>For the format dropdown, select <strong>Comma-separated values (.csv)</strong></li>
        <li>Click the <strong>Publish</strong> button and confirm</li>
        <li>Copy the generated link (it will look like: https://docs.google.com/spreadsheets/d/e/...)</li>
        <li>Paste the link in the field below</li>
        </ol>
        <p><strong>Note:</strong> The sheet must be published as CSV format, not as a web page.</p>
        </div>
        """, unsafe_allow_html=True)
        
        sheets_url = st.text_input(
            "Google Sheets URL * (Required)",
            placeholder="Example: https://docs.google.com/spreadsheets/d/e/2PACX-1vS...",
            help="Paste the CSV link you copied from 'Publish to web'. Must end with /pub?output=csv or similar.",
            key="google_sheets_url_input"
        )
        
        if st.button("Load from Google Sheets", key="load_sheets_btn", help="Click to import data from the URL above"):
            if sheets_url:
                with st.spinner("Loading data from Google Sheets..."):
                    try:
                        # Read CSV directly from the published URL
                        df = pd.read_csv(sheets_url)
                        
                        if df is not None and not df.empty:
                            # Reset index to start at 1 instead of 0
                            df.index = range(1, len(df) + 1)
                            df.index.name = None
                            # Replace any existing dataframe with the new one
                            st.session_state.global_dataframes = {'active_data': df}
                            st.success(f"✅ Successfully loaded data from Google Sheets! Loaded {len(df)} rows and {len(df.columns)} columns.")
                            st.write("**Preview of Loaded Data:**")
                            show_table(df)
                            
                            # Reset manual entry if Google Sheets is loaded
                            st.session_state.manual_entry_df = pd.DataFrame({'Column A': ['']})
                        else:
                            st.error("❌ Error: The Google Sheet appears to be empty. Please check that your sheet contains data and try again.")
                    except pd.errors.ParserError as pe:
                        st.error(f"❌ Error: Unable to parse the data from Google Sheets. {pe}")
                        st.info("💡 **How to fix:** Make sure you published the sheet as 'Comma-separated values (.csv)' format, not as a web page or other format.")
                    except Exception as e:
                        st.error(f"❌ Error loading Google Sheets: {e}")
                        st.info("""
                        💡 **Troubleshooting steps:**
                        - Verify the sheet is published to the web (File → Share → Publish to web)
                        - Ensure you selected 'Comma-separated values (.csv)' as the format
                        - Check that the URL starts with https://docs.google.com/spreadsheets/
                        - Make sure the sheet is not restricted or private
                        - Try copying the publish link again
                        """)
            else:
                st.warning("⚠️ Required field: Please enter a Google Sheets URL in the field above before clicking Load.")
        uploaded_file = None  # Set to None so file upload logic doesn't run
    else:  # Manual Entry
        uploaded_file = None  # Set to None so file upload logic doesn't run

    if input_method == "Upload File":
        uploaded_file_original = uploaded_file  # Store for later reference
    else:
        uploaded_file = None

    if uploaded_file is not None:
        try:
            file_name = uploaded_file.name
            file_extension = file_name.split('.')[-1].lower()
            df = None

            if file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_extension == 'xlsx':
                df = pd.read_excel(uploaded_file)

            if df is not None:
                # Reset index to start at 1 instead of 0
                df.index = range(1, len(df) + 1)
                df.index.name = None  # Set to None to avoid showing "None" header
                # Replace any existing dataframe with the new one
                st.session_state.global_dataframes = {'active_data': df}
                st.success(f"Successfully uploaded and processed '{file_name}'. This replaces any previously loaded data.")
                st.write("Uploaded data:")
                show_table(df)

                # --- Allow inline header renaming for the uploaded DataFrame ---
                try:
                    st.markdown("**Edit Column Names for Uploaded Data**")
                    header_valid = True
                    new_header_names = []
                    if df is not None and not df.empty:
                        header_cols = st.columns(len(df.columns))
                        for i, col in enumerate(df.columns):
                            with header_cols[i]:
                                new_name = st.text_input(f"Column {i+1}", value=col, key=f"upload_header_input_active_{i}", label_visibility="collapsed")
                            new_header_names.append(new_name.strip())

                        # Validate header names
                        empty_headers = [i+1 for i, n in enumerate(new_header_names) if n == ""]
                        seen = {}
                        duplicate_headers = []
                        for i, n in enumerate(new_header_names):
                            if n in seen:
                                duplicate_headers.extend([seen[n]+1, i+1])
                            else:
                                seen[n] = i
                        duplicate_headers = sorted(list(set(duplicate_headers)))

                        if empty_headers or duplicate_headers:
                            header_valid = False
                            if empty_headers:
                                st.error(f"Column name(s) cannot be empty. Check column(s): {', '.join(map(str, empty_headers))}.")
                            if duplicate_headers:
                                st.error(f"Duplicate column name(s) detected for columns: {', '.join(map(str, duplicate_headers))}. Please use unique names.")
                        else:
                            if new_header_names != list(df.columns):
                                rename_map = {old: new for old, new in zip(df.columns, new_header_names) if new and new != old}
                                if rename_map:
                                    try:
                                        st.session_state.global_dataframes['active_data'] = df.rename(columns=rename_map)
                                        df = st.session_state.global_dataframes['active_data']
                                        st.success("Applied column name changes to uploaded data.")
                                    except Exception:
                                        st.warning("Could not apply header rename changes.")
                    else:
                        df = st.session_state.global_dataframes.get('active_data', df)

                    # Persist header validity flag for this uploaded dataset
                    st.session_state['header_valid_active'] = header_valid
                except Exception:
                    st.warning("Header rename UI unavailable for this upload.")

                # Reset manual entry if a file is uploaded, as it's separate data
                st.session_state.manual_entry_df = pd.DataFrame({'Column A': ['']})
            else:
                st.error(f"Unsupported file type: {file_extension}")
        except Exception as e:
            st.error(f"Error processing file: {e}")

    if input_method == "Manual Entry":
        st.subheader("Manual Data Entry")
        
        # Initialize with one row if empty
        if 'table_data' not in st.session_state:
            st.session_state.table_data = pd.DataFrame({'Column 1': ['']})
        
        # Check if clear action was triggered
        if st.session_state.get('clear_all_triggered', False):
            st.session_state.table_data = pd.DataFrame({'Column 1': ['']})
            st.session_state.clear_all_triggered = False
        
        # This is our working copy that persists across reruns
        table_data = st.session_state.table_data
    
        # Editable column headers
        st.markdown("**Click column name to edit:**")
        header_cols = st.columns(len(table_data.columns))
        new_header_names = []
        for i, col in enumerate(table_data.columns):
            with header_cols[i]:
                if f'editing_col_{i}' not in st.session_state:
                    st.session_state[f'editing_col_{i}'] = False
            
                if st.session_state[f'editing_col_{i}']:
                    new_name = st.text_input(f"Edit Column {i+1} Name", value=col, key=f"header_input_{i}", label_visibility="collapsed")
                    if st.button("✓", key=f"save_header_{i}"):
                        st.session_state[f'editing_col_{i}'] = False
                        if new_name.strip() and new_name.strip() not in [c for j, c in enumerate(table_data.columns) if j != i]:
                            new_header_names.append(new_name.strip())
                        else:
                            new_header_names.append(col)
                            if not new_name.strip():
                                st.warning("Column name cannot be empty.")
                            else:
                                st.warning("Column name must be unique.")
                    else:
                        new_header_names.append(col)
                else:
                    if st.button(col, key=f"edit_header_{i}"):
                        st.session_state[f'editing_col_{i}'] = True
                    new_header_names.append(col)
    
        # Apply renamed headers if changed
        if new_header_names != list(table_data.columns) and len(new_header_names) == len(table_data.columns):
            rename_map = {old: new for old, new in zip(table_data.columns, new_header_names) if new != old}
            if rename_map:
                table_data = table_data.rename(columns=rename_map)
                st.session_state.table_data = table_data
                safe_rerun()
    
        # Data editor with automatic new row on Enter
        st.markdown("**Enter data below:**")
        st.markdown("""
        <div role="region" aria-label="Manual Data Entry Grid">
        <p id="data-editor-help">💡 Tip: Type in the table and use Tab to navigate between cells. 
        Click the '+' icon at the bottom of the table to add rows. Use the trash icon to delete rows.</p>
        </div>
        """, unsafe_allow_html=True)
    
        # Use data editor with dynamic rows - this allows adding/removing rows
        # Reset index to avoid warnings with hide_index
        # Create a copy with 1-based index for display
        display_df = table_data.copy()
        display_df.index = range(1, len(display_df) + 1)
    
        edited_df = st.data_editor(
            display_df,
            num_rows="dynamic",
            width="stretch",
            key="data_editor",
            hide_index=True,  # Hide index to avoid "None" issue when adding rows
        )
    
        # Keep 1-based index for consistency with uploaded data
        if edited_df is not None and len(edited_df) > 0:
            edited_df.index = range(1, len(edited_df) + 1)
            edited_df.index.name = None  # Set to None to avoid showing "None" header

        # DO NOT update session state here - it causes reruns that erase data
        # The data_editor widget manages its own state via the key
        # We'll only sync to session state when needed (buttons) or when processing
    
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("Add Column", key="add_col_btn"):
                new_col_num = len(edited_df.columns) + 1
                new_col_name = f"Column {new_col_num}"
                while new_col_name in edited_df.columns:
                    new_col_num += 1
                    new_col_name = f"Column {new_col_num}"
                edited_df[new_col_name] = ""
                # Update our persistent table_data
                st.session_state.table_data = edited_df
                st.rerun()
    
        with col2:
            if st.button("Clear All", key="clear_all_btn_unique"):
                # Set flag to clear on next render
                st.session_state.clear_all_triggered = True
                st.rerun()

    
        # Process button
        if st.button("Process Manual Entry Data"):
            # Get the current data from the editor (stored by its key in session state)
            # The data_editor stores its state under the key we provided
            table_data = edited_df if edited_df is not None else pd.DataFrame()
        
            if not table_data.empty:
                # Remove completely empty rows
                cleaned_data = table_data.dropna(how='all')
                if not cleaned_data.empty:
                    try:
                        processed_manual_df = process_manual_entry_data(cleaned_data)
                        # Keep 1-based index for consistency with uploaded data
                        processed_manual_df.index = range(1, len(processed_manual_df) + 1)
                        processed_manual_df.index.name = None  # Set to None to avoid showing "None" header
                        # Replace any existing dataframe with the manual entry data
                        st.session_state.global_dataframes = {'active_data': processed_manual_df}
                        st.success("Manual entry data processed and stored. This replaces any previously loaded data.")
                        st.write("Processed Manual Entry Data:")
                        show_table(processed_manual_df)
                    except Exception as e:
                        st.error(f"Error processing manual entry data: {e}")
                else:
                    st.warning("Manual entry table is empty. Please add some data.")
            else:
                st.warning("Manual entry table is empty. Please add some data.")

    # Display currently loaded dataframe
    st.subheader("Current Data:")
    if st.session_state.global_dataframes and 'active_data' in st.session_state.global_dataframes:
        df = st.session_state.global_dataframes['active_data']
        st.write(f"**Active Dataset** ({df.shape[0]} rows, {df.shape[1]} columns)")
        show_table(df)
    else:
        st.info("No dataframes loaded yet.")

elif selected_tab == "Tables":
    st.header("Tables")

    if not st.session_state.global_dataframes or 'active_data' not in st.session_state.global_dataframes:
        st.info("Please load or enter data in the 'Data Input' tab first.")
    else:
        df = st.session_state.global_dataframes['active_data']
        
        table_type = st.selectbox(
            "Select Table Type",
            ["Frequency Table", "Relative Frequency Table", "Two-Way Table"],
            key="table_type_select"
        )

        if table_type in ["Frequency Table", "Relative Frequency Table"]:
            st.subheader(table_type)
            
            # Get only categorical columns (non-numeric or numeric with few unique values)
            categorical_cols_options = ['']
            for col in df.columns:
                # Consider a column categorical if it's non-numeric or has 15 or fewer unique values
                try:
                    pd.to_numeric(df[col], errors='raise')
                    # It's numeric - check unique count
                    if df[col].nunique() <= 15:
                        categorical_cols_options.append(col)
                except (ValueError, TypeError):
                    # It's non-numeric (categorical)
                    categorical_cols_options.append(col)
            
            selected_col = st.selectbox(
                "Select Categorical Column for Table",
                options=categorical_cols_options,
                key="table_column_select"
            )

            if selected_col and st.button("Generate Table", key="generate_freq_table"):
                try:
                    # Get the column data and drop NaN values
                    data = df[selected_col].dropna()
                    
                    if data.empty:
                        raise ValueError(f"Column '{selected_col}' is empty after removing missing values.")
                    
                    # Count frequencies
                    frequency_counts = data.value_counts().sort_index()
                    total_count = len(data)
                    
                    if table_type == "Frequency Table":
                        # Create frequency table without cumulative column
                        freq_table = pd.DataFrame({
                            'Category': frequency_counts.index,
                            'Frequency': frequency_counts.values
                        })
                        # Add total row
                        total_row = pd.DataFrame({'Category': ['Total'], 'Frequency': [total_count]})
                        freq_table = pd.concat([freq_table, total_row], ignore_index=True)
                        
                        st.write(f"**Frequency Table for '{selected_col}'**")
                        show_table(freq_table, hide_index=True)
                        st.caption(f"Frequency table showing counts for each category in {selected_col}. Total observations: {total_count}.")
                        
                    else:  # Relative Frequency Table
                        # Create relative frequency table without cumulative column
                        rel_freq_table = pd.DataFrame({
                            'Category': frequency_counts.index,
                            'Frequency': frequency_counts.values,
                            'Relative Frequency': (frequency_counts.values / total_count).round(4),
                            'Percentage': ((frequency_counts.values / total_count) * 100).round(2)
                        })
                        # Add total row
                        total_row = pd.DataFrame({
                            'Category': ['Total'], 
                            'Frequency': [total_count],
                            'Relative Frequency': [1.0000],
                            'Percentage': [100.00]
                        })
                        rel_freq_table = pd.concat([rel_freq_table, total_row], ignore_index=True)
                        
                        st.write(f"**Relative Frequency Table for '{selected_col}'**")
                        show_table(rel_freq_table, hide_index=True)
                        st.caption(f"Relative frequency table showing proportions and percentages for each category in {selected_col}. Total observations: {total_count}.")

                except ValueError as ve:
                    st.error(f"⚠️ Error: {ve}. Please check that you've selected a valid column with data.")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {e}. Please try selecting a different column or reloading your data.")

        elif table_type == "Two-Way Table":
            st.subheader("Two-Way Contingency Table")
            
            # Get only categorical columns
            categorical_cols_options = ['']
            for col in df.columns:
                try:
                    pd.to_numeric(df[col], errors='raise')
                    if df[col].nunique() <= 15:
                        categorical_cols_options.append(col)
                except (ValueError, TypeError):
                    categorical_cols_options.append(col)
            
            col1, col2 = st.columns(2)
            with col1:
                row_col = st.selectbox("Select Row Variable", options=categorical_cols_options, key="twoway_row_select")
            with col2:
                col_col = st.selectbox("Select Column Variable", options=categorical_cols_options, key="twoway_col_select")

            if row_col and col_col and st.button("Generate Two-Way Table", key="generate_twoway_table"):
                try:
                    # Create contingency table
                    contingency_table = pd.crosstab(
                        df[row_col], 
                        df[col_col], 
                        margins=True, 
                        margins_name='Total'
                    )
                    
                    # Remove variable names from index and columns
                    contingency_table.index.name = None
                    contingency_table.columns.name = None
                    
                    st.write(f"**Two-Way Frequency Table**")
                    show_table(contingency_table)
                    st.caption(f"Two-way frequency table showing counts for combinations of {row_col} (rows) and {col_col} (columns).")

                except ValueError as ve:
                    st.error(f"⚠️ Error: {ve}. Please ensure both variables are selected and contain valid categorical data.")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {e}. Please verify your column selections and data format.")

elif selected_tab == "Descriptive Statistics":
    st.header("Descriptive Statistics")

    if not st.session_state.global_dataframes or 'active_data' not in st.session_state.global_dataframes:
        st.info("Please load or enter data in the 'Data Input' tab first.")
    else:
        selected_df = st.session_state.global_dataframes['active_data']

        # Filter for numeric columns
        numeric_cols = selected_df.select_dtypes(include=np.number).columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns found in the active dataset. Please ensure your data contains numeric values.")
        else:
            multiple_columns = st.checkbox("Select multiple columns", value=False, key="descriptive_multiple_cols")
            
            if multiple_columns:
                selected_columns = st.multiselect(
                    "Select Columns * (Required)", 
                    options=numeric_cols, 
                    key="descriptive_col_multiselect",
                    help="Choose one or more numeric columns to analyze"
                )
            else:
                selected_column = st.selectbox(
                    "Select a Column * (Required)", 
                    options=[''] + numeric_cols, 
                    key="descriptive_col_select",
                    help="Choose a numeric column to analyze"
                )
                selected_columns = [selected_column] if selected_column else []

            if not selected_columns:
                st.info("👆 Please select at least one column above to begin analysis")
            
            if selected_columns:
                # Define all available statistics
                all_stats = [
                    'n', 'Mean', 'Median', 'Mode',
                    'Standard Deviation (s)', 'Variance', 'Range',
                    'Min Value', 'Max Value',
                    'Q1 (25th Percentile)', 'Q3 (75th Percentile)', 'IQR',
                    'Skewness', 'Kurtosis'
                ]
                
                # Let users select which statistics to display using checkboxes
                st.markdown("**Select Statistics to Display:**")
                
                # Create checkboxes in a compact grid layout
                cols = st.columns(3)
                selected_stats = []
                
                for idx, stat in enumerate(all_stats):
                    col_idx = idx % 3
                    with cols[col_idx]:
                        if st.checkbox(stat, value=False, key=f"stat_checkbox_{stat}"):
                            selected_stats.append(stat)
                
                if st.button("Calculate Descriptive Statistics", key="calc_descriptive_stats"):
                    if not selected_stats:
                        st.warning("⚠️ Please select at least one statistic from the checkboxes above to display results.")
                    else:
                        # Create a dictionary to store all columns' statistics
                        all_columns_stats = {}
                        has_error = False
                        
                        # Process each selected column
                        for column in selected_columns:
                            data_for_analysis = selected_df[column].dropna()
                            if data_for_analysis.empty:
                                st.warning(f"Column '{column}' is empty or contains no valid numeric data after dropping NaNs.")
                                has_error = True
                            else:
                                stats_results = calculate_descriptive_statistics(data_for_analysis)
                                if "Error" in stats_results:
                                    st.error(f"Error in column '{column}': {stats_results['Error']}")
                                    has_error = True
                                else:
                                    # Filter results based on selected statistics
                                    filtered_stats = {k: v for k, v in stats_results.items() if k in selected_stats}
                                    all_columns_stats[column] = filtered_stats
                        
                        # If we have valid statistics for at least one column, display the combined table
                        if all_columns_stats:
                            st.subheader("Descriptive Statistics Results")
                            
                            # Create a combined DataFrame with statistics as rows and columns as columns
                            # Start with the statistic names as the index
                            combined_df = pd.DataFrame(index=selected_stats)
                            combined_df.index.name = None
                            
                            # Add each column's statistics
                            for column_name, stats_dict in all_columns_stats.items():
                                # Create a column with the statistics values
                                column_values = [stats_dict.get(stat, '') for stat in selected_stats]
                                # Format float values to 4 decimal places
                                formatted_values = [f'{v:.4f}' if isinstance(v, (float, np.float32, np.float64)) else str(v) for v in column_values]
                                combined_df[column_name] = formatted_values
                            
                            # Display the combined table
                            show_table(combined_df)

elif selected_tab == "Probability Distributions":
    st.header("Probability Distributions")

    selected_dist_type = st.selectbox(
        "Select Distribution Type",
        options=['Normal', 'Binomial', 'Chi-square', 'Student-t', 'F-Distribution'],
        key="dist_type_select"
    )

    st.subheader("Distribution Parameters")
    params = {}
    if selected_dist_type == 'Normal':
        params['mean'] = st.number_input('Mean (μ):', value=0.0, step=0.1, key="normal_mean")
        params['std_dev'] = st.number_input('Std Dev (σ):', value=1.0, min_value=0.001, step=0.1, key="normal_std_dev")
    elif selected_dist_type == 'Binomial':
        params['n'] = st.number_input('Trials (n):', value=10, min_value=1, step=1, key="binomial_n")
        params['p'] = st.number_input('Prob. of Success (p):', value=0.5, min_value=0.0, max_value=1.0, step=0.01, key="binomial_p")
    elif selected_dist_type == 'Chi-square':
        params['df'] = st.number_input('Degrees of Freedom (df):', value=5, min_value=1, step=1, key="chi2_df")
    elif selected_dist_type == 'Student-t':
        params['df'] = st.number_input('Degrees of Freedom (df):', value=10, min_value=1, step=1, key="t_df")
    elif selected_dist_type == 'F-Distribution':
        params['dfn'] = st.number_input('Numerator df (df1):', value=5, min_value=1, step=1, key="f_dfn")
        params['dfd'] = st.number_input('Denominator df (df2):', value=10, min_value=1, step=1, key="f_dfd")

    st.subheader("Probability Calculation")
    
    # Different options for binomial (discrete) vs continuous distributions
    if selected_dist_type == 'Binomial':
        selected_calc_type = st.selectbox(
            "Calculation Type",
            options=['P(X = k)', 'P(X ≤ k)', 'P(X ≥ k)', 'P(X < k)', 'P(X > k)', 'P(a ≤ X ≤ b)'],
            key="prob_calc_type"
        )
    elif selected_dist_type == 'Chi-square':
        selected_calc_type = st.selectbox(
            "Calculation Type",
            options=['P(X > a)'],
            key="prob_calc_type"
        )
    else:
        selected_calc_type = st.selectbox(
            "Calculation Type",
            options=['P(X < a)', 'P(X > a)', 'P(a < X < b)'],
            key="prob_calc_type"
        )

    x_val, a_val, b_val = None, None, None
    if selected_calc_type in ['P(X < a)', 'P(X > a)', 'P(X = k)', 'P(X ≤ k)', 'P(X ≥ k)', 'P(X < k)', 'P(X > k)']:
        if selected_dist_type == 'Binomial':
            x_val = st.number_input('Value of k:', value=0, min_value=0, step=1, key="prob_x_input")
        else:
            x_val = st.number_input('Value of a:', value=0.0, step=0.1, key="prob_x_input")
    elif selected_calc_type in ['P(a < X < b)', 'P(a ≤ X ≤ b)']:
        col1, col2 = st.columns(2)
        with col1:
            if selected_dist_type == 'Binomial':
                a_val = st.number_input('Value of a:', value=0, min_value=0, step=1, key="prob_a_input")
            else:
                a_val = st.number_input('Value of a:', value=0.0, step=0.1, key="prob_a_input")
        with col2:
            if selected_dist_type == 'Binomial':
                b_val = st.number_input('Value of b:', value=1, min_value=0, step=1, key="prob_b_input")
            else:
                b_val = st.number_input('Value of b:', value=1.0, step=0.1, key="prob_b_input")

    if st.button("Calculate Probability and Plot", key="calc_prob_button"):
        st.subheader("Calculation Results")
        try:
            result = None
            fig = None
            calc_kwargs = {}

            calc_type_mapping = {
                'P(X < a)': 'cdf_strict',
                'P(X > a)': 'survival_strict',
                'P(a < X < b)': 'interval',
                'P(X = k)': 'pmf',
                'P(X ≤ k)': 'cdf',
                'P(X ≥ k)': 'survival',
                'P(X < k)': 'cdf_strict',
                'P(X > k)': 'survival_strict',
                'P(a ≤ X ≤ b)': 'interval_inclusive'
            }
            calc_kwargs['calc_type'] = calc_type_mapping.get(selected_calc_type)

            if selected_calc_type in ['P(X < a)', 'P(X > a)', 'P(X = k)', 'P(X ≤ k)', 'P(X ≥ k)', 'P(X < k)', 'P(X > k)']:
                if selected_dist_type == 'Binomial':
                    calc_kwargs['k'] = int(x_val) if x_val is not None else None
                else:
                    calc_kwargs['x'] = x_val
            elif selected_calc_type in ['P(a < X < b)', 'P(a ≤ X ≤ b)']:
                if selected_dist_type == 'Binomial':
                    calc_kwargs['a'] = int(a_val) if a_val is not None else None
                    calc_kwargs['b'] = int(b_val) if b_val is not None else None
                else:
                    calc_kwargs['a'] = a_val
                    calc_kwargs['b'] = b_val

            if selected_dist_type == 'Normal':
                result = calculate_normal_distribution(**params, **calc_kwargs)
                fig = plot_normal_distribution(**params, shade_x=x_val, shade_a=a_val, shade_b=b_val, calc_type=calc_kwargs['calc_type'])
            elif selected_dist_type == 'Binomial':
                result = calculate_binomial_distribution(**params, **calc_kwargs)
                fig = plot_binomial_distribution(**params, shade_k=x_val, shade_a=a_val, shade_b=b_val, calc_type=calc_kwargs['calc_type'])
            elif selected_dist_type == 'Chi-square':
                result = calculate_chi_square_distribution(**params, **calc_kwargs)
                fig = plot_chi_square_distribution(**params, shade_x=x_val, shade_a=a_val, shade_b=b_val, calc_type=calc_kwargs['calc_type'])
            elif selected_dist_type == 'Student-t':
                result = calculate_student_t_distribution(**params, **calc_kwargs)
                fig = plot_student_t_distribution(**params, shade_x=x_val, shade_a=a_val, shade_b=b_val, calc_type=calc_kwargs['calc_type'])
            elif selected_dist_type == 'F-Distribution':
                result = calculate_f_distribution(**params, **calc_kwargs)
                fig = plot_f_distribution(**params, shade_x=x_val, shade_a=a_val, shade_b=b_val, calc_type=calc_kwargs['calc_type'])

            if result is not None:
                st.write(f"--- **{selected_dist_type} Distribution Calculation** ---")
                st.write(f"**Parameters**: {params}")
                st.write(f"**Calculation Type**: {selected_calc_type}")
                if x_val is not None:
                    st.write(f"**x** = {x_val}")
                if a_val is not None:
                    st.write(f"**a** = {a_val}")
                if b_val is not None:
                    st.write(f"**b** = {b_val}")
                st.markdown(f"<p style='color: black; font-size: 18px;'><b>Calculated Probability: {result:.6f}</b></p>", unsafe_allow_html=True)
                if fig is not None:
                    st.pyplot(fig)
                    # Accessibility: Add text alternative for screen readers
                    caption_text = f"{selected_dist_type} distribution plot. Parameters: {', '.join([f'{k}={v}' for k,v in params.items()])}. "
                    if calc_kwargs['calc_type'] == 'cdf':
                        caption_text += f"Shows cumulative probability P(X ≤ {x_val}) = {result:.6f}. Shaded area represents probability."
                    elif calc_kwargs['calc_type'] == 'survival':
                        caption_text += f"Shows survival probability P(X ≥ {x_val}) = {result:.6f}. Shaded area represents probability."
                    elif calc_kwargs['calc_type'] == 'interval':
                        caption_text += f"Shows interval probability P({a_val} < X < {b_val}) = {result:.6f}. Shaded area represents probability."
                    elif calc_kwargs['calc_type'] == 'pmf':
                        caption_text += f"Shows probability mass function. P(X = {x_val}) = {result:.6f}. Highlighted bar shows probability."
                    st.caption(caption_text)
            else:
                st.warning("No calculation performed.")

        except ValueError as ve:
            st.error(f"Input Error: {ve}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

elif selected_tab == "Confidence Intervals":
    st.header("Confidence Intervals")

    if not st.session_state.global_dataframes:
        st.info("Please load or enter data in the 'Data Input' tab first to use raw data input.")

    ci_type_options = [
        'Mean (sigma unknown) - t-interval',
        'Proportion',
        'Difference Between Two Means (Independent, sigma known)',
        'Difference Between Two Means (Independent, sigma unknown, equal variances)',
        'Difference Between Two Means (Independent, sigma unknown, unequal variances)',
        'Difference Between Two Proportions',
        'Paired Differences'
    ]
    selected_ci_type = st.selectbox("Select CI Type", options=ci_type_options, key="ci_type_select")

    # Determine input method options based on selected CI type
    input_method_options = []
    if selected_ci_type in ['Proportion', 'Difference Between Two Proportions']:
        input_method_options = ['Summary Statistics Input']
    else:
        input_method_options = ['Raw Data', 'Summary Statistics Input']

    input_method = st.radio("Input Method", options=input_method_options, key="ci_input_method")

    st.subheader("Parameters")

    # Dynamic parameter inputs based on CI type and input method
    params = {}
    numeric_cols = [''] + get_numeric_columns()

    # Helper to get the value from session state if available, else a default
    def get_state_value(key, default):
        return st.session_state.get(key, default)


    if selected_ci_type == 'Mean (sigma unknown) - t-interval':
        if input_method == 'Raw Data':
            params['data_column'] = st.selectbox('Select Data Column', options=numeric_cols, key="ci_mean_suk_raw_data_col")
        else: # Summary Statistics Input
            params['sample_mean'] = st.number_input('Sample Mean (x̄):', value=get_state_value('ci_mean_suk_sum_mean', 0.0), key="ci_mean_suk_sum_mean")
            params['sample_std_dev'] = st.number_input('Sample Std Dev (s):', value=get_state_value('ci_mean_suk_sum_std_dev', 1.0), min_value=0.001, key="ci_mean_suk_sum_std_dev")
            params['sample_size'] = st.number_input('Sample Size (n):', value=get_state_value('ci_mean_suk_sum_size', 30), min_value=2, step=1, key="ci_mean_suk_sum_size")

    elif selected_ci_type == 'Proportion':
        # Only Summary Statistics Input
        params['num_successes'] = st.number_input('Number of Observed Successes (x):', value=get_state_value('ci_prop_sum_succ', 10), min_value=0, step=1, key="ci_prop_sum_succ")
        params['num_trials'] = st.number_input('Number of Trials (n):', value=get_state_value('ci_prop_sum_trials', 20), min_value=1, step=1, key="ci_prop_sum_trials")

    elif selected_ci_type == 'Difference Between Two Means (Independent, sigma known)':
        if input_method == 'Raw Data':
            col1, col2 = st.columns(2)
            with col1:
                params['data_column1'] = st.selectbox('Select Sample 1 Data', options=numeric_cols, key="ci_diff_mean_sk_raw_data_col1")
                params['pop_std_dev1'] = st.number_input('Pop. Std Dev 1 (σ1):', value=get_state_value('ci_diff_mean_sk_pop_std_dev1', 1.0), min_value=0.001, key="ci_diff_mean_sk_pop_std_dev1")
            with col2:
                params['data_column2'] = st.selectbox('Select Sample 2 Data', options=numeric_cols, key="ci_diff_mean_sk_raw_data_col2")
                params['pop_std_dev2'] = st.number_input('Pop. Std Dev 2 (σ2):', value=get_state_value('ci_diff_mean_sk_pop_std_dev2', 1.0), min_value=0.001, key="ci_diff_mean_sk_pop_std_dev2")
        else: # Summary Statistics Input
            col1, col2 = st.columns(2)
            with col1:
                params['sample_mean1'] = st.number_input('Sample 1 Mean (x̄1):', value=get_state_value('ci_diff_mean_sk_sum_mean1', 0.0), key="ci_diff_mean_sk_sum_mean1")
                params['pop_std_dev1'] = st.number_input('Pop. Std Dev 1 (σ1):', value=get_state_value('ci_diff_mean_sk_sum_pop_std_dev1', 1.0), min_value=0.001, key="ci_diff_mean_sk_sum_pop_std_dev1")
                params['sample_size1'] = st.number_input('Sample 1 Size (n1):', value=get_state_value('ci_diff_mean_sk_sum_size1', 30), min_value=1, step=1, key="ci_diff_mean_sk_sum_size1")
            with col2:
                params['sample_mean2'] = st.number_input('Sample 2 Mean (x̄2):', value=get_state_value('ci_diff_mean_sk_sum_mean2', 0.0), key="ci_diff_mean_sk_sum_mean2")
                params['pop_std_dev2'] = st.number_input('Pop. Std Dev 2 (σ2):', value=get_state_value('ci_diff_mean_sk_sum_pop_std_dev2', 1.0), min_value=0.001, key="ci_diff_mean_sk_sum_pop_std_dev2")
                params['sample_size2'] = st.number_input('Sample 2 Size (n2):', value=get_state_value('ci_diff_mean_sk_sum_size2', 30), min_value=1, step=1, key="ci_diff_mean_sk_sum_size2")

    elif selected_ci_type == 'Difference Between Two Means (Independent, sigma unknown, equal variances)':
        if input_method == 'Raw Data':
            col1, col2 = st.columns(2)
            with col1:
                params['data_column1'] = st.selectbox('Select Sample 1 Data', options=numeric_cols, key="ci_diff_mean_suev_raw_data_col1")
            with col2:
                params['data_column2'] = st.selectbox('Select Sample 2 Data', options=numeric_cols, key="ci_diff_mean_suev_raw_data_col2")
        else: # Summary Statistics Input
            col1, col2 = st.columns(2)
            with col1:
                params['sample_mean1'] = st.number_input('Sample 1 Mean (x̄1):', value=get_state_value('ci_diff_mean_suev_sum_mean1', 0.0), key="ci_diff_mean_suev_sum_mean1")
                params['sample_std_dev1'] = st.number_input('Sample 1 Std Dev (s1):', value=get_state_value('ci_diff_mean_suev_sum_std_dev1', 1.0), min_value=0.001, key="ci_diff_mean_suev_sum_std_dev1")
                params['sample_size1'] = st.number_input('Sample 1 Size (n1):', value=get_state_value('ci_diff_mean_suev_sum_size1', 30), min_value=2, step=1, key="ci_diff_mean_suev_sum_size1")
            with col2:
                params['sample_mean2'] = st.number_input('Sample 2 Mean (x̄2):', value=get_state_value('ci_diff_mean_suev_sum_mean2', 0.0), key="ci_diff_mean_suev_sum_mean2")
                params['sample_std_dev2'] = st.number_input('Sample 2 Std Dev (s2):', value=get_state_value('ci_diff_mean_suev_sum_std_dev2', 1.0), min_value=0.001, key="ci_diff_mean_suev_sum_std_dev2")
                params['sample_size2'] = st.number_input('Sample 2 Size (n2):', value=get_state_value('ci_diff_mean_suev_sum_size2', 30), min_value=2, step=1, key="ci_diff_mean_suev_sum_size2")

    elif selected_ci_type == 'Difference Between Two Means (Independent, sigma unknown, unequal variances)':
        if input_method == 'Raw Data':
            col1, col2 = st.columns(2)
            with col1:
                params['data_column1'] = st.selectbox('Select Sample 1 Data', options=numeric_cols, key="ci_diff_mean_suuv_raw_data_col1")
            with col2:
                params['data_column2'] = st.selectbox('Select Sample 2 Data', options=numeric_cols, key="ci_diff_mean_suuv_raw_data_col2")
        else: # Summary Statistics Input
            col1, col2 = st.columns(2)
            with col1:
                params['sample_mean1'] = st.number_input('Sample 1 Mean (x̄1):', value=get_state_value('ci_diff_mean_suuv_sum_mean1', 0.0), key="ci_diff_mean_suuv_sum_mean1")
                params['sample_std_dev1'] = st.number_input('Sample 1 Std Dev (s1):', value=get_state_value('ci_diff_mean_suuv_sum_std_dev1', 1.0), min_value=0.001, key="ci_diff_mean_suuv_sum_std_dev1")
                params['sample_size1'] = st.number_input('Sample 1 Size (n1):', value=get_state_value('ci_diff_mean_suuv_sum_size1', 30), min_value=2, step=1, key="ci_diff_mean_suuv_sum_size1")
            with col2:
                params['sample_mean2'] = st.number_input('Sample 2 Mean (x̄2):', value=get_state_value('ci_diff_mean_suuv_sum_mean2', 0.0), key="ci_diff_mean_suuv_sum_mean2")
                params['sample_std_dev2'] = st.number_input('Sample 2 Std Dev (s2):', value=get_state_value('ci_diff_mean_suuv_sum_std_dev2', 1.0), min_value=0.001, key="ci_diff_mean_suuv_sum_std_dev2")
                params['sample_size2'] = st.number_input('Sample 2 Size (n2):', value=get_state_value('ci_diff_mean_suuv_sum_size2', 30), min_value=2, step=1, key="ci_diff_mean_suuv_sum_size2")

    elif selected_ci_type == 'Difference Between Two Proportions':
        col1, col2 = st.columns(2)
        with col1:
            params['num_successes1'] = st.number_input('Observed Successes 1 (x1):', value=get_state_value('ci_diff_prop_sum_succ1', 10), min_value=0, step=1, key="ci_diff_prop_sum_succ1")
            params['num_trials1'] = st.number_input('Trials 1 (n1):', value=get_state_value('ci_diff_prop_sum_trials1', 20), min_value=1, step=1, key="ci_diff_prop_sum_trials1")
        with col2:
            params['num_successes2'] = st.number_input('Observed Successes 2 (x2):', value=get_state_value('ci_diff_prop_sum_succ2', 8), min_value=0, step=1, key="ci_diff_prop_sum_succ2")
            params['num_trials2'] = st.number_input('Trials 2 (n2):', value=get_state_value('ci_diff_prop_sum_trials2', 15), min_value=1, step=1, key="ci_diff_prop_sum_trials2")

    elif selected_ci_type == 'Paired Differences':
        if input_method == 'Raw Data':
            col1, col2 = st.columns(2)
            with col1:
                params['data_column1'] = st.selectbox('Select Sample 1 (Before)', options=numeric_cols, key="ci_paired_raw_data_col1")
            with col2:
                params['data_column2'] = st.selectbox('Select Sample 2 (After)', options=numeric_cols, key="ci_paired_raw_data_col2")
        else: # Summary Statistics Input
            params['mean_difference'] = st.number_input('Mean of Differences (d̄):', value=get_state_value('ci_paired_sum_mean_diff', 0.0), key="ci_paired_sum_mean_diff")
            params['std_dev_difference'] = st.number_input('Std Dev of Differences (sd):', value=get_state_value('ci_paired_sum_std_diff', 1.0), min_value=0.001, key="ci_paired_sum_std_diff")
            params['sample_size_difference'] = st.number_input('Number of Pairs (n):', value=get_state_value('ci_paired_sum_size_diff', 20), min_value=2, step=1, key="ci_paired_sum_size_diff")

    confidence_level = st.number_input('Confidence Level (e.g., 0.95):', value=get_state_value('ci_confidence_level', 0.95), min_value=0.01, max_value=0.99, step=0.01, format="%.2f", key="ci_confidence_level_input")

    if st.button("Calculate Confidence Interval", key="calc_ci_button"):
        st.subheader("Calculation Results")
        try:
            lower_bound, upper_bound = None, None

            if selected_ci_type == 'Mean (sigma unknown) - t-interval':
                if input_method == 'Raw Data':
                    data = get_data_from_col_string(params['data_column'])
                    lower_bound, upper_bound = ci_mean_sigma_unknown(data.mean(), data.std(), len(data), confidence_level)
                else:
                    lower_bound, upper_bound = ci_mean_sigma_unknown(params['sample_mean'], params['sample_std_dev'], params['sample_size'], confidence_level)

            elif selected_ci_type == 'Proportion':
                lower_bound, upper_bound = ci_proportion(params['num_successes'], params['num_trials'], confidence_level)

            elif selected_ci_type == 'Difference Between Two Means (Independent, sigma known)':
                if input_method == 'Raw Data':
                    data1 = get_data_from_col_string(params['data_column1'])
                    data2 = get_data_from_col_string(params['data_column2'])
                    lower_bound, upper_bound = ci_diff_means_sigma_known(data1.mean(), params['pop_std_dev1'], len(data1), data2.mean(), params['pop_std_dev2'], len(data2), confidence_level)
                else:
                    lower_bound, upper_bound = ci_diff_means_sigma_known(params['sample_mean1'], params['pop_std_dev1'], params['sample_size1'], params['sample_mean2'], params['pop_std_dev2'], params['sample_size2'], confidence_level)

            elif selected_ci_type == 'Difference Between Two Means (Independent, sigma unknown, equal variances)':
                if input_method == 'Raw Data':
                    data1 = get_data_from_col_string(params['data_column1'])
                    data2 = get_data_from_col_string(params['data_column2'])
                    lower_bound, upper_bound = ci_diff_means_sigma_unknown_equal_var(data1.mean(), data1.std(), len(data1), data2.mean(), data2.std(), len(data2), confidence_level)
                else:
                    lower_bound, upper_bound = ci_diff_means_sigma_unknown_equal_var(params['sample_mean1'], params['sample_std_dev1'], params['sample_size1'], params['sample_mean2'], params['sample_std_dev2'], params['sample_size2'], confidence_level)

            elif selected_ci_type == 'Difference Between Two Means (Independent, sigma unknown, unequal variances)':
                if input_method == 'Raw Data':
                    data1 = get_data_from_col_string(params['data_column1'])
                    data2 = get_data_from_col_string(params['data_column2'])
                    lower_bound, upper_bound = ci_diff_means_sigma_unknown_unequal_var(data1.mean(), data1.std(), len(data1), data2.mean(), data2.std(), len(data2), confidence_level)
                else:
                    lower_bound, upper_bound = ci_diff_means_sigma_unknown_unequal_var(params['sample_mean1'], params['sample_std_dev1'], params['sample_size1'], params['sample_mean2'], params['sample_std_dev2'], params['sample_size2'], confidence_level)

            elif selected_ci_type == 'Difference Between Two Proportions':
                lower_bound, upper_bound = ci_diff_proportions(params['num_successes1'], params['num_trials1'], params['num_successes2'], params['num_trials2'], confidence_level)

            elif selected_ci_type == 'Paired Differences':
                if input_method == 'Raw Data':
                    data1 = get_data_from_col_string(params['data_column1'])
                    data2 = get_data_from_col_string(params['data_column2'])
                    lower_bound, upper_bound = ci_paired_differences(data1, data2, confidence_level)
                else:
                    lower_bound, upper_bound = ci_paired_differences_summary(
                        params['mean_difference'],
                        params['std_dev_difference'],
                        params['sample_size_difference'],
                        confidence_level
                    )

            st.success(f"Confidence Interval ({confidence_level*100:.0f}%): ({lower_bound:.4f}, {upper_bound:.4f})")

        except ValueError as ve:
            st.error(f"Input Error: {ve}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

elif selected_tab == "Hypothesis Testing":
    st.header("Hypothesis Testing")

    if not st.session_state.global_dataframes:
        st.info("Please load or enter data in the 'Data Input' tab first to use raw data input.")

    ht_type_options = [
        'One-Sample t-test',
        'Two-Sample t-test (Independent Samples)',
        'Paired t-test',
        'One-Sample Z-test for Proportions',
        'Two-Sample Z-test for Proportions',
        'Chi-Square Goodness-of-Fit Test',
        'Chi-Square Test of Independence',
        'ANOVA (Analysis of Variance) F-test'
    ]
    selected_ht_type = st.selectbox("Select Hypothesis Test Type", options=ht_type_options, key="ht_type_select")

    # Determine input method options based on selected HT type
    ht_input_method_options = []
    if selected_ht_type in ['One-Sample Z-test for Proportions', 'Two-Sample Z-test for Proportions', 'Chi-Square Goodness-of-Fit Test']:
        ht_input_method_options = ['Summary Statistics']
    elif selected_ht_type == 'Chi-Square Test of Independence':
        ht_input_method_options = ['Raw Data', 'Summary Statistics (Contingency Table)']
    elif selected_ht_type == 'ANOVA (Analysis of Variance) F-test':
        ht_input_method_options = ['Raw Data'] # ANOVA typically uses raw data groups
    else:
        ht_input_method_options = ['Raw Data', 'Summary Statistics']

    st.subheader("Parameters")
    
    input_method = st.radio("Input Type:", options=ht_input_method_options, key="ht_input_method")

    params = {}
    numeric_cols = [''] + get_numeric_columns()
    all_cols = [''] + get_all_columns() # For categorical variables if needed

    # Helper to get the value from session state if available, else a default
    def get_state_value(key, default):
        return st.session_state.get(key, default)

    alternative_options = {
        'Two-sided (≠)': 'two-sided',
        'Greater Than (>)': 'greater',
        'Less Than (<)': 'less'
    }

    # Dynamic parameter inputs based on HT type and input method
    if selected_ht_type == 'One-Sample t-test':
        st.write("**Hypotheses**")
        # Create columns for hypothesis display with input box
        col_h0_1, col_h0_input, col_h0_2 = st.columns([1, 2, 4])
        with col_h0_1:
            st.write("H₀: μ =")
        with col_h0_input:
            if input_method == 'Raw Data':
                params['hypothesized_mean'] = st.number_input('μ₀', value=get_state_value('ht_os_t_hypo_mean_raw', 0.0), key="ht_os_t_hypo_mean_raw", label_visibility="collapsed")
            else:
                params['hypothesized_mean'] = st.number_input('μ₀', value=get_state_value('ht_os_t_hypo_mean_sum', 0.0), key="ht_os_t_hypo_mean_sum", label_visibility="collapsed")
        
        alt_hypothesis_key = f"ht_{selected_ht_type.replace(' ', '_').replace('-', '_')}_alt"
        selected_alternative_display = st.selectbox(
            "Alternative Hypothesis (HA):",
            options=list(alternative_options.keys()),
            format_func=lambda x: x.split(' ')[0], # Display only 'Two-sided', 'Greater', 'Less'
            key=alt_hypothesis_key
        )
        params['alternative'] = alternative_options[selected_alternative_display]
        
        # Display HA based on selection
        if params['alternative'] == 'two-sided':
            st.write(f"Hₐ: μ ≠ {params['hypothesized_mean']}")
        elif params['alternative'] == 'greater':
            st.write(f"Hₐ: μ > {params['hypothesized_mean']}")
        elif params['alternative'] == 'less':
            st.write(f"Hₐ: μ < {params['hypothesized_mean']}")

        if input_method == 'Raw Data':
            params['sample_data'] = st.selectbox('Select Sample Data Column', options=numeric_cols, key="ht_os_t_raw_data_col")
        else: # Summary Statistics Input
            params['sample_mean'] = st.number_input('Sample Mean (x̄):', value=get_state_value('ht_os_t_sum_mean', 0.0), key="ht_os_t_sum_mean")
            params['sample_std_dev'] = st.number_input('Sample Std Dev (s):', value=get_state_value('ht_os_t_sum_std_dev', 1.0), min_value=0.001, key="ht_os_t_sum_std_dev")
            params['sample_size'] = st.number_input('Sample Size (n):', value=get_state_value('ht_os_t_sum_size', 30), min_value=2, step=1, key="ht_os_t_sum_size")

    elif selected_ht_type == 'Two-Sample t-test (Independent Samples)':
        st.write("**Hypotheses**")
        st.write("H₀: μ₁ = μ₂")
        
        alt_hypothesis_key = f"ht_{selected_ht_type.replace(' ', '_').replace('-', '_')}_alt"
        selected_alternative_display = st.selectbox(
            "Alternative Hypothesis (HA):",
            options=list(alternative_options.keys()),
            format_func=lambda x: x.split(' ')[0], # Display only 'Two-sided', 'Greater', 'Less'
            key=alt_hypothesis_key
        )
        params['alternative'] = alternative_options[selected_alternative_display]
        
        # Display HA based on selection
        if params['alternative'] == 'two-sided':
            st.write("Hₐ: μ₁ ≠ μ₂")
        elif params['alternative'] == 'greater':
            st.write("Hₐ: μ₁ > μ₂")
        elif params['alternative'] == 'less':
            st.write("Hₐ: μ₁ < μ₂")

        params['equal_variances'] = st.checkbox('Assume Equal Variances', value=True, key="ht_ts_t_equal_var")
        if input_method == 'Raw Data':
            col1, col2 = st.columns(2)
            with col1:
                params['sample_data1'] = st.selectbox('Select Sample 1 Data Column', options=numeric_cols, key="ht_ts_t_raw_data_col1")
            with col2:
                params['sample_data2'] = st.selectbox('Select Sample 2 Data Column', options=numeric_cols, key="ht_ts_t_raw_data_col2")
        else: # Summary Statistics Input
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Sample 1**")
                params['sample1_mean'] = st.number_input('Sample 1 Mean (x̄1):', value=get_state_value('ht_ts_t_sum_mean1', 0.0), key="ht_ts_t_sum_mean1")
                params['sample1_std_dev'] = st.number_input('Sample 1 Std Dev (s1):', value=get_state_value('ht_ts_t_sum_std_dev1', 1.0), min_value=0.001, key="ht_ts_t_sum_std_dev1")
                params['sample1_size'] = st.number_input('Sample 1 Size (n1):', value=get_state_value('ht_ts_t_sum_size1', 30), min_value=2, step=1, key="ht_ts_t_sum_size1")
            with col2:
                st.write("**Sample 2**")
                params['sample2_mean'] = st.number_input('Sample 2 Mean (x̄2):', value=get_state_value('ht_ts_t_sum_mean2', 0.0), key="ht_ts_t_sum_mean2")
                params['sample2_std_dev'] = st.number_input('Sample 2 Std Dev (s2):', value=get_state_value('ht_ts_t_sum_std_dev2', 1.0), min_value=0.001, key="ht_ts_t_sum_std_dev2")
                params['sample2_size'] = st.number_input('Sample 2 Size (n2):', value=get_state_value('ht_ts_t_sum_size2', 30), min_value=2, step=1, key="ht_ts_t_sum_size2")

    elif selected_ht_type == 'Paired t-test':
        st.write("**Hypotheses**")
        st.write("H₀: μd = 0")
        
        alt_hypothesis_key = f"ht_{selected_ht_type.replace(' ', '_').replace('-', '_')}_alt"
        selected_alternative_display = st.selectbox(
            "Alternative Hypothesis (HA):",
            options=list(alternative_options.keys()),
            format_func=lambda x: x.split(' ')[0], # Display only 'Two-sided', 'Greater', 'Less'
            key=alt_hypothesis_key
        )
        params['alternative'] = alternative_options[selected_alternative_display]
        
        # Display HA based on selection
        if params['alternative'] == 'two-sided':
            st.write("Hₐ: μd ≠ 0")
        elif params['alternative'] == 'greater':
            st.write("Hₐ: μd > 0")
        elif params['alternative'] == 'less':
            st.write("Hₐ: μd < 0")

        if input_method == 'Raw Data':
            col1, col2 = st.columns(2)
            with col1:
                params['sample_data1'] = st.selectbox('Select Sample 1 Data (Before)', options=numeric_cols, key="ht_paired_t_raw_data_col1")
            with col2:
                params['sample_data2'] = st.selectbox('Select Sample 2 Data (After)', options=numeric_cols, key="ht_paired_t_raw_data_col2")
        else: # Summary Statistics Input
            params['mean_difference'] = st.number_input('Mean of Differences (d̄):', value=get_state_value('ht_paired_t_sum_mean_diff', 0.0), key="ht_paired_t_sum_mean_diff")
            params['std_dev_difference'] = st.number_input('Std Dev of Differences (sd):', value=get_state_value('ht_paired_t_sum_std_diff', 1.0), min_value=0.001, key="ht_paired_t_sum_std_diff")
            params['sample_size_difference'] = st.number_input('Number of Pairs (n):', value=get_state_value('ht_paired_t_sum_size_diff', 20), min_value=2, step=1, key="ht_paired_t_sum_size_diff")

    elif selected_ht_type == 'One-Sample Z-test for Proportions':
        st.write("**Hypotheses**")
        # Create columns for hypothesis display with input box
        col_h0_1, col_h0_input, col_h0_2 = st.columns([1, 2, 4])
        with col_h0_1:
            st.write("H₀: p =")
        with col_h0_input:
            params['hypothesized_proportion'] = st.number_input('p₀', value=get_state_value('ht_os_z_prop_sum_hypo_prop', 0.5), min_value=0.0, max_value=1.0, step=0.01, key="ht_os_z_prop_sum_hypo_prop", label_visibility="collapsed")
        
        alt_hypothesis_key = f"ht_{selected_ht_type.replace(' ', '_').replace('-', '_')}_alt"
        selected_alternative_display = st.selectbox(
            "Alternative Hypothesis (HA):",
            options=list(alternative_options.keys()),
            format_func=lambda x: x.split(' ')[0], # Display only 'Two-sided', 'Greater', 'Less'
            key=alt_hypothesis_key
        )
        params['alternative'] = alternative_options[selected_alternative_display]
        
        # Display HA based on selection
        if params['alternative'] == 'two-sided':
            st.write(f"Hₐ: p ≠ {params['hypothesized_proportion']}")
        elif params['alternative'] == 'greater':
            st.write(f"Hₐ: p > {params['hypothesized_proportion']}")
        elif params['alternative'] == 'less':
            st.write(f"Hₐ: p < {params['hypothesized_proportion']}")

        # Only Summary Statistics Input
        params['num_successes'] = st.number_input('Number of Observed Successes (x):', value=get_state_value('ht_os_z_prop_sum_succ', 10), min_value=0, step=1, key="ht_os_z_prop_sum_succ")
        params['num_trials'] = st.number_input('Number of Trials (n):', value=get_state_value('ht_os_z_prop_sum_trials', 20), min_value=1, step=1, key="ht_os_z_prop_sum_trials")

    elif selected_ht_type == 'Two-Sample Z-test for Proportions':
        st.write("**Hypotheses**")
        st.write("H₀: p₁ = p₂")
        
        alt_hypothesis_key = f"ht_{selected_ht_type.replace(' ', '_').replace('-', '_')}_alt"
        selected_alternative_display = st.selectbox(
            "Alternative Hypothesis (HA):",
            options=list(alternative_options.keys()),
            format_func=lambda x: x.split(' ')[0], # Display only 'Two-sided', 'Greater', 'Less'
            key=alt_hypothesis_key
        )
        params['alternative'] = alternative_options[selected_alternative_display]
        
        # Display HA based on selection
        if params['alternative'] == 'two-sided':
            st.write("Hₐ: p₁ ≠ p₂")
        elif params['alternative'] == 'greater':
            st.write("Hₐ: p₁ > p₂")
        elif params['alternative'] == 'less':
            st.write("Hₐ: p₁ < p₂")

        # Only Summary Statistics Input
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Sample 1**")
            params['num_successes1'] = st.number_input('Observed Successes 1 (x1):', value=get_state_value('ht_ts_z_prop_sum_succ1', 10), min_value=0, step=1, key="ht_ts_z_prop_sum_succ1")
            params['num_trials1'] = st.number_input('Trials 1 (n1):', value=get_state_value('ht_ts_z_prop_sum_trials1', 20), min_value=1, step=1, key="ht_ts_z_prop_sum_trials1")
        with col2:
            st.write("**Sample 2**")
            params['num_successes2'] = st.number_input('Observed Successes 2 (x2):', value=get_state_value('ht_ts_z_prop_sum_succ2', 8), min_value=0, step=1, key="ht_ts_z_prop_sum_succ2")
            params['num_trials2'] = st.number_input('Trials 2 (n2):', value=get_state_value('ht_ts_z_prop_sum_trials2', 15), min_value=1, step=1, key="ht_ts_z_prop_sum_trials2")

    elif selected_ht_type == 'Chi-Square Goodness-of-Fit Test':
        # Only Summary Statistics Input
        st.write("**Frequencies Table**")
        num_categories = st.number_input('Number of Categories:', value=get_state_value('ht_chi2_gof_num_cat', 3), min_value=2, max_value=20, step=1, key="ht_chi2_gof_num_cat")
        
        # Input category names
        st.write("**Category Names:**")
        cat_cols = st.columns(min(int(num_categories), 5))  # Max 5 columns per row
        category_names = []
        for i in range(int(num_categories)):
            col_idx = i % 5
            with cat_cols[col_idx]:
                cat_key = f"ht_chi2_gof_cat_name_{i}"
                default_name = get_state_value(cat_key, f"Cat {i+1}")
                name = st.text_input(f'Category {i+1}', value=default_name, key=cat_key, label_visibility="collapsed")
                category_names.append(name)
        
        # Create table input with borders
        st.write("**Enter frequencies:**")
        
        with st.container(border=True):
            # Header row
            header_cols = st.columns([2, 1.5, 1.5])
            with header_cols[0]:
                st.markdown("**Category**")
            with header_cols[1]:
                st.markdown("**Observed**")
            with header_cols[2]:
                st.markdown("**Expected**")
            
            st.markdown('<hr style="margin: 5px 0; border: 1px solid #4a4a4a;">', unsafe_allow_html=True)
            
            # Data rows
            observed_values = []
            expected_values = []
            for i in range(int(num_categories)):
                cols = st.columns([2, 1.5, 1.5])
                with cols[0]:
                    st.markdown(f"**{category_names[i]}**")
                with cols[1]:
                    obs_key = f"ht_chi2_gof_obs_{i}"
                    obs_val = st.number_input(f'Obs {i}', value=get_state_value(obs_key, 10.0), min_value=0.0, step=1.0, key=obs_key, label_visibility="collapsed")
                    observed_values.append(obs_val)
                with cols[2]:
                    exp_key = f"ht_chi2_gof_exp_{i}"
                    exp_val = st.number_input(f'Exp {i}', value=get_state_value(exp_key, 0.0), min_value=0.0, step=1.0, key=exp_key, label_visibility="collapsed")
                    expected_values.append(exp_val)
                
                # Add horizontal line between rows (except after last row)
                if i < int(num_categories) - 1:
                    st.markdown('<hr style="margin: 5px 0; border: 0.5px solid #ddd;">', unsafe_allow_html=True)
        
        # Convert to comma-separated strings for compatibility
        params['observed_frequencies'] = ','.join([str(v) for v in observed_values])
        # Store category names for output display
        params['category_names'] = category_names
        # If all expected values are 0, leave empty string for equal distribution
        if all(v == 0.0 for v in expected_values):
            params['expected_frequencies'] = ''
        else:
            params['expected_frequencies'] = ','.join([str(v) for v in expected_values])

    elif selected_ht_type == 'Chi-Square Test of Independence':
        if input_method == "Raw Data":
            st.write("**Select Two Categorical Variables**")
            
            # Get categorical columns only
            categorical_cols_options = ['']
            for df_name, df in st.session_state.global_dataframes.items():
                for col in df.columns:
                    try:
                        pd.to_numeric(df[col], errors='raise')
                        if df[col].nunique() <= 15:
                            categorical_cols_options.append(f"{df_name}: {col}")
                    except (ValueError, TypeError):
                        categorical_cols_options.append(f"{df_name}: {col}")
            
            col1, col2 = st.columns(2)
            with col1:
                row_var = st.selectbox("Row Variable", options=categorical_cols_options, key="chi2_ind_row_var")
            with col2:
                col_var = st.selectbox("Column Variable", options=categorical_cols_options, key="chi2_ind_col_var")
            
            params['chi2_ind_input_type'] = 'raw_data'
            params['row_variable'] = row_var
            params['col_variable'] = col_var
            
        else:  # Summary Statistics
            st.write("**Contingency Table**")
            num_rows = st.number_input('Number of Rows:', value=get_state_value('ht_chi2_ind_num_rows', 2), min_value=2, max_value=10, step=1, key="ht_chi2_ind_num_rows")
            num_cols = st.number_input('Number of Columns:', value=get_state_value('ht_chi2_ind_num_cols', 2), min_value=2, max_value=10, step=1, key="ht_chi2_ind_num_cols")
            params['chi2_ind_input_type'] = 'summary'
            
            # Input category names for rows
            st.write("**Row Categories:**")
            row_cols = st.columns(int(num_rows))
            row_names = []
            for i in range(int(num_rows)):
                with row_cols[i]:
                    row_key = f"ht_chi2_ind_row_name_{i}"
                    default_name = get_state_value(row_key, f"Row {i+1}")
                    name = st.text_input(f'Row {i+1} Name', value=default_name, key=row_key, label_visibility="collapsed")
                    row_names.append(name)
            
            # Input category names for columns
            st.write("**Column Categories:**")
            col_cols = st.columns(int(num_cols))
            col_names = []
            for j in range(int(num_cols)):
                with col_cols[j]:
                    col_key = f"ht_chi2_ind_col_name_{j}"
                    default_name = get_state_value(col_key, f"Col {j+1}")
                    name = st.text_input(f'Col {j+1} Name', value=default_name, key=col_key, label_visibility="collapsed")
                    col_names.append(name)
            
            # Create table input with category labels and borders
            st.write("**Enter values for each cell:**")
            
            # Add CSS for better table styling with column borders
            st.markdown("""
            <style>
            .chi2-table-cell {
                border-right: 1px solid #ddd;
                padding: 5px;
            }
            .chi2-table-header {
                border-right: 1px solid #ddd;
                border-bottom: 2px solid #4a4a4a;
                padding: 5px;
                text-align: center;
                font-weight: bold;
            }
            .chi2-table-row-header {
                border-right: 2px solid #4a4a4a;
                padding: 5px;
                font-weight: bold;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Container with border styling
            with st.container(border=True):
                # Header row with column names
                header_cols = st.columns([1.5] + [1] * int(num_cols))
                with header_cols[0]:
                    st.markdown('<div class="chi2-table-row-header">&nbsp;</div>', unsafe_allow_html=True)  # Empty corner cell
                for j in range(int(num_cols)):
                    with header_cols[j + 1]:
                        st.markdown(f'<div class="chi2-table-header">{col_names[j]}</div>', unsafe_allow_html=True)
                
                st.markdown('<hr style="margin: 5px 0; border: 1px solid #4a4a4a;">', unsafe_allow_html=True)
                
                # Data rows
                table_data = []
                for i in range(int(num_rows)):
                    # Create header column for row name plus data columns
                    cols = st.columns([1.5] + [1] * int(num_cols))
                    with cols[0]:
                        st.markdown(f'<div class="chi2-table-row-header">{row_names[i]}</div>', unsafe_allow_html=True)
                    
                    row_data = []
                    for j in range(int(num_cols)):
                        with cols[j + 1]:
                            cell_key = f"ht_chi2_ind_cell_{i}_{j}"
                            default_val = get_state_value(cell_key, 10.0)
                            val = st.number_input(f'{row_names[i]}-{col_names[j]}', value=default_val, min_value=0.0, step=1.0, key=cell_key, label_visibility="collapsed")
                            row_data.append(val)
                    table_data.append(row_data)
                    
                    # Add horizontal line between rows (except after last row)
                    if i < int(num_rows) - 1:
                        st.markdown('<hr style="margin: 5px 0; border: 0.5px solid #ddd;">', unsafe_allow_html=True)
            
            # Convert table to string format for compatibility with existing code
            params['contingency_table'] = ';'.join([','.join([str(val) for val in row]) for row in table_data])

    elif selected_ht_type == 'ANOVA (Analysis of Variance) F-test':
        # Only Raw Data Input
        if not numeric_cols:
            st.warning("No numeric columns available. Please upload or enter data first.")
        else:
            num_groups = st.number_input('Number of Groups:', value=get_state_value('ht_anova_num_groups', 2), min_value=2, step=1, key="ht_anova_num_groups")

            group_data_cols = []
            for i in range(int(num_groups)):
                col_key = f"ht_anova_group_data_col_{i+1}"
                # Ensure we have a valid default index
                default_index = i if i < len(numeric_cols) else 0
                selected_col = st.selectbox(f'Select Group {i+1} Data Column', options=numeric_cols, index=default_index, key=col_key)
                group_data_cols.append(selected_col)
            params['group_data_cols'] = group_data_cols

    alpha_level = st.number_input('Significance Level (α) for visualization:', value=get_state_value('ht_alpha_level', 0.05), min_value=0.001, max_value=0.999, step=0.01, key="ht_alpha_level")

    if st.button("Perform Hypothesis Test", key="perform_ht_button"):
        st.subheader("Test Results")
        try:
            test_statistic, p_value, degrees_freedom, expected_frequencies = None, None, None, None
            st.write(f"--- **{selected_ht_type}** ---")

            # Execute the selected test
            if selected_ht_type == 'One-Sample t-test':
                if input_method == 'Raw Data':
                    data = get_data_from_col_string(params['sample_data'])
                    test_statistic, p_value = one_sample_t_test(data, params['hypothesized_mean'], alternative=params['alternative'])
                    st.write(f"Sample Mean: {np.mean(data):.4f}")
                else:
                    test_statistic, p_value = one_sample_t_test_summary(params['sample_mean'], params['sample_std_dev'], params['sample_size'], params['hypothesized_mean'], alternative=params['alternative'])
                    st.write(f"Sample Mean: {params['sample_mean']:.4f}, Sample Std Dev: {params['sample_std_dev']:.4f}, Sample Size: {params['sample_size']}")
                st.write(f"Hypothesized Mean (μ0): {params['hypothesized_mean']}")

            elif selected_ht_type == 'Two-Sample t-test (Independent Samples)':
                if input_method == 'Raw Data':
                    data1 = get_data_from_col_string(params['sample_data1'])
                    data2 = get_data_from_col_string(params['sample_data2'])
                    test_statistic, p_value = two_sample_t_test_independent(data1, data2, equal_variances=params['equal_variances'], alternative=params['alternative'])
                    st.write(f"Sample 1 Mean: {np.mean(data1):.4f} (N={len(data1)}) ")
                    st.write(f"Sample 2 Mean: {np.mean(data2):.4f} (N={len(data2)}) ")
                else:
                    test_statistic, p_value = two_sample_t_test_independent_summary(params['sample1_mean'], params['sample1_std_dev'], params['sample1_size'], params['sample2_mean'], params['sample2_std_dev'], params['sample2_size'], equal_variances=params['equal_variances'], alternative=params['alternative'])
                    st.write(f"Sample 1: Mean={params['sample1_mean']:.4f}, Std Dev={params['sample1_std_dev']:.4f}, Size={params['sample1_size']}")
                    st.write(f"Sample 2: Mean={params['sample2_mean']:.4f}, Std Dev={params['sample2_std_dev']:.4f}, Size={params['sample2_size']}")
                st.write(f"Assumed Equal Variances: {params['equal_variances']}")

            elif selected_ht_type == 'Paired t-test':
                if input_method == 'Raw Data':
                    data1 = get_data_from_col_string(params['sample_data1'])
                    data2 = get_data_from_col_string(params['sample_data2'])
                    test_statistic, p_value = paired_t_test(data1, data2, alternative=params['alternative'])
                    st.write(f"Sample 1 (Before) Mean: {np.mean(data1):.4f}")
                    st.write(f"Sample 2 (After) Mean: {np.mean(data2):.4f}")
                else:
                    test_statistic, p_value = paired_t_test_summary(params['mean_difference'], params['std_dev_difference'], params['sample_size_difference'], alternative=params['alternative'])
                    st.write(f"Mean Difference: {params['mean_difference']:.4f}, Std Dev of Differences: {params['std_dev_difference']:.4f}, Number of Pairs: {params['sample_size_difference']}")

            elif selected_ht_type == 'One-Sample Z-test for Proportions':
                test_statistic, p_value = one_sample_z_test_proportion(params['num_successes'], params['num_trials'], params['hypothesized_proportion'], alternative=params['alternative'])
                st.write(f"Sample Proportion: {(params['num_successes']/params['num_trials']):.4f} (x={params['num_successes']}, n={params['num_trials']})")
                st.write(f"Hypothesized Proportion (p0): {params['hypothesized_proportion']}")

            elif selected_ht_type == 'Two-Sample Z-test for Proportions':
                test_statistic, p_value = two_sample_z_test_proportion(params['num_successes1'], params['num_trials1'], params['num_successes2'], params['num_trials2'], alternative=params['alternative'])
                st.write(f"Sample 1 Proportion: {(params['num_successes1']/params['num_trials1']):.4f} (x1={params['num_successes1']}, n1={params['num_trials1']})")
                st.write(f"Sample 2 Proportion: {(params['num_successes2']/params['num_trials2']):.4f} (x2={params['num_successes2']}, n2={params['num_trials2']})")

            elif selected_ht_type == 'Chi-Square Goodness-of-Fit Test':
                observed = [float(x.strip()) for x in params['observed_frequencies'].split(',') if x.strip()]
                expected = []
                if params['expected_frequencies']:
                    expected = [float(x.strip()) for x in params['expected_frequencies'].split(',') if x.strip()]
                else:
                    # Use equal distribution
                    expected = [np.mean(observed)] * len(observed)
                
                test_statistic, p_value = chi_square_goodness_of_fit_test(observed, expected_frequencies=expected if params['expected_frequencies'] else None)
                
                # Get category names
                category_names = params.get('category_names', [f"Category {i+1}" for i in range(len(observed))])
                
                # Create HTML table with black borders
                table_html = """
                <style>
                .gof-table {
                    border-collapse: collapse;
                    width: 100%;
                    margin: 10px 0;
                }
                .gof-table th, .gof-table td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: center;
                }
                .gof-table th {
                    background-color: #f0f0f0;
                    font-weight: bold;
                }
                </style>
                <table class="gof-table">
                <tr>
                    <th>Category</th>
                    <th>Observed</th>
                    <th>Expected</th>
                </tr>
                """
                
                for i, (cat_name, obs_val, exp_val) in enumerate(zip(category_names, observed, expected)):
                    table_html += f"""
                <tr>
                    <td>{cat_name}</td>
                    <td>{obs_val:.2f}</td>
                    <td>{exp_val:.2f}</td>
                </tr>
                """
                
                table_html += "</table>"
                st.markdown(table_html, unsafe_allow_html=True)

            elif selected_ht_type == 'Chi-Square Test of Independence':
                if params.get('chi2_ind_input_type') == 'raw_data':
                    # Process raw data
                    if not params.get('row_variable') or not params.get('col_variable'):
                        raise ValueError("Please select both row and column variables.")
                    
                    df_name_row, col_name_row = params['row_variable'].split(': ', 1)
                    df_name_col, col_name_col = params['col_variable'].split(': ', 1)
                    
                    if df_name_row != df_name_col:
                        raise ValueError("Both variables must come from the same DataFrame.")
                    
                    df = st.session_state.global_dataframes.get(df_name_row)
                    if df is None:
                        raise ValueError(f"DataFrame '{df_name_row}' not found.")
                    
                    # Create contingency table from raw data
                    contingency_table = pd.crosstab(df[col_name_row], df[col_name_col])
                    table = contingency_table.values.tolist()
                    
                    test_statistic, p_value, degrees_freedom, expected_frequencies = chi_square_test_of_independence(table)
                    
                    st.write(f"**Observed Frequencies:**")
                    contingency_table.index.name = None
                    contingency_table.columns.name = None
                    show_table(contingency_table)
                    
                    expected_df = pd.DataFrame(
                        expected_frequencies, 
                        index=contingency_table.index, 
                        columns=contingency_table.columns
                    )
                    expected_df.index.name = None
                    expected_df.columns.name = None
                    st.write(f"**Expected Frequencies:**")
                    show_table(expected_df.round(2))
                    st.write(f"**Degrees of Freedom:** {degrees_freedom}")
                    
                else:
                    # Process summary statistics (contingency table input)
                    rows = params['contingency_table'].split(';')
                    table = []
                    for row in rows:
                        table.append([float(val.strip()) for val in row.split(',')])
                    test_statistic, p_value, degrees_freedom, expected_frequencies = chi_square_test_of_independence(table)
                    st.write(f"**Observed Frequencies:**")
                    st.write(np.array(table))
                    st.write(f"**Expected Frequencies:**")
                    st.write(np.array(expected_frequencies).round(2))
                    st.write(f"**Degrees of Freedom:** {degrees_freedom}")

            elif selected_ht_type == 'ANOVA (Analysis of Variance) F-test':
                group_data = []
                for i, col_string in enumerate(params['group_data_cols']):
                    if col_string:
                        try:
                            data = get_data_from_col_string(col_string)
                            if len(data) < 2:
                                raise ValueError(f"Group {i+1} has only {len(data)} observation(s). At least 2 observations are required.")
                            group_data.append(data)
                        except Exception as e:
                            raise ValueError(f"Error loading Group {i+1} data: {str(e)}")
                
                if len(group_data) < 2:
                    raise ValueError("ANOVA requires at least two groups with data.")
                test_statistic, p_value = anova_f_test(*group_data)
                for i, data in enumerate(group_data):
                    st.write(f"Group {i+1} Mean: {np.mean(data):.4f} (N={len(data)}) ")

            if test_statistic is not None and p_value is not None:
                st.write(f"**Test Statistic**: {test_statistic:.4f}")
                if p_value < 0.0001:
                    st.write(f"**P-value**: <.0001")
                else:
                    st.write(f"**P-value**: {p_value:.4f}")
                
                # Create visualization
                st.write("**Visualization**")
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Determine the distribution and plot accordingly
                if selected_ht_type in ['One-Sample t-test', 'Two-Sample t-test (Independent Samples)', 'Paired t-test']:
                    # t-distribution - convert to original scale
                    if selected_ht_type == 'One-Sample t-test':
                        if input_method == 'Raw Data':
                            data = get_data_from_col_string(params['sample_data'])
                            df = len(data) - 1
                            sample_mean = np.mean(data)
                            se = np.std(data, ddof=1) / np.sqrt(len(data))
                        else:
                            df = params['sample_size'] - 1
                            sample_mean = params['sample_mean']
                            se = params['sample_std_dev'] / np.sqrt(params['sample_size'])
                        
                        mu0 = params['hypothesized_mean']
                        # Convert t-scores to original scale
                        t_range = np.linspace(-4, 4, 1000)
                        x_original = mu0 + t_range * se
                        # Scale the density appropriately
                        y = stats.t.pdf(t_range, df) / se
                        ax.plot(x_original, y, 'b-', linewidth=2, label=f't-distribution (df={df})')
                        
                        # Get actual sample mean value
                        actual_value = sample_mean
                        
                    elif selected_ht_type == 'Two-Sample t-test (Independent Samples)':
                        if input_method == 'Raw Data':
                            data1 = get_data_from_col_string(params['sample_data1'])
                            data2 = get_data_from_col_string(params['sample_data2'])
                            n1, n2 = len(data1), len(data2)
                            df = n1 + n2 - 2
                            mean1, mean2 = np.mean(data1), np.mean(data2)
                            if params['equal_variances']:
                                s1, s2 = np.std(data1, ddof=1), np.std(data2, ddof=1)
                                sp = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / df)
                                se = sp * np.sqrt(1/n1 + 1/n2)
                            else:
                                se = np.sqrt(np.var(data1, ddof=1)/n1 + np.var(data2, ddof=1)/n2)
                        else:
                            df = params['sample1_size'] + params['sample2_size'] - 2
                            mean1, mean2 = params['sample1_mean'], params['sample2_mean']
                            n1, n2 = params['sample1_size'], params['sample2_size']
                            if params['equal_variances']:
                                sp = np.sqrt(((n1-1)*params['sample1_std_dev']**2 + (n2-1)*params['sample2_std_dev']**2) / df)
                                se = sp * np.sqrt(1/n1 + 1/n2)
                            else:
                                se = np.sqrt(params['sample1_std_dev']**2/n1 + params['sample2_std_dev']**2/n2)
                        
                        # Convert t-scores to difference in means scale
                        t_range = np.linspace(-4, 4, 1000)
                        x_original = t_range * se  # centered at 0 for H0: μ1 - μ2 = 0
                        y = stats.t.pdf(t_range, df) / se
                        ax.plot(x_original, y, 'b-', linewidth=2, label=f't-distribution (df={df})')
                        
                        actual_value = mean1 - mean2
                        
                    else:  # Paired t-test
                        if input_method == 'Raw Data':
                            data1 = get_data_from_col_string(params['sample_data1'])
                            data2 = get_data_from_col_string(params['sample_data2'])
                            differences = np.array(data1) - np.array(data2)
                            df = len(differences) - 1
                            mean_diff = np.mean(differences)
                            se = np.std(differences, ddof=1) / np.sqrt(len(differences))
                        else:
                            df = params['sample_size_difference'] - 1
                            mean_diff = params['mean_difference']
                            se = params['std_dev_difference'] / np.sqrt(params['sample_size_difference'])
                        
                        # Convert t-scores to difference scale
                        t_range = np.linspace(-4, 4, 1000)
                        x_original = t_range * se  # centered at 0 for H0: μd = 0
                        y = stats.t.pdf(t_range, df) / se
                        ax.plot(x_original, y, 'b-', linewidth=2, label=f't-distribution (df={df})')
                        
                        actual_value = mean_diff
                    
                    # Determine critical values and shade regions on original scale
                    if params['alternative'] == 'two-sided':
                        critical_low_t = stats.t.ppf(alpha_level/2, df)
                        critical_high_t = stats.t.ppf(1 - alpha_level/2, df)
                        
                        if selected_ht_type == 'One-Sample t-test':
                            critical_low = mu0 + critical_low_t * se
                            critical_high = mu0 + critical_high_t * se
                            x_left = np.linspace(x_original.min(), critical_low, 100)
                            x_right = np.linspace(critical_high, x_original.max(), 100)
                        else:
                            critical_low = critical_low_t * se
                            critical_high = critical_high_t * se
                            x_left = np.linspace(x_original.min(), critical_low, 100)
                            x_right = np.linspace(critical_high, x_original.max(), 100)
                        
                        t_left = (x_left - (mu0 if selected_ht_type == 'One-Sample t-test' else 0)) / se
                        t_right = (x_right - (mu0 if selected_ht_type == 'One-Sample t-test' else 0)) / se
                        ax.fill_between(x_left, stats.t.pdf(t_left, df) / se, alpha=0.3, color='red', label=f'Rejection region (α={alpha_level})')
                        ax.fill_between(x_right, stats.t.pdf(t_right, df) / se, alpha=0.3, color='red')
                        
                        # Shade p-value region
                        if actual_value < (mu0 if selected_ht_type == 'One-Sample t-test' else 0):
                            x_pval_left = np.linspace(x_original.min(), actual_value, 100)
                            t_pval_left = (x_pval_left - (mu0 if selected_ht_type == 'One-Sample t-test' else 0)) / se
                            ax.fill_between(x_pval_left, stats.t.pdf(t_pval_left, df) / se, alpha=0.5, color='yellow', label=f'p-value region')
                            
                            mirror_value = 2*(mu0 if selected_ht_type == 'One-Sample t-test' else 0) - actual_value
                            x_pval_right = np.linspace(mirror_value, x_original.max(), 100)
                            t_pval_right = (x_pval_right - (mu0 if selected_ht_type == 'One-Sample t-test' else 0)) / se
                            ax.fill_between(x_pval_right, stats.t.pdf(t_pval_right, df) / se, alpha=0.5, color='yellow')
                        else:
                            mirror_value = 2*(mu0 if selected_ht_type == 'One-Sample t-test' else 0) - actual_value
                            x_pval_left = np.linspace(x_original.min(), mirror_value, 100)
                            t_pval_left = (x_pval_left - (mu0 if selected_ht_type == 'One-Sample t-test' else 0)) / se
                            ax.fill_between(x_pval_left, stats.t.pdf(t_pval_left, df) / se, alpha=0.5, color='yellow', label=f'p-value region')
                            
                            x_pval_right = np.linspace(actual_value, x_original.max(), 100)
                            t_pval_right = (x_pval_right - (mu0 if selected_ht_type == 'One-Sample t-test' else 0)) / se
                            ax.fill_between(x_pval_right, stats.t.pdf(t_pval_right, df) / se, alpha=0.5, color='yellow')
                            
                    elif params['alternative'] == 'greater':
                        critical_val_t = stats.t.ppf(1 - alpha_level, df)
                        if selected_ht_type == 'One-Sample t-test':
                            critical_val = mu0 + critical_val_t * se
                        else:
                            critical_val = critical_val_t * se
                        
                        x_crit = np.linspace(critical_val, x_original.max(), 100)
                        t_crit = (x_crit - (mu0 if selected_ht_type == 'One-Sample t-test' else 0)) / se
                        ax.fill_between(x_crit, stats.t.pdf(t_crit, df) / se, alpha=0.3, color='red', label=f'Rejection region (α={alpha_level})')
                        
                        x_pval = np.linspace(actual_value, x_original.max(), 100)
                        t_pval = (x_pval - (mu0 if selected_ht_type == 'One-Sample t-test' else 0)) / se
                        ax.fill_between(x_pval, stats.t.pdf(t_pval, df) / se, alpha=0.5, color='yellow', label=f'p-value region')
                        
                    else:  # less
                        critical_val_t = stats.t.ppf(alpha_level, df)
                        if selected_ht_type == 'One-Sample t-test':
                            critical_val = mu0 + critical_val_t * se
                        else:
                            critical_val = critical_val_t * se
                        
                        x_crit = np.linspace(x_original.min(), critical_val, 100)
                        t_crit = (x_crit - (mu0 if selected_ht_type == 'One-Sample t-test' else 0)) / se
                        ax.fill_between(x_crit, stats.t.pdf(t_crit, df) / se, alpha=0.3, color='red', label=f'Rejection region (α={alpha_level})')
                        
                        x_pval = np.linspace(x_original.min(), actual_value, 100)
                        t_pval = (x_pval - (mu0 if selected_ht_type == 'One-Sample t-test' else 0)) / se
                        ax.fill_between(x_pval, stats.t.pdf(t_pval, df) / se, alpha=0.5, color='yellow', label=f'p-value region')
                    
                    # Mark test statistic on original scale
                    ax.axvline(actual_value, color='green', linestyle='--', linewidth=2, label=f'Sample statistic = {actual_value:.3f}')
                    
                    if selected_ht_type == 'One-Sample t-test':
                        ax.set_xlabel('Mean (μ)')
                        ax.axvline(mu0, color='gray', linestyle=':', linewidth=1.5, alpha=0.7, label=f'H₀: μ = {mu0}')
                    elif selected_ht_type == 'Two-Sample t-test (Independent Samples)':
                        ax.set_xlabel('Difference in Means (μ₁ - μ₂)')
                        ax.axvline(0, color='gray', linestyle=':', linewidth=1.5, alpha=0.7, label='H₀: μ₁ - μ₂ = 0')
                    else:
                        ax.set_xlabel('Mean Difference (μd)')
                        ax.axvline(0, color='gray', linestyle=':', linewidth=1.5, alpha=0.7, label='H₀: μd = 0')
                    
                    ax.set_ylabel('Probability Density')
                    ax.set_title(f'{selected_ht_type} Visualization')
                    
                elif selected_ht_type in ['One-Sample Z-test for Proportions', 'Two-Sample Z-test for Proportions']:
                    # Standard normal distribution - convert to proportion scale
                    if selected_ht_type == 'One-Sample Z-test for Proportions':
                        p0 = params['hypothesized_proportion']
                        n = params['num_trials']
                        p_hat = params['num_successes'] / n
                        se = np.sqrt(p0 * (1 - p0) / n)
                        
                        # Convert z-scores to proportion scale
                        z_range = np.linspace(-4, 4, 1000)
                        x_original = p0 + z_range * se
                        # Clip to valid proportion range [0, 1]
                        x_original = np.clip(x_original, 0, 1)
                        y = stats.norm.pdf(z_range) / se
                        ax.plot(x_original, y, 'b-', linewidth=2, label='Normal Approximation')
                        
                        actual_value = p_hat
                        center = p0
                        
                    else:  # Two-Sample Z-test for Proportions
                        p1_hat = params['num_successes1'] / params['num_trials1']
                        p2_hat = params['num_successes2'] / params['num_trials2']
                        n1, n2 = params['num_trials1'], params['num_trials2']
                        
                        # Pooled proportion under H0
                        p_pool = (params['num_successes1'] + params['num_successes2']) / (n1 + n2)
                        se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
                        
                        # Convert z-scores to difference in proportions scale
                        z_range = np.linspace(-4, 4, 1000)
                        x_original = z_range * se  # centered at 0 for H0: p1 - p2 = 0
                        # Clip to valid range [-1, 1]
                        x_original = np.clip(x_original, -1, 1)
                        y = stats.norm.pdf(z_range) / se
                        ax.plot(x_original, y, 'b-', linewidth=2, label='Normal Approximation')
                        
                        actual_value = p1_hat - p2_hat
                        center = 0
                    
                    # Determine critical values and shade regions on original scale
                    if params['alternative'] == 'two-sided':
                        critical_low_z = stats.norm.ppf(alpha_level/2)
                        critical_high_z = stats.norm.ppf(1 - alpha_level/2)
                        
                        critical_low = center + critical_low_z * se
                        critical_high = center + critical_high_z * se
                        
                        x_left = np.linspace(x_original.min(), critical_low, 100)
                        x_right = np.linspace(critical_high, x_original.max(), 100)
                        
                        z_left = (x_left - center) / se
                        z_right = (x_right - center) / se
                        ax.fill_between(x_left, stats.norm.pdf(z_left) / se, alpha=0.3, color='red', label=f'Rejection region (α={alpha_level})')
                        ax.fill_between(x_right, stats.norm.pdf(z_right) / se, alpha=0.3, color='red')
                        
                        # Shade p-value region
                        if actual_value < center:
                            x_pval_left = np.linspace(x_original.min(), actual_value, 100)
                            z_pval_left = (x_pval_left - center) / se
                            ax.fill_between(x_pval_left, stats.norm.pdf(z_pval_left) / se, alpha=0.5, color='yellow', label=f'p-value region')
                            
                            mirror_value = 2*center - actual_value
                            x_pval_right = np.linspace(mirror_value, x_original.max(), 100)
                            z_pval_right = (x_pval_right - center) / se
                            ax.fill_between(x_pval_right, stats.norm.pdf(z_pval_right) / se, alpha=0.5, color='yellow')
                        else:
                            mirror_value = 2*center - actual_value
                            x_pval_left = np.linspace(x_original.min(), mirror_value, 100)
                            z_pval_left = (x_pval_left - center) / se
                            ax.fill_between(x_pval_left, stats.norm.pdf(z_pval_left) / se, alpha=0.5, color='yellow', label=f'p-value region')
                            
                            x_pval_right = np.linspace(actual_value, x_original.max(), 100)
                            z_pval_right = (x_pval_right - center) / se
                            ax.fill_between(x_pval_right, stats.norm.pdf(z_pval_right) / se, alpha=0.5, color='yellow')
                            
                    elif params['alternative'] == 'greater':
                        critical_val_z = stats.norm.ppf(1 - alpha_level)
                        critical_val = center + critical_val_z * se
                        
                        x_crit = np.linspace(critical_val, x_original.max(), 100)
                        z_crit = (x_crit - center) / se
                        ax.fill_between(x_crit, stats.norm.pdf(z_crit) / se, alpha=0.3, color='red', label=f'Rejection region (α={alpha_level})')
                        
                        x_pval = np.linspace(actual_value, x_original.max(), 100)
                        z_pval = (x_pval - center) / se
                        ax.fill_between(x_pval, stats.norm.pdf(z_pval) / se, alpha=0.5, color='yellow', label=f'p-value region')
                        
                    else:  # less
                        critical_val_z = stats.norm.ppf(alpha_level)
                        critical_val = center + critical_val_z * se
                        
                        x_crit = np.linspace(x_original.min(), critical_val, 100)
                        z_crit = (x_crit - center) / se
                        ax.fill_between(x_crit, stats.norm.pdf(z_crit) / se, alpha=0.3, color='red', label=f'Rejection region (α={alpha_level})')
                        
                        x_pval = np.linspace(x_original.min(), actual_value, 100)
                        z_pval = (x_pval - center) / se
                        ax.fill_between(x_pval, stats.norm.pdf(z_pval) / se, alpha=0.5, color='yellow', label=f'p-value region')
                    
                    # Mark test statistic on original scale
                    ax.axvline(actual_value, color='green', linestyle='--', linewidth=2, label=f'Sample statistic = {actual_value:.4f}')
                    
                    if selected_ht_type == 'One-Sample Z-test for Proportions':
                        ax.set_xlabel('Proportion (p)')
                        ax.axvline(p0, color='gray', linestyle=':', linewidth=1.5, alpha=0.7, label=f'H₀: p = {p0}')
                    else:
                        ax.set_xlabel('Difference in Proportions (p₁ - p₂)')
                        ax.axvline(0, color='gray', linestyle=':', linewidth=1.5, alpha=0.7, label='H₀: p₁ - p₂ = 0')
                    
                    ax.set_ylabel('Probability Density')
                    ax.set_title(f'{selected_ht_type} Visualization')
                    
                elif selected_ht_type == 'Chi-Square Goodness-of-Fit Test' or selected_ht_type == 'Chi-Square Test of Independence':
                    # Chi-square distribution
                    if selected_ht_type == 'Chi-Square Goodness-of-Fit Test':
                        df = len([float(x.strip()) for x in params['observed_frequencies'].split(',') if x.strip()]) - 1
                    else:
                        df = degrees_freedom
                    
                    x = np.linspace(0, max(test_statistic * 1.5, stats.chi2.ppf(0.999, df)), 1000)
                    y = stats.chi2.pdf(x, df)
                    ax.plot(x, y, 'b-', linewidth=2, label=f'Chi-square distribution (df={df})')
                    
                    # Critical value (always right-tailed for chi-square)
                    critical_val = stats.chi2.ppf(1 - alpha_level, df)
                    x_crit = np.linspace(critical_val, max(test_statistic * 1.5, stats.chi2.ppf(0.999, df)), 100)
                    ax.fill_between(x_crit, stats.chi2.pdf(x_crit, df), alpha=0.3, color='red', label=f'Rejection region (α={alpha_level})')
                    
                    # Shade p-value region
                    x_pval = np.linspace(test_statistic, max(test_statistic * 1.5, stats.chi2.ppf(0.999, df)), 100)
                    ax.fill_between(x_pval, stats.chi2.pdf(x_pval, df), alpha=0.5, color='yellow', label=f'p-value region')
                    
                    ax.axvline(test_statistic, color='green', linestyle='--', linewidth=2, label=f'Test statistic = {test_statistic:.3f}')
                    ax.set_xlabel('χ² value')
                    ax.set_ylabel('Probability Density')
                    ax.set_title(f'{selected_ht_type} Visualization')
                    
                elif selected_ht_type == 'ANOVA (Analysis of Variance) F-test':
                    # F-distribution
                    k = len(params['group_data_cols'])  # number of groups
                    n = sum(len(get_data_from_col_string(col)) for col in params['group_data_cols'] if col)
                    df1 = k - 1  # between groups
                    df2 = n - k  # within groups
                    
                    x = np.linspace(0, max(test_statistic * 1.5, stats.f.ppf(0.999, df1, df2)), 1000)
                    y = stats.f.pdf(x, df1, df2)
                    ax.plot(x, y, 'b-', linewidth=2, label=f'F-distribution (df1={df1}, df2={df2})')
                    
                    # Critical value (always right-tailed for F-test)
                    critical_val = stats.f.ppf(1 - alpha_level, df1, df2)
                    x_crit = np.linspace(critical_val, max(test_statistic * 1.5, stats.f.ppf(0.999, df1, df2)), 100)
                    ax.fill_between(x_crit, stats.f.pdf(x_crit, df1, df2), alpha=0.3, color='red', label=f'Rejection region (α={alpha_level})')
                    
                    # Shade p-value region
                    x_pval = np.linspace(test_statistic, max(test_statistic * 1.5, stats.f.ppf(0.999, df1, df2)), 100)
                    ax.fill_between(x_pval, stats.f.pdf(x_pval, df1, df2), alpha=0.5, color='yellow', label=f'p-value region')
                    
                    ax.axvline(test_statistic, color='green', linestyle='--', linewidth=2, label=f'Test statistic = {test_statistic:.3f}')
                    ax.set_xlabel('F-value')
                    ax.set_ylabel('Probability Density')
                    ax.set_title(f'{selected_ht_type} Visualization')
                
                ax.legend(loc='best')
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()
            else:
                st.warning("Could not complete the hypothesis test. Check inputs and test type.")

        except ValueError as ve:
            st.error(f"Input Error: {ve}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

elif selected_tab == "Visualizations":
    st.header("Visualizations")

    if not st.session_state.global_dataframes:
        st.info("Please load or enter data in the 'Data Input' tab first to generate visualizations.")
    else:
        plot_type = st.selectbox(
            "Select Plot Type",
            options=['Histogram', 'Boxplot', 'Bar Plot', 'Dot Plot', 'Scatter Plot'],
            key="plot_type_select"
        )

        numeric_cols_options = [''] + get_numeric_columns()
        all_cols_options = [''] + get_all_columns()

        x_axis_col = None
        y_axis_col = None
        plot_options = {}

        if plot_type in ['Histogram', 'Boxplot', 'Dot Plot']:
            if plot_type == 'Boxplot':
                plot_options['multiple'] = st.checkbox("Plot multiple boxplots", value=False, key="boxplot_multiple")
                if plot_options['multiple']:
                    x_axis_col = st.multiselect("Select Data Columns", options=numeric_cols_options[1:], key="x_axis_select_multiple_numeric")
                else:
                    x_axis_col = st.selectbox("Select Data Column", options=numeric_cols_options, key="x_axis_select_single_numeric")
                plot_options['horizontal'] = st.radio("Orientation:", options=['Vertical', 'Horizontal'], index=0, key="boxplot_orientation") == 'Horizontal'
            else:
                x_axis_col = st.selectbox("Select Data Column", options=numeric_cols_options, key="x_axis_select_single_numeric")
            if plot_type == 'Histogram':
                # Calculate optimal number of bins using Sturges' rule
                optimal_bins = 'auto'  # Default to matplotlib's auto binning
                if x_axis_col:
                    try:
                        data_for_bins = get_data_from_col_string(x_axis_col)
                        n = len(data_for_bins)
                        # Sturges' rule: k = ceil(log2(n) + 1)
                        optimal_bins = int(np.ceil(np.log2(n) + 1))
                    except:
                        optimal_bins = 'auto'
                
                # Allow user to override with manual bin count or use 'auto'
                if isinstance(optimal_bins, int):
                    plot_options['bins'] = st.number_input("Number of Bins", min_value=1, max_value=100, value=optimal_bins, step=1, key="hist_bins")
                else:
                    # Use auto as default, but provide option to manually specify
                    manual_bins = st.checkbox("Manually specify number of bins", value=False, key="manual_bins_checkbox")
                    if manual_bins:
                        plot_options['bins'] = st.number_input("Number of Bins", min_value=1, max_value=100, value=10, step=1, key="hist_bins")
                    else:
                        plot_options['bins'] = 'auto'
                        st.caption("Using automatic bin selection (Sturges' rule)")
                
                plot_options['force_integer_bins'] = st.checkbox("Use integer bin boundaries", value=False, key="force_integer_bins")
                plot_options['use_relative'] = st.radio("Y-axis:", options=['Frequency', 'Relative Frequency'], index=0, key="hist_yaxis") == 'Relative Frequency'
        elif plot_type == 'Bar Plot':
            x_axis_col = st.selectbox("Select Data Column (Categorical/Numeric)", options=all_cols_options, key="x_axis_select_single_all")
            plot_options['stacked'] = st.radio("Bar Style:", options=['Unstacked (Grouped)', 'Stacked'], index=0, key="bar_plot_style") == 'Stacked'
            plot_options['use_relative'] = st.radio("Y-axis:", options=['Frequency', 'Relative Frequency'], index=0, key="bar_plot_yaxis") == 'Relative Frequency'
        elif plot_type == 'Scatter Plot':
            col1, col2 = st.columns(2)
            with col1:
                x_axis_col = st.selectbox("Select X-axis Variable", options=numeric_cols_options, key="x_axis_select_scatter")
            with col2:
                y_axis_col = st.selectbox("Select Y-axis Variable", options=numeric_cols_options, key="y_axis_select_scatter")

        if st.button("Generate Plot", key="generate_plot_button"):
            st.subheader("Generated Plot")
            try:
                fig = None
                if plot_type == 'Histogram':
                    if not x_axis_col: raise ValueError("Please select a data column for the histogram.")
                    data = get_data_from_col_string(x_axis_col)
                    # Extract column name - handle both "key: value" format and plain column names
                    col_label = x_axis_col.split(": ", 1)[1] if ": " in x_axis_col else x_axis_col
                    fig = plot_histogram(data, bins=plot_options['bins'], title=f'Histogram of {col_label}', xlabel=col_label, use_relative=plot_options.get('use_relative', False), force_integer_bins=plot_options.get('force_integer_bins', False))
                elif plot_type == 'Boxplot':
                    if not x_axis_col: raise ValueError("Please select at least one data column for the boxplot.")
                    if plot_options.get('multiple', False):
                        # Multiple boxplots
                        if isinstance(x_axis_col, list) and len(x_axis_col) > 0:
                            data_list = [get_data_from_col_string(col) for col in x_axis_col]
                            labels = [col.split(": ", 1)[1] if ": " in col else col for col in x_axis_col]
                            fig = plot_box_plot(data_list, title='Box Plots Comparison', ylabel='Value', horizontal=plot_options.get('horizontal', False), labels=labels)
                        else:
                            raise ValueError("Please select at least one data column for the boxplot.")
                    else:
                        # Single boxplot
                        data = get_data_from_col_string(x_axis_col)
                        col_label = x_axis_col.split(": ", 1)[1] if ": " in x_axis_col else x_axis_col
                        fig = plot_box_plot(data, title=f'Box Plot of {col_label}', ylabel=col_label, horizontal=plot_options.get('horizontal', False))
                elif plot_type == 'Bar Plot':
                    if not x_axis_col: raise ValueError("Please select a data column for the bar plot.")
                    df_name, col_name = x_axis_col.split(': ', 1)
                    df = st.session_state.global_dataframes.get(df_name)
                    if df is None: raise ValueError(f"DataFrame '{df_name}' not found.")
                    data = df[col_name].dropna() # Bar plot can use non-numeric directly
                    if data.empty: raise ValueError(f"Selected column '{col_name}' is empty after dropping NaNs.")
                    fig = plot_bar_plot(data, title=f'Bar Plot of {col_name}', xlabel=col_name, stacked=plot_options.get('stacked', False), use_relative=plot_options.get('use_relative', False))
                elif plot_type == 'Dot Plot':
                    if not x_axis_col: raise ValueError("Please select a data column for the dot plot.")
                    data = get_data_from_col_string(x_axis_col)
                    col_label = x_axis_col.split(": ", 1)[1] if ": " in x_axis_col else x_axis_col
                    fig = plot_dot_plot(data, title=f'Dot Plot of {col_label}', xlabel=col_label)
                elif plot_type == 'Scatter Plot':
                    if not x_axis_col or not y_axis_col: raise ValueError("Please select both X and Y axis variables.")
                    df_name_x, col_name_x = x_axis_col.split(': ', 1)
                    df_name_y, col_name_y = y_axis_col.split(': ', 1)
                    if df_name_x != df_name_y: raise ValueError("For Scatter Plot, X and Y variables must come from the same DataFrame.")
                    
                    source_df = st.session_state.global_dataframes.get(df_name_x)
                    if source_df is None: raise ValueError(f"DataFrame '{df_name_x}' not found.")

                    combined_series = pd.DataFrame({
                        'x_val': pd.to_numeric(source_df[col_name_x], errors='coerce'),
                        'y_val': pd.to_numeric(source_df[col_name_y], errors='coerce')
                    }).dropna()

                    if combined_series.empty:
                        raise ValueError("No common numeric data points found for X and Y axes after cleaning.")
                    
                    fig = plot_scatter_plot(combined_series['x_val'], combined_series['y_val'], title=f'Scatter Plot: {col_name_x} vs {col_name_y}', xlabel=col_name_x, ylabel=col_name_y)

                if fig is not None:
                    st.pyplot(fig)

            except ValueError as ve:
                st.error(f"Plotting Error: {ve}")
            except Exception as e:
                st.error(f"An unexpected error occurred during plotting: {e}")

elif selected_tab == "Linear Regression":
    st.header("Linear Regression")

    if not st.session_state.global_dataframes:
        st.info("Please load or enter data in the 'Data Input' tab first to perform linear regression.")
    else:
        numeric_cols_options = [''] + get_numeric_columns()

        col1, col2 = st.columns(2)
        with col1:
            lr_x_axis_selector = st.selectbox("Select X-axis Variable (Independent)", options=numeric_cols_options, key="lr_x_axis_select")
        with col2:
            lr_y_axis_selector = st.selectbox("Select Y-axis Variable (Dependent)", options=numeric_cols_options, key="lr_y_axis_select")

        if st.button("Calculate Linear Regression", key="calc_lr_button"):
            st.subheader("Linear Regression Results")
            try:
                if not lr_x_axis_selector: raise ValueError("Please select an X-axis variable.")
                if not lr_y_axis_selector: raise ValueError("Please select a Y-axis variable.")

                df_name_x, col_name_x = lr_x_axis_selector.split(': ', 1)
                df_name_y, col_name_y = lr_y_axis_selector.split(': ', 1)

                if df_name_x != df_name_y:
                    raise ValueError("X and Y variables must come from the same DataFrame for Linear Regression.")

                source_df = st.session_state.global_dataframes.get(df_name_x)
                if source_df is None: raise ValueError(f"DataFrame '{df_name_x}' not found.")

                # Use get_data_from_col_string which also handles dropping NaNs and type conversion
                x_data = get_data_from_col_string(lr_x_axis_selector)
                y_data = get_data_from_col_string(lr_y_axis_selector)

                # Ensure that x_data and y_data correspond to the same rows after cleaning
                # This is important if original DataFrame had NaNs at different positions.
                # Re-create a temporary DataFrame to align indices and drop NaNs commonly.
                combined_data = pd.DataFrame({'x': pd.to_numeric(source_df[col_name_x], errors='coerce'),
                                              'y': pd.to_numeric(source_df[col_name_y], errors='coerce')}).dropna()
                if combined_data.empty:
                    raise ValueError("No common numeric data points found for X and Y axes after cleaning.")

                cleaned_x = combined_data['x']
                cleaned_y = combined_data['y']

                r_value, r_squared, regression_equation, fig = perform_linear_regression_analysis(
                    cleaned_x, cleaned_y,
                    title=f'Linear Regression: {col_name_y} vs {col_name_x}',
                    xlabel=col_name_x, ylabel=col_name_y
                )

                st.write(f"**Correlation Coefficient (r)**: {r_value:.4f}")
                st.write(f"**Coefficient of Determination (R²)**: {r_squared:.4f}")
                st.write(f"**Regression Equation**: {regression_equation}")
                st.pyplot(fig)
                # Accessibility: Add text alternative for screen readers
                st.caption(f"Linear regression scatter plot with fitted line. X-axis: {col_name_x}, Y-axis: {col_name_y}. "
                          f"Correlation r={r_value:.4f}, R²={r_squared:.4f}. {regression_equation}")
            except ValueError as ve:
                st.error(f"Input Error: {ve}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

elif selected_tab == "Simulations":
    st.header("Simulations")
    
    # Create tabs for different simulations
    sim_tabs = st.tabs(["Binomial Approximation", "Sample Means", "Sample Proportions", "Unusual Proportions", "Confidence Intervals", "Hypothesis Testing", "Two Proportions", "Two Means", "t vs Normal", "F-Statistic Explorer"])
    
    with sim_tabs[0]:
        st.subheader("Normal Approximation of the Binomial Distribution")
        st.write("""
        This simulation helps you explore how the binomial distribution approaches a normal distribution 
        as the sample size increases. This is a key concept in statistics known as the **Central Limit Theorem**.
        """)
        
        # Create input columns
        col1, col2 = st.columns(2)
        
        with col1:
            n_trials = st.slider(
                "Number of Trials (n)", 
                min_value=5, 
                max_value=500, 
                value=30,
                help="Move the slider to see how the number of trials affects the approximation"
            )
        
        with col2:
            p_prob = st.number_input(
                "Probability of Success (p)", 
                min_value=0.01, 
                max_value=0.99, 
                value=0.5, 
                step=0.01,
                format="%.2f",
                help="The probability of success on each trial"
            )
        
        # Plot updates automatically (no button needed)
        try:
            # Calculate binomial distribution
            x_values = np.arange(0, n_trials + 1)
            binomial_pmf = stats.binom.pmf(x_values, n=n_trials, p=p_prob)
            
            # Calculate normal approximation
            mean = n_trials * p_prob
            std_dev = np.sqrt(n_trials * p_prob * (1 - p_prob))
            
            # Create continuous x values for normal curve
            x_continuous = np.linspace(0, n_trials, 1000)
            normal_pdf = stats.norm.pdf(x_continuous, loc=mean, scale=std_dev)
            
            # Create the plot
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Plot binomial distribution as vertical lines
            markerline, stemlines, baseline = ax.stem(x_values, binomial_pmf, linefmt='steelblue', 
                                                       markerfmt='o', basefmt=' ',
                                                       label=f'Binomial(n={n_trials}, p={p_prob})')
            plt.setp(stemlines, 'linewidth', 2)
            plt.setp(markerline, 'markersize', 6, 'markerfacecolor', 'steelblue', 'markeredgecolor', 'steelblue')
            
            # Plot normal approximation as a curve
            ax.plot(x_continuous, normal_pdf, 'r-', linewidth=2, 
                    label=f'Normal(μ={mean:.2f}, σ={std_dev:.2f})')
            
            # Add labels and title
            ax.set_xlabel('Number of Successes', fontsize=12)
            ax.set_ylabel('Probability', fontsize=12)
            ax.set_title(f'Binomial Distribution vs Normal Approximation\n(n={n_trials}, p={p_prob})', 
                        fontsize=14, fontweight='bold')
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
            
            # Display the plot
            st.pyplot(fig)
            
            # Add interpretation
            st.write("---")
            st.subheader("Interpretation")
            st.write(f"**Mean (μ)**: {mean:.2f}")
            st.write(f"**Standard Deviation (σ)**: {std_dev:.2f}")
            
            # Check if normal approximation is appropriate
            np_value = n_trials * p_prob
            nq_value = n_trials * (1 - p_prob)
            
            if np_value >= 10 and nq_value >= 10:
                st.success(f"✓ Normal approximation is appropriate: np = {np_value:.2f} ≥ 10 and n(1-p) = {nq_value:.2f} ≥ 10")
            else:
                st.warning(f"⚠ Normal approximation may not be accurate: np = {np_value:.2f} and n(1-p) = {nq_value:.2f}")
                st.write("**Rule of thumb**: The normal approximation works well when both np ≥ 10 and n(1-p) ≥ 10")
            
            st.write("""
            **What to observe:**
            - As the number of trials increases, the binomial distribution becomes more symmetric and bell-shaped
            - The normal curve (red line) approximates the binomial bars more closely with larger sample sizes
            - When p is close to 0.5, the approximation works better for smaller sample sizes
            """)
            
        except Exception as e:
            st.error(f"An error occurred while generating the plot: {e}")
    
    with sim_tabs[1]:
        st.subheader("Sampling Distribution of Sample Means")
        st.write("""
        This simulation demonstrates the **Central Limit Theorem** for sample means. It shows how the 
        sampling distribution of sample means becomes approximately normal, regardless of the shape of 
        the population distribution, as the sample size increases.
        """)
        
        # Create input columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pop_dist_type = st.selectbox(
                "Population Distribution",
                options=["Normal", "Right Skewed (Exponential)", "Left Skewed (Beta)", "Uniform", "Bimodal"],
                help="Choose the shape of the population distribution"
            )
        
        with col2:
            sample_size_means = st.slider(
                "Sample Size (n)", 
                min_value=2, 
                max_value=100, 
                value=30,
                help="The size of each random sample"
            )
        
        with col3:
            num_samples_means = st.number_input(
                "Number of Samples", 
                min_value=100, 
                max_value=5000, 
                value=1000,
                step=100,
                help="How many samples to draw from the population"
            )
        
        if st.button("Run Simulation", key="sampling_means_button"):
            try:
                # Generate population based on selected distribution
                pop_size = 100000
                
                if pop_dist_type == "Normal":
                    population = np.random.normal(loc=50, scale=15, size=pop_size)
                    pop_color = 'steelblue'
                elif pop_dist_type == "Right Skewed (Exponential)":
                    population = np.random.exponential(scale=20, size=pop_size)
                    pop_color = 'coral'
                elif pop_dist_type == "Left Skewed (Beta)":
                    population = np.random.beta(a=8, b=2, size=pop_size) * 100
                    pop_color = 'mediumpurple'
                elif pop_dist_type == "Uniform":
                    population = np.random.uniform(low=0, high=100, size=pop_size)
                    pop_color = 'lightgreen'
                else:  # Bimodal
                    pop1 = np.random.normal(loc=30, scale=8, size=pop_size//2)
                    pop2 = np.random.normal(loc=70, scale=8, size=pop_size//2)
                    population = np.concatenate([pop1, pop2])
                    pop_color = 'gold'
                
                # Calculate population parameters
                pop_mean = np.mean(population)
                pop_std = np.std(population)
                
                # Create placeholders for progressive updates
                progress_bar = st.progress(0)
                status_text = st.empty()
                plot_placeholder = st.empty()
                stats_placeholder = st.empty()
                
                # Store sample means
                sample_means = []
                
                # Generate samples in batches
                batch_size = 100
                num_batches = int(np.ceil(num_samples_means / batch_size))
                
                for batch in range(num_batches):
                    # Update progress
                    progress = (batch + 1) / num_batches
                    progress_bar.progress(progress)
                    status_text.text(f"Generating samples... {int(progress * 100)}%")
                    
                    # Generate batch of samples
                    samples_in_batch = min(batch_size, num_samples_means - batch * batch_size)
                    
                    for _ in range(samples_in_batch):
                        # Draw a random sample from the population
                        sample = np.random.choice(population, size=sample_size_means, replace=False)
                        sample_mean = np.mean(sample)
                        sample_means.append(sample_mean)
                    
                    # Update plot every few batches
                    if (batch + 1) % 3 == 0 or batch == num_batches - 1:
                        with plot_placeholder.container():
                            # Create figure with two subplots
                            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
                            
                            # Plot 1: Population Distribution
                            ax1.hist(population, bins=60, density=True, alpha=0.7, color=pop_color, 
                                    edgecolor='black', label='Population Distribution')
                            ax1.axvline(pop_mean, color='darkred', linestyle='--', linewidth=2, 
                                       label=f'Population Mean = {pop_mean:.2f}')
                            ax1.set_xlabel('Value', fontsize=11)
                            ax1.set_ylabel('Density', fontsize=11)
                            ax1.set_title(f'Population Distribution: {pop_dist_type}', fontsize=12, fontweight='bold')
                            ax1.legend(loc='best')
                            ax1.grid(True, alpha=0.3)
                            
                            # Plot 2: Sampling Distribution of Sample Means
                            ax2.hist(sample_means, bins=40, density=True, alpha=0.7, color='steelblue', 
                                    edgecolor='black', label='Sample Means')
                            
                            # Overlay theoretical normal distribution
                            theoretical_mean = pop_mean
                            theoretical_std = pop_std / np.sqrt(sample_size_means)
                            x_range = np.linspace(min(sample_means), max(sample_means), 200)
                            normal_curve = stats.norm.pdf(x_range, loc=theoretical_mean, scale=theoretical_std)
                            ax2.plot(x_range, normal_curve, 'r-', linewidth=2, 
                                    label=f'Normal(μ={theoretical_mean:.2f}, σ={theoretical_std:.2f})')
                            
                            # Mark the mean
                            mean_of_means = np.mean(sample_means)
                            ax2.axvline(mean_of_means, color='orange', linestyle=':', linewidth=2, 
                                       label=f'Mean of Sample Means = {mean_of_means:.2f}')
                            ax2.axvline(pop_mean, color='darkred', linestyle='--', linewidth=2, 
                                       label=f'Population Mean = {pop_mean:.2f}')
                            
                            ax2.set_xlabel('Sample Mean', fontsize=11)
                            ax2.set_ylabel('Density', fontsize=11)
                            ax2.set_title(f'Sampling Distribution of Sample Means (n={sample_size_means})', 
                                         fontsize=12, fontweight='bold')
                            ax2.legend(loc='best', fontsize=9)
                            ax2.grid(True, alpha=0.3)
                            
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close()
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Display final statistics
                with stats_placeholder.container():
                    st.write("---")
                    st.subheader("Summary Statistics")
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("Population Mean (μ)", f"{pop_mean:.2f}")
                        st.metric("Population Std Dev (σ)", f"{pop_std:.2f}")
                    
                    with col_b:
                        mean_of_means = np.mean(sample_means)
                        std_of_means = np.std(sample_means, ddof=1)
                        st.metric("Mean of Sample Means", f"{mean_of_means:.2f}")
                        st.metric("Std Dev of Sample Means", f"{std_of_means:.2f}")
                    
                    with col_c:
                        theoretical_mean = pop_mean
                        theoretical_std = pop_std / np.sqrt(sample_size_means)
                        st.metric("Expected Mean", f"{theoretical_mean:.2f}")
                        st.metric("Expected Std Dev (σ/√n)", f"{theoretical_std:.2f}")
                    
                    st.write("---")
                    st.write("**Central Limit Theorem Observations:**")
                    st.write(f"- The mean of sample means ({mean_of_means:.2f}) is approximately equal to the population mean ({pop_mean:.2f})")
                    st.write(f"- The standard deviation of sample means ({std_of_means:.2f}) is approximately σ/√n = {theoretical_std:.2f}")
                    st.write(f"- Even though the population distribution is **{pop_dist_type}**, the sampling distribution")
                    st.write(f"  of sample means appears approximately **normal** (especially with larger sample sizes)")
                    st.write(f"- Larger sample sizes (n) → narrower sampling distribution → more precise estimates")
                    
                    st.write("---")
                    st.info("""
                    **Key Insight**: The Central Limit Theorem states that the sampling distribution of sample means 
                    will be approximately normal, regardless of the population distribution shape, when the sample 
                    size is sufficiently large (typically n ≥ 30). Try different distributions and sample sizes 
                    to see this in action!
                    """)
                
            except Exception as e:
                st.error(f"An error occurred while running the simulation: {e}")
    
    with sim_tabs[2]:
        st.subheader("Sampling Distribution of Sample Proportions")
        st.write("""
        This simulation demonstrates how sample proportions from repeated random samples form a distribution 
        centered around the true population proportion. This illustrates the **Central Limit Theorem for Proportions**.
        """)
        
        # Create input columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pop_proportion = st.number_input(
                "Population Proportion (p)", 
                min_value=0.01, 
                max_value=0.99, 
                value=0.6, 
                step=0.01,
                format="%.2f",
                help="The true proportion in the population"
            )
        
        with col2:
            sample_size = st.slider(
                "Sample Size (n)", 
                min_value=10, 
                max_value=500, 
                value=50,
                help="The size of each random sample"
            )
        
        with col3:
            num_samples = st.slider(
                "Number of Samples", 
                min_value=10, 
                max_value=1000, 
                value=100,
                step=10,
                help="How many samples to draw from the population"
            )
        
        # Add a button to run the simulation
        if st.button("Run Simulation", key="sampling_dist_button"):
            try:
                # Initialize session state for animation if not exists
                if 'sample_proportions' not in st.session_state:
                    st.session_state.sample_proportions = []
                
                # Create placeholders for dynamic updates
                sample_viz_placeholder = st.empty()
                dist_plot_placeholder = st.empty()
                stats_placeholder = st.empty()
                
                # Store all sample proportions
                sample_proportions = []
                
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate drawing samples
                for i in range(num_samples):
                    # Draw a random sample (1 = success, 0 = failure)
                    sample = np.random.binomial(1, pop_proportion, sample_size)
                    sample_prop = np.mean(sample)
                    sample_proportions.append(sample_prop)
                    
                    # Update progress
                    progress = (i + 1) / num_samples
                    progress_bar.progress(progress)
                    status_text.text(f"Drawing sample {i+1} of {num_samples}...")
                    
                    # Show visualization of current sample every 10 samples or on last sample
                    if (i + 1) % max(1, num_samples // 20) == 0 or i == num_samples - 1:
                        # Visualize the current sample
                        with sample_viz_placeholder.container():
                            st.write("---")
                            st.write(f"**Current Sample #{i+1}**: Sample Proportion = {sample_prop:.4f}")
                            
                            # Create a visual representation of the sample
                            fig_sample, ax_sample = plt.subplots(figsize=(12, 2))
                            
                            # Show first 100 observations max for visualization
                            display_sample = sample[:min(100, len(sample))]
                            colors = ['green' if x == 1 else 'red' for x in display_sample]
                            x_pos = np.arange(len(display_sample))
                            
                            ax_sample.scatter(x_pos, [0.5] * len(display_sample), c=colors, s=50, alpha=0.7)
                            ax_sample.set_ylim(0, 1)
                            ax_sample.set_xlim(-1, len(display_sample))
                            ax_sample.set_yticks([])
                            ax_sample.set_xlabel('Observation Number', fontsize=10)
                            ax_sample.set_title(f'Sample Visualization (Green = Success, Red = Failure) - Showing {len(display_sample)} of {sample_size} observations', 
                                              fontsize=11, fontweight='bold')
                            ax_sample.grid(True, alpha=0.3, axis='x')
                            
                            st.pyplot(fig_sample)
                            plt.close(fig_sample)
                        
                        # Update sampling distribution plot
                        with dist_plot_placeholder.container():
                            st.write("---")
                            st.write("**Sampling Distribution of Sample Proportions**")
                            
                            fig_dist, ax_dist = plt.subplots(figsize=(12, 6))
                            
                            # Plot histogram of sample proportions
                            ax_dist.hist(sample_proportions, bins=min(30, max(10, len(sample_proportions)//5)), 
                                        color='steelblue', alpha=0.7, edgecolor='black', density=True,
                                        label=f'Sample Proportions (n={len(sample_proportions)})')
                            
                            # Overlay theoretical normal distribution
                            if len(sample_proportions) > 1:
                                mean_prop = pop_proportion
                                std_prop = np.sqrt(pop_proportion * (1 - pop_proportion) / sample_size)
                                
                                x_norm = np.linspace(max(0, mean_prop - 4*std_prop), 
                                                    min(1, mean_prop + 4*std_prop), 1000)
                                y_norm = stats.norm.pdf(x_norm, mean_prop, std_prop)
                                
                                ax_dist.plot(x_norm, y_norm, 'r-', linewidth=2, 
                                           label=f'Theoretical N(μ={mean_prop:.3f}, σ={std_prop:.4f})')
                            
                            # Add vertical line at population proportion
                            ax_dist.axvline(pop_proportion, color='green', linestyle='--', linewidth=2, 
                                          label=f'Population Proportion (p={pop_proportion})')
                            
                            # Add vertical line at mean of sample proportions
                            if len(sample_proportions) > 0:
                                ax_dist.axvline(np.mean(sample_proportions), color='orange', linestyle='--', linewidth=2,
                                              label=f'Mean of Sample Proportions ({np.mean(sample_proportions):.4f})')
                            
                            ax_dist.set_xlabel('Sample Proportion', fontsize=12)
                            ax_dist.set_ylabel('Density', fontsize=12)
                            ax_dist.set_title('Sampling Distribution of Sample Proportions', 
                                            fontsize=14, fontweight='bold')
                            ax_dist.legend(fontsize=9)
                            ax_dist.grid(True, alpha=0.3)
                            
                            st.pyplot(fig_dist)
                            plt.close(fig_dist)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Display final statistics
                with stats_placeholder.container():
                    st.write("---")
                    st.subheader("Summary Statistics")
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("Population Proportion (p)", f"{pop_proportion:.4f}")
                        st.metric("Sample Size (n)", sample_size)
                    
                    with col_b:
                        mean_sample_props = np.mean(sample_proportions)
                        st.metric("Mean of Sample Proportions", f"{mean_sample_props:.4f}")
                        st.metric("Standard Deviation of Sample Proportions", f"{np.std(sample_proportions, ddof=1):.4f}")
                    
                    with col_c:
                        theoretical_mean = pop_proportion
                        theoretical_std = np.sqrt(pop_proportion * (1 - pop_proportion) / sample_size)
                        st.metric("Theoretical Mean", f"{theoretical_mean:.4f}")
                        st.metric("Theoretical Std Dev", f"{theoretical_std:.4f}")
                    
                    st.write("---")
                    st.write("**Key Observations:**")
                    st.write(f"- The mean of sample proportions ({mean_sample_props:.4f}) should be close to the population proportion ({pop_proportion:.4f})")
                    st.write(f"- The standard deviation of sample proportions is approximately {theoretical_std:.4f}")
                    st.write(f"- As sample size increases, the sampling distribution becomes narrower (smaller standard deviation)")
                    st.write(f"- The sampling distribution is approximately normal when np ≥ 10 and n(1-p) ≥ 10")
                    
                    # Check conditions for normality
                    np_check = sample_size * pop_proportion
                    nq_check = sample_size * (1 - pop_proportion)
                    
                    if np_check >= 10 and nq_check >= 10:
                        st.success(f"✓ Conditions met for normal approximation: np = {np_check:.1f} ≥ 10 and n(1-p) = {nq_check:.1f} ≥ 10")
                    else:
                        st.warning(f"⚠ Conditions not fully met: np = {np_check:.1f} and n(1-p) = {nq_check:.1f}")
                
            except Exception as e:
                st.error(f"An error occurred while running the simulation: {e}")
    
    with sim_tabs[3]:
        st.subheader("Unusual Sample Proportions")
        st.write("""
        This simulation helps you determine if a sample proportion is unusual given a population proportion. 
        A sample proportion is typically considered unusual if it falls more than **2 standard errors** away 
        from the population proportion (approximately outside the 95% confidence region).
        """)
        
        # Create input columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pop_prop = st.number_input(
                "Population Proportion (p)", 
                min_value=0.01, 
                max_value=0.99, 
                value=0.5, 
                step=0.01,
                format="%.3f",
                help="The assumed or known population proportion",
                key="unusual_pop_prop"
            )
        
        with col2:
            sample_prop = st.number_input(
                "Sample Proportion (p̂)", 
                min_value=0.0, 
                max_value=1.0, 
                value=0.65, 
                step=0.01,
                format="%.3f",
                help="The proportion observed in your sample",
                key="unusual_sample_prop"
            )
        
        with col3:
            samp_size = st.number_input(
                "Sample Size (n)", 
                min_value=10, 
                max_value=10000, 
                value=100, 
                step=10,
                help="The size of your sample",
                key="unusual_sample_size"
            )
        
        # Calculate and plot automatically
        try:
            # Check conditions for normal approximation
            np_val = samp_size * pop_prop
            nq_val = samp_size * (1 - pop_prop)
            
            if np_val < 10 or nq_val < 10:
                st.warning(f"⚠ **Note**: Normal approximation may not be accurate. np = {np_val:.1f} and n(1-p) = {nq_val:.1f}. Both should be ≥ 10.")
            
            # Calculate standard error
            standard_error = np.sqrt(pop_prop * (1 - pop_prop) / samp_size)
            
            # Calculate z-score
            z_score = (sample_prop - pop_prop) / standard_error
            
            # Calculate bounds for ±2 SE
            lower_bound_2se = pop_prop - 2 * standard_error
            upper_bound_2se = pop_prop + 2 * standard_error
            
            # Create the plot
            fig, ax = plt.subplots(figsize=(12, 7))
            
            # Create x values for the normal curve
            x_min = max(0, pop_prop - 4 * standard_error)
            x_max = min(1, pop_prop + 4 * standard_error)
            x_values = np.linspace(x_min, x_max, 1000)
            
            # Calculate normal distribution values
            y_values = stats.norm.pdf(x_values, loc=pop_prop, scale=standard_error)
            
            # Plot the normal curve
            ax.plot(x_values, y_values, 'b-', linewidth=2, label='Sampling Distribution')
            
            # Shade the region within ±2 SE (usual region)
            x_fill = x_values[(x_values >= lower_bound_2se) & (x_values <= upper_bound_2se)]
            y_fill = stats.norm.pdf(x_fill, loc=pop_prop, scale=standard_error)
            ax.fill_between(x_fill, y_fill, alpha=0.3, color='green', 
                           label=f'Within 2 SE (Usual)\n[{lower_bound_2se:.4f}, {upper_bound_2se:.4f}]')
            
            # Shade unusual regions (beyond ±2 SE)
            x_left = x_values[x_values < lower_bound_2se]
            if len(x_left) > 0:
                y_left = stats.norm.pdf(x_left, loc=pop_prop, scale=standard_error)
                ax.fill_between(x_left, y_left, alpha=0.3, color='red', label='Unusual (Below -2 SE)')
            
            x_right = x_values[x_values > upper_bound_2se]
            if len(x_right) > 0:
                y_right = stats.norm.pdf(x_right, loc=pop_prop, scale=standard_error)
                ax.fill_between(x_right, y_right, alpha=0.3, color='red', label='Unusual (Above +2 SE)')
            
            # Mark the population proportion
            ax.axvline(pop_prop, color='blue', linestyle='--', linewidth=2, 
                      label=f'Population Proportion (p={pop_prop:.3f})')
            
            # Mark the ±2 SE bounds
            ax.axvline(lower_bound_2se, color='orange', linestyle=':', linewidth=1.5, 
                      label=f'-2 SE = {lower_bound_2se:.4f}')
            ax.axvline(upper_bound_2se, color='orange', linestyle=':', linewidth=1.5, 
                      label=f'+2 SE = {upper_bound_2se:.4f}')
            
            # Mark the sample proportion
            y_max = max(y_values)
            ax.axvline(sample_prop, color='red' if abs(z_score) > 2 else 'green', 
                      linestyle='-', linewidth=3, alpha=0.8,
                      label=f'Sample Proportion (p̂={sample_prop:.3f})')
            
            # Add a marker at the top for the sample proportion
            ax.plot(sample_prop, y_max * 1.05, 'v', 
                   color='red' if abs(z_score) > 2 else 'green', 
                   markersize=15, markeredgecolor='black', markeredgewidth=1.5)
            
            # Labels and title
            ax.set_xlabel('Sample Proportion', fontsize=12)
            ax.set_ylabel('Probability Density', fontsize=12)
            ax.set_title('Is the Sample Proportion Unusual?\nSampling Distribution of Sample Proportions', 
                        fontsize=14, fontweight='bold')
            ax.legend(fontsize=9, loc='upper right')
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            plt.close(fig)
            
            # Display statistics and interpretation
            st.write("---")
            st.subheader("Analysis")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("Standard Error (SE)", f"{standard_error:.4f}")
                st.metric("2 × SE", f"{2 * standard_error:.4f}")
            
            with col_b:
                st.metric("Z-Score", f"{z_score:.3f}")
                st.metric("Distance from p", f"{abs(sample_prop - pop_prop):.4f}")
            
            with col_c:
                st.metric("Lower Bound (-2 SE)", f"{lower_bound_2se:.4f}")
                st.metric("Upper Bound (+2 SE)", f"{upper_bound_2se:.4f}")
            
            st.write("---")
            st.subheader("Interpretation")
            
            # Determine if unusual
            if abs(z_score) > 2:
                st.error(f"🔴 **The sample proportion ({sample_prop:.3f}) is UNUSUAL**")
                st.write(f"The sample proportion is **{abs(z_score):.2f} standard errors** away from the population proportion.")
                st.write(f"This falls **outside** the usual range of ±2 SE from the population proportion.")
                if z_score > 2:
                    st.write(f"📈 The sample proportion is **significantly higher** than expected.")
                else:
                    st.write(f"📉 The sample proportion is **significantly lower** than expected.")
            else:
                st.success(f"🟢 **The sample proportion ({sample_prop:.3f}) is NOT unusual**")
                st.write(f"The sample proportion is only **{abs(z_score):.2f} standard errors** away from the population proportion.")
                st.write(f"This falls **within** the usual range of ±2 SE from the population proportion.")
                st.write(f"✓ This difference could easily occur by random chance.")
            
            st.write("---")
            st.write("**Rule of Thumb:**")
            st.write("- If |z-score| > 2: The sample proportion is considered **unusual** (roughly outside the 95% range)")
            st.write("- If |z-score| ≤ 2: The sample proportion is considered **usual** (within the 95% range)")
            st.write("- Standard Error (SE) = √[p(1-p)/n]")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
    
    with sim_tabs[4]:
        st.subheader("Confidence Interval Explorer for Proportions")
        st.write("""
        This simulation helps you understand how confidence intervals work. A confidence interval constructed 
        around a **sample proportion** will capture the **true population proportion** a certain percentage of the time 
        (e.g., 95% of the time for a 95% confidence interval).
        """)
        
        # Create input columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ci_pop_prop = st.number_input(
                "True Population Proportion (p)", 
                min_value=0.01, 
                max_value=0.99, 
                value=0.6, 
                step=0.01,
                format="%.3f",
                help="The true (but usually unknown) population proportion",
                key="ci_pop_prop"
            )
        
        with col2:
            ci_sample_size = st.number_input(
                "Sample Size (n)", 
                min_value=10, 
                max_value=1000, 
                value=100, 
                step=10,
                help="The size of your sample",
                key="ci_sample_size"
            )
        
        with col3:
            confidence_level = st.selectbox(
                "Confidence Level",
                options=[0.90, 0.95, 0.99],
                index=1,
                format_func=lambda x: f"{int(x*100)}%",
                help="The confidence level for the interval",
                key="ci_confidence_level"
            )
        
        # Calculate z-critical value based on confidence level
        z_critical = stats.norm.ppf((1 + confidence_level) / 2)
        
        # Calculate margin of error based on population proportion
        standard_error = np.sqrt(ci_pop_prop * (1 - ci_pop_prop) / ci_sample_size)
        margin_of_error = z_critical * standard_error
        
        st.write("---")
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.info(f"**Z-critical value**: {z_critical:.3f}")
            st.info(f"**Standard Error**: {standard_error:.4f}")
        with col_info2:
            st.info(f"**Margin of Error**: ±{margin_of_error:.4f}")
            st.info(f"**Formula**: ME = z* × √[p(1-p)/n]")
        
        # Calculate confidence interval around the population proportion (for reference)
        pop_ci_lower = ci_pop_prop - margin_of_error
        pop_ci_upper = ci_pop_prop + margin_of_error
        
        # Sample proportion input or random generation
        st.write("---")
        st.subheader("Choose Exploration Method")
        
        exploration_mode = st.radio(
            "Select Mode",
            options=["Single Sample", "Multiple Samples"],
            key="ci_exploration_mode",
            horizontal=True
        )
        
        ci_sample_prop = None
        sample_provided = False
        multiple_samples = []
        
        if exploration_mode == "Single Sample":
            st.write("Add a sample proportion (p̂) to see if an interval with the same margin of error would capture the population proportion.")
            
            col_choice1, col_choice2 = st.columns(2)
            
            with col_choice1:
                sample_method = st.radio(
                    "Method",
                    options=["Enter Manually", "Generate Random Sample"],
                    key="ci_sample_method"
                )
            
            with col_choice2:
                if sample_method == "Enter Manually":
                    ci_sample_prop = st.slider(
                        "Sample Proportion (p̂)", 
                        min_value=0.0, 
                        max_value=1.0, 
                        value=None,
                        step=0.01,
                        format="%.3f",
                        help="Move the slider to explore different sample proportions",
                        key="ci_sample_prop_slider"
                    )
                    if ci_sample_prop is not None:
                        sample_provided = True
                else:
                    if st.button("Generate Random Sample", key="generate_random_sample"):
                        # Generate a random sample
                        sample = np.random.binomial(1, ci_pop_prop, ci_sample_size)
                        st.session_state.random_sample_prop = np.mean(sample)
                        sample_provided = True
                    
                    # Display the random sample proportion
                    if 'random_sample_prop' in st.session_state:
                        ci_sample_prop = st.session_state.random_sample_prop
                        st.metric("Generated Sample Proportion", f"{ci_sample_prop:.4f}")
                        sample_provided = True
        
        else:  # Multiple Samples mode
            st.write(f"""
            Generate multiple random samples to see what percentage of confidence intervals 
            capture the true population proportion. This illustrates that a **{int(confidence_level*100)}% confidence level** 
            means approximately **{int(confidence_level*100)}%** of intervals will contain the true parameter.
            """)
            
            col_multi1, col_multi2 = st.columns(2)
            
            with col_multi1:
                num_samples_to_generate = st.slider(
                    "Number of Samples to Generate",
                    min_value=10,
                    max_value=200,
                    value=100,
                    step=10,
                    key="num_samples_multi"
                )
            
            with col_multi2:
                if st.button("Generate Multiple Samples", key="generate_multiple_samples"):
                    # Generate multiple samples
                    st.session_state.multiple_samples_data = []
                    for i in range(num_samples_to_generate):
                        sample = np.random.binomial(1, ci_pop_prop, ci_sample_size)
                        sample_prop = np.mean(sample)
                        ci_low = sample_prop - margin_of_error
                        ci_high = sample_prop + margin_of_error
                        captures_p = ci_low <= ci_pop_prop <= ci_high
                        st.session_state.multiple_samples_data.append({
                            'sample_prop': sample_prop,
                            'ci_lower': ci_low,
                            'ci_upper': ci_high,
                            'captures': captures_p
                        })
            
            if 'multiple_samples_data' in st.session_state and st.session_state.multiple_samples_data:
                multiple_samples = st.session_state.multiple_samples_data
                sample_provided = True
        
        # Create visualization
        st.write("---")
        st.subheader("Visualization")
        
        try:
            if exploration_mode == "Multiple Samples" and multiple_samples:
                # Multiple samples visualization
                fig, ax = plt.subplots(figsize=(14, 10))
                
                # Calculate statistics
                num_captured = sum(1 for s in multiple_samples if s['captures'])
                capture_rate = (num_captured / len(multiple_samples)) * 100
                
                # Determine plot range
                all_bounds = [s['ci_lower'] for s in multiple_samples] + [s['ci_upper'] for s in multiple_samples]
                plot_min = max(0, min(all_bounds + [ci_pop_prop]) - 0.1)
                plot_max = min(1, max(all_bounds + [ci_pop_prop]) + 0.1)
                
                # Draw vertical line at population proportion
                ax.axvline(ci_pop_prop, color='purple', linestyle='--', linewidth=3, 
                          label=f'Population Proportion (p = {ci_pop_prop:.3f})', zorder=10)
                
                # Draw each confidence interval
                for i, sample_data in enumerate(multiple_samples):
                    y_pos = i
                    color = 'green' if sample_data['captures'] else 'red'
                    
                    # Draw interval line
                    ax.plot([sample_data['ci_lower'], sample_data['ci_upper']], [y_pos, y_pos],
                           color=color, linewidth=1.5, alpha=0.7)
                    
                    # Draw endpoints
                    ax.plot([sample_data['ci_lower'], sample_data['ci_upper']], [y_pos, y_pos],
                           'o', color=color, markersize=3)
                
                # Add legend entries for captured/missed
                ax.plot([], [], color='green', linewidth=2, label=f'Captures p ({num_captured})')
                ax.plot([], [], color='red', linewidth=2, label=f'Misses p ({len(multiple_samples) - num_captured})')
                
                ax.set_xlim(plot_min, plot_max)
                ax.set_ylim(-1, len(multiple_samples))
                ax.set_xlabel('Proportion', fontsize=12, fontweight='bold')
                ax.set_ylabel('Sample Number', fontsize=12, fontweight='bold')
                ax.set_title(f'{len(multiple_samples)} Confidence Intervals: {capture_rate:.1f}% Capture the Population Proportion\n' + 
                            f'(Expected: {int(confidence_level*100)}%)', 
                            fontsize=14, fontweight='bold', pad=15)
                ax.legend(fontsize=10, loc='upper right')
                ax.grid(True, alpha=0.3, axis='x')
                
                st.pyplot(fig)
                plt.close(fig)
                
                # Display statistics
                st.write("---")
                st.subheader("Results Summary")
                
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    st.metric("Total Samples", len(multiple_samples))
                    st.metric("Intervals Capturing p", num_captured)
                
                with col_stat2:
                    st.metric("Intervals Missing p", len(multiple_samples) - num_captured)
                    st.metric("Capture Rate", f"{capture_rate:.1f}%")
                
                with col_stat3:
                    st.metric("Expected Rate", f"{int(confidence_level*100)}%")
                    difference = capture_rate - (confidence_level * 100)
                    st.metric("Difference", f"{difference:+.1f}%")
                
                st.write("---")
                if abs(difference) <= 5:
                    st.success(f"""
                    ✓ The observed capture rate ({capture_rate:.1f}%) is very close to the expected {int(confidence_level*100)}%! 
                    This demonstrates that confidence intervals work as intended.
                    """)
                else:
                    st.info(f"""
                    The observed capture rate ({capture_rate:.1f}%) differs from the expected {int(confidence_level*100)}% by {abs(difference):.1f}%. 
                    This is normal due to random variation. Try generating more samples to see the rate approach {int(confidence_level*100)}%.
                    """)
                
                st.write("""
                **Key Insight:**
                - Each horizontal line represents a confidence interval from a different sample
                - Green intervals successfully capture the true population proportion (purple line)
                - Red intervals miss the population proportion
                - With a large number of samples, approximately the confidence level percentage will be green
                """)
            
            else:
                # Single sample visualization
                fig, ax = plt.subplots(figsize=(14, 8))
                
                # Determine plot range
                if sample_provided and ci_sample_prop is not None:
                    plot_min = max(0, min(ci_pop_prop, ci_sample_prop) - 0.2)
                    plot_max = min(1, max(ci_pop_prop, ci_sample_prop) + 0.2)
                    # Calculate confidence interval around the sample proportion
                    ci_lower = ci_sample_prop - margin_of_error
                    ci_upper = ci_sample_prop + margin_of_error
                    # Check if interval captures population proportion
                    captures = ci_lower <= ci_pop_prop <= ci_upper
                else:
                    plot_min = max(0, ci_pop_prop - 0.3)
                    plot_max = min(1, ci_pop_prop + 0.3)
                    captures = None
                
                # ALWAYS draw the interval around population proportion (static)
                y_pop = 0.65
                ax.plot([pop_ci_lower, pop_ci_upper], [y_pop, y_pop], 
                       color='steelblue', linewidth=8, alpha=0.5,
                       label=f'Interval Around p (ME = ±{margin_of_error:.3f})')
                
                # Draw endpoints
                ax.plot([pop_ci_lower, pop_ci_upper], [y_pop, y_pop], 
                       'o', color='steelblue', markersize=15, markeredgecolor='black', 
                       markeredgewidth=2)
                
                # Draw the population proportion
                ax.plot(ci_pop_prop, y_pop, 's', color='purple', markersize=20,
                       markeredgecolor='black', markeredgewidth=2,
                       label=f'Population Proportion (p = {ci_pop_prop:.3f})', zorder=5)
                
                # Add shaded region for population interval
                ax.axvspan(pop_ci_lower, pop_ci_upper, alpha=0.15, color='steelblue', zorder=1)
                
                # Add text annotations for population interval
                ax.text(pop_ci_lower, y_pop + 0.12, f'{pop_ci_lower:.3f}', 
                       ha='center', va='bottom', fontsize=10, fontweight='bold', color='steelblue')
                ax.text(pop_ci_upper, y_pop + 0.12, f'{pop_ci_upper:.3f}', 
                       ha='center', va='bottom', fontsize=10, fontweight='bold', color='steelblue')
                
                # If sample proportion is provided, draw interval around it
                if sample_provided and ci_sample_prop is not None:
                    y_sample = 0.35
                    interval_color = 'green' if captures else 'red'
                    
                    # Draw the interval line around sample proportion
                    ax.plot([ci_lower, ci_upper], [y_sample, y_sample], 
                           color=interval_color, linewidth=8, alpha=0.7,
                           label=f'Interval Around p̂ (same ME)')
                    
                    # Draw endpoints of the interval
                    ax.plot([ci_lower, ci_upper], [y_sample, y_sample], 
                           'o', color=interval_color, markersize=15, markeredgecolor='black', 
                           markeredgewidth=2)
                    
                    # Draw the sample proportion at the center
                    ax.plot(ci_sample_prop, y_sample, 'D', color='blue', markersize=20,
                           markeredgecolor='black', markeredgewidth=2,
                           label=f'Sample Proportion (p̂ = {ci_sample_prop:.3f})', zorder=5)
                    
                    # Add shaded region for sample interval
                    ax.axvspan(ci_lower, ci_upper, alpha=0.15, color=interval_color, zorder=1)
                    
                    # Add text annotations for sample interval
                    ax.text(ci_lower, y_sample - 0.12, f'{ci_lower:.3f}', 
                           ha='center', va='top', fontsize=10, fontweight='bold', color=interval_color)
                    ax.text(ci_upper, y_sample - 0.12, f'{ci_upper:.3f}', 
                           ha='center', va='top', fontsize=10, fontweight='bold', color=interval_color)
                    
                    # Draw vertical line at population proportion to see if it's captured
                    ax.axvline(ci_pop_prop, color='purple', linestyle='--', linewidth=2, alpha=0.6, zorder=3)
                
                # Formatting
                ax.set_xlim(plot_min, plot_max)
                ax.set_ylim(0, 1)
                ax.set_yticks([])
                ax.set_xlabel('Proportion', fontsize=14, fontweight='bold')
                
                if sample_provided and ci_sample_prop is not None:
                    if captures:
                        title_text = f'✓ Confidence Interval Around p̂ CAPTURES the Population Proportion!'
                        title_color = 'green'
                    else:
                        title_text = f'✗ Confidence Interval Around p̂ DOES NOT capture the Population Proportion'
                        title_color = 'red'
                else:
                    title_text = 'Confidence Interval Around Population Proportion\n(Add a sample proportion to compare)'
                    title_color = 'black'
                
                ax.set_title(title_text, fontsize=16, fontweight='bold', color=title_color, pad=20)
                ax.legend(fontsize=11, loc='upper right')
                ax.grid(True, alpha=0.3, axis='x')
                
                st.pyplot(fig)
                plt.close(fig)
                
                # Explanation - only show when sample is provided
                if sample_provided and ci_sample_prop is not None:
                    st.write("---")
                    st.subheader("Interpretation")
                    
                    col_result1, col_result2 = st.columns(2)
                    
                    with col_result1:
                        st.metric("Confidence Interval Around p̂", f"[{ci_lower:.4f}, {ci_upper:.4f}]")
                        st.metric("Interval Width", f"{ci_upper - ci_lower:.4f}")
                        st.metric("Sample Proportion (p̂)", f"{ci_sample_prop:.4f}")
                    
                    with col_result2:
                        st.metric("Population Proportion (p)", f"{ci_pop_prop:.4f}")
                        st.metric("Distance from p̂ to p", f"{abs(ci_sample_prop - ci_pop_prop):.4f}")
                        if captures:
                            st.success("✓ Interval captures p")
                        else:
                            st.error("✗ Interval does not capture p")
                    
                    st.write("---")
                    st.write("**Key Concepts:**")
                    
                    if captures:
                        st.success(f"""
                        🎯 **Success!** The confidence interval [{ci_lower:.3f}, {ci_upper:.3f}] constructed around 
                        the sample proportion (p̂ = {ci_sample_prop:.3f}) successfully captures the true population 
                        proportion (p = {ci_pop_prop:.3f}).
                        """)
                    else:
                        st.error(f"""
                        ❌ **Miss!** The confidence interval [{ci_lower:.3f}, {ci_upper:.3f}] constructed around 
                        the sample proportion (p̂ = {ci_sample_prop:.3f}) does NOT capture the true population 
                        proportion (p = {ci_pop_prop:.3f}). This happens about {100-int(confidence_level*100)}% of the time.
                        """)
                    
                    st.write(f"""
                    - A **{int(confidence_level*100)}% confidence interval** means that if we took many samples and 
                      constructed an interval around each sample proportion using the same margin of error, 
                      approximately **{int(confidence_level*100)}%** of those intervals would capture the true population proportion.
                    
                    - The **margin of error** ({margin_of_error:.4f}) determines the width of the interval.
                    
                    - **Larger sample sizes** lead to smaller margins of error (narrower, more precise intervals).
                    
                    - **Higher confidence levels** lead to larger margins of error (wider intervals to increase 
                      the chance of capturing the true parameter).
                    
                    - Try moving the slider or generating random samples to see which intervals capture the population 
                      proportion and which don't!
                    """)
                
        except Exception as e:
            st.error(f"An error occurred while creating the visualization: {e}")
    
    with sim_tabs[5]:
        st.subheader("Hypothesis Testing Explorer")
        st.write("""
        This interactive simulation helps you understand hypothesis testing by visualizing the relationship 
        between test statistics, p-values, and significance levels. Adjust the sample statistic to see 
        how the p-value changes and whether you would reject the null hypothesis.
        """)
        
        # Put controls in an expander to make visualization more prominent
        with st.expander("⚙️ Test Configuration & Controls", expanded=True):
            # Test selection and parameters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                test_type = st.selectbox(
                    "Select Test Type",
                    options=["Z-test (Proportion)", "Z-test (Mean)", "T-test (Mean)", "Chi-Square Test"],
                    key="ht_test_type"
                )
            
            with col2:
                alternative = st.selectbox(
                    "Alternative Hypothesis",
                    options=["Two-tailed (≠)", "Right-tailed (>)", "Left-tailed (<)"],
                    key="ht_alternative"
                )
            
            with col3:
                alpha = st.selectbox(
                    "Significance Level (α)",
                    options=[0.01, 0.05, 0.10],
                    index=1,
                    format_func=lambda x: f"{x}",
                    key="ht_alpha"
                )
            
            st.write("---")
            
            # Test-specific parameters
            if test_type == "Z-test (Proportion)":
                null_value = st.number_input(
                    "Null Hypothesis Value (p₀)",
                    min_value=0.01,
                    max_value=0.99,
                    value=0.5,
                    step=0.01,
                    format="%.2f",
                    key="ht_null_prop"
                )
                sample_size_ht = st.number_input(
                    "Sample Size (n)",
                    min_value=10,
                    max_value=1000,
                    value=100,
                    step=10,
                    key="ht_n_prop"
                )
                se = np.sqrt(null_value * (1 - null_value) / sample_size_ht)
                test_stat_min = null_value - 4 * se
                test_stat_max = null_value + 4 * se
                default_stat = null_value + 1.5 * se
                x_label = "Sample Proportion (p̂)"
                dist_name = "Normal Distribution"
            elif test_type in ["Z-test (Mean)", "T-test (Mean)"]:  # Mean tests
                null_value = st.number_input(
                    "Null Hypothesis Value (μ₀)",
                    min_value=-100.0,
                    max_value=100.0,
                    value=0.0,
                    step=0.1,
                    format="%.1f",
                    key="ht_null_mean"
                )
                
                # Get sample size to calculate SE
                sample_size_mean = st.number_input(
                    "Sample Size (n)",
                    min_value=2,
                    max_value=500,
                    value=30,
                    step=1,
                    key="ht_n_mean"
                )
                
                sample_std = st.number_input(
                    "Sample Std Dev (s)" if test_type == "T-test (Mean)" else "Population Std Dev (σ)",
                    min_value=0.1,
                    max_value=50.0,
                    value=5.0,
                    step=0.1,
                    format="%.1f",
                    key="ht_std_mean"
                )
                
                # Calculate SE automatically
                se = sample_std / np.sqrt(sample_size_mean)
                if test_type == "T-test (Mean)":
                    df_ht = sample_size_mean - 1
                
                test_stat_min = null_value - 4 * se
                test_stat_max = null_value + 4 * se
                default_stat = null_value + 1.5 * se
                x_label = "Sample Mean (x̄)"
                dist_name = "T-Distribution" if test_type == "T-test (Mean)" else "Normal Distribution"
                
                # Display computed SE
                st.caption(f"Computed SE = {se:.4f}")
            elif test_type == "Chi-Square Test":
                df_chi = st.number_input(
                    "Degrees of Freedom",
                    min_value=1,
                    max_value=50,
                    value=5,
                    step=1,
                    key="ht_df_chi"
                )
                
                null_value = df_chi  # For chi-square, center is at df
                dist_name = "Chi-Square Distribution"
                x_label = "χ² Statistic"
                test_stat_min = 0.0
                test_stat_max = float(df_chi * 4)
                default_stat = float(df_chi * 1.5)
        
        # Sample statistic slider - separate section for better visibility
        st.write("---")
        st.subheader("📊 Adjust Sample Statistic")
        test_statistic = st.slider(
            x_label,
            min_value=float(test_stat_min),
            max_value=float(test_stat_max),
            value=float(default_stat),
            step=float((test_stat_max - test_stat_min)/200) if test_type != "Chi-Square Test" else 0.1,
            format="%.3f" if test_type != "Chi-Square Test" else "%.2f",
            key="ht_test_stat",
            help="Move the slider to adjust the sample statistic and observe how the p-value and test decision change"
        )
        
        # Visualization section - now more prominent above detailed results
        st.write("---")
        st.subheader("Visualization")
        
        try:
            fig, ax = plt.subplots(figsize=(10, 4))
            
            # Generate distribution
            if test_type == "Chi-Square Test":
                x_vals = np.linspace(0.001, df_chi * 4, 1000)
                y_vals = stats.chi2.pdf(x_vals, df_chi)
                
                # Calculate critical values and p-value for chi-square (always right-tailed)
                crit_val = stats.chi2.ppf(1 - alpha, df_chi)
                p_value = stats.chi2.sf(test_statistic, df_chi)
                
                # Plot distribution
                ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'χ²({df_chi})')
                
                # Shade significance region (right tail)
                x_crit = x_vals[x_vals >= crit_val]
                y_crit = stats.chi2.pdf(x_crit, df_chi)
                ax.fill_between(x_crit, y_crit, alpha=0.3, color='red', label=f'Rejection Region (α={alpha})')
                
                # Shade p-value region
                x_pval = x_vals[x_vals >= test_statistic]
                y_pval = stats.chi2.pdf(x_pval, df_chi)
                ax.fill_between(x_pval, y_pval, alpha=0.5, color='orange', label=f'P-value = {p_value:.4f}')
                
                # Mark test statistic
                ax.axvline(test_statistic, color='green', linestyle='--', linewidth=2, 
                          label=f'Test Statistic = {test_statistic:.2f}')
                ax.axvline(crit_val, color='red', linestyle=':', linewidth=2,
                          label=f'Critical Value = {crit_val:.2f}')
                
            else:
                # For Z-test and T-test - use original scale
                if test_type == "T-test (Mean)":
                    # Calculate on original scale
                    t_stat = (test_statistic - null_value) / se
                    
                    # Calculate critical values on standardized scale, then convert to original
                    if alternative == "Two-tailed (≠)":
                        crit_lower_std = stats.t.ppf(alpha/2, df_ht)
                        crit_upper_std = stats.t.ppf(1 - alpha/2, df_ht)
                        crit_lower = null_value + crit_lower_std * se
                        crit_upper = null_value + crit_upper_std * se
                        p_value = 2 * min(stats.t.cdf(t_stat, df_ht), stats.t.sf(t_stat, df_ht))
                    elif alternative == "Right-tailed (>)":
                        crit_upper_std = stats.t.ppf(1 - alpha, df_ht)
                        crit_upper = null_value + crit_upper_std * se
                        crit_lower = None
                        p_value = stats.t.sf(t_stat, df_ht)
                    else:  # Left-tailed
                        crit_lower_std = stats.t.ppf(alpha, df_ht)
                        crit_lower = null_value + crit_lower_std * se
                        crit_upper = None
                        p_value = stats.t.cdf(t_stat, df_ht)
                    
                    # Generate x values on original scale
                    x_vals = np.linspace(null_value - 4*se, null_value + 4*se, 1000)
                    # Calculate y values using scaled t-distribution
                    y_vals = stats.t.pdf((x_vals - null_value) / se, df_ht) / se
                    
                    ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f't-distribution (df={df_ht})')
                    test_stat_plot = test_statistic  # Original scale for plotting
                    std_test_stat = t_stat  # Standardized for display
                    
                else:  # Z-tests
                    z_stat = (test_statistic - null_value) / se
                    
                    # Calculate critical values on standardized scale, then convert to original
                    if alternative == "Two-tailed (≠)":
                        crit_lower_std = stats.norm.ppf(alpha/2)
                        crit_upper_std = stats.norm.ppf(1 - alpha/2)
                        crit_lower = null_value + crit_lower_std * se
                        crit_upper = null_value + crit_upper_std * se
                        p_value = 2 * min(stats.norm.cdf(z_stat), stats.norm.sf(z_stat))
                    elif alternative == "Right-tailed (>)":
                        crit_upper_std = stats.norm.ppf(1 - alpha)
                        crit_upper = null_value + crit_upper_std * se
                        crit_lower = None
                        p_value = stats.norm.sf(z_stat)
                    else:  # Left-tailed
                        crit_lower_std = stats.norm.ppf(alpha)
                        crit_lower = null_value + crit_lower_std * se
                        crit_upper = None
                        p_value = stats.norm.cdf(z_stat)
                    
                    # Generate x values on original scale
                    x_vals = np.linspace(null_value - 4*se, null_value + 4*se, 1000)
                    # Calculate y values using scaled normal distribution
                    y_vals = stats.norm.pdf(x_vals, loc=null_value, scale=se)
                    
                    ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'Normal Distribution')
                    test_stat_plot = test_statistic  # Original scale for plotting
                    std_test_stat = z_stat  # Standardized for display
                
                # Shade significance regions
                if alternative == "Two-tailed (≠)":
                    x_left = x_vals[x_vals <= crit_lower]
                    if test_type == "T-test (Mean)":
                        y_left = stats.t.pdf((x_left - null_value) / se, df_ht) / se
                    else:
                        y_left = stats.norm.pdf(x_left, loc=null_value, scale=se)
                    ax.fill_between(x_left, y_left, alpha=0.3, color='red', label=f'Rejection Region (α={alpha})')
                    
                    x_right = x_vals[x_vals >= crit_upper]
                    if test_type == "T-test (Mean)":
                        y_right = stats.t.pdf((x_right - null_value) / se, df_ht) / se
                    else:
                        y_right = stats.norm.pdf(x_right, loc=null_value, scale=se)
                    ax.fill_between(x_right, y_right, alpha=0.3, color='red')
                    
                elif alternative == "Right-tailed (>)":
                    x_right = x_vals[x_vals >= crit_upper]
                    if test_type == "T-test (Mean)":
                        y_right = stats.t.pdf((x_right - null_value) / se, df_ht) / se
                    else:
                        y_right = stats.norm.pdf(x_right, loc=null_value, scale=se)
                    ax.fill_between(x_right, y_right, alpha=0.3, color='red', label=f'Rejection Region (α={alpha})')
                    
                else:  # Left-tailed
                    x_left = x_vals[x_vals <= crit_lower]
                    if test_type == "T-test (Mean)":
                        y_left = stats.t.pdf((x_left - null_value) / se, df_ht) / se
                    else:
                        y_left = stats.norm.pdf(x_left, loc=null_value, scale=se)
                    ax.fill_between(x_left, y_left, alpha=0.3, color='red', label=f'Rejection Region (α={alpha})')
                
                # Shade p-value region
                if alternative == "Two-tailed (≠)":
                    if test_stat_plot >= null_value:
                        x_pval = x_vals[x_vals >= test_stat_plot]
                        x_pval_mirror = x_vals[x_vals <= (null_value - (test_stat_plot - null_value))]
                    else:
                        x_pval = x_vals[x_vals <= test_stat_plot]
                        x_pval_mirror = x_vals[x_vals >= (null_value + (null_value - test_stat_plot))]
                    
                    if test_type == "T-test (Mean)":
                        y_pval = stats.t.pdf((x_pval - null_value) / se, df_ht) / se
                        y_pval_mirror = stats.t.pdf((x_pval_mirror - null_value) / se, df_ht) / se
                    else:
                        y_pval = stats.norm.pdf(x_pval, loc=null_value, scale=se)
                        y_pval_mirror = stats.norm.pdf(x_pval_mirror, loc=null_value, scale=se)
                    
                    ax.fill_between(x_pval, y_pval, alpha=0.5, color='orange', label=f'P-value = {p_value:.4f}')
                    ax.fill_between(x_pval_mirror, y_pval_mirror, alpha=0.5, color='orange')
                    
                elif alternative == "Right-tailed (>)":
                    x_pval = x_vals[x_vals >= test_stat_plot]
                    if test_type == "T-test (Mean)":
                        y_pval = stats.t.pdf((x_pval - null_value) / se, df_ht) / se
                    else:
                        y_pval = stats.norm.pdf(x_pval, loc=null_value, scale=se)
                    ax.fill_between(x_pval, y_pval, alpha=0.5, color='orange', label=f'P-value = {p_value:.4f}')
                    
                else:  # Left-tailed
                    x_pval = x_vals[x_vals <= test_stat_plot]
                    if test_type == "T-test (Mean)":
                        y_pval = stats.t.pdf((x_pval - null_value) / se, df_ht) / se
                    else:
                        y_pval = stats.norm.pdf(x_pval, loc=null_value, scale=se)
                    ax.fill_between(x_pval, y_pval, alpha=0.5, color='orange', label=f'P-value = {p_value:.4f}')
                
                # Mark test statistic and critical values
                if test_type == "Chi-Square Test":
                    stat_label = f'Test Statistic = {test_stat_plot:.3f}'
                else:
                    # Show standardized statistic for Z and T tests
                    stat_label = f'Test Statistic = {std_test_stat:.3f}'
                ax.axvline(test_stat_plot, color='green', linestyle='--', linewidth=2,
                          label=stat_label)
                
                if alternative == "Two-tailed (≠)":
                    ax.axvline(crit_lower, color='red', linestyle=':', linewidth=2,
                              label=f'Critical Values = {crit_lower:.4f}, {crit_upper:.4f}')
                    ax.axvline(crit_upper, color='red', linestyle=':', linewidth=2)
                elif alternative == "Right-tailed (>)":
                    ax.axvline(crit_upper, color='red', linestyle=':', linewidth=2,
                              label=f'Critical Value = {crit_upper:.4f}')
                else:  # Left-tailed
                    ax.axvline(crit_lower, color='red', linestyle=':', linewidth=2,
                              label=f'Critical Value = {crit_lower:.4f}')
            
            # Formatting
            if test_type == "Chi-Square Test":
                x_label = 'χ² Statistic'
            elif test_type == "Z-test (Proportion)":
                x_label = 'Sampling Distribution of Sample Proportion'
            else:  # Mean tests
                x_label = 'Sampling Distribution of Sample Mean'
            ax.set_xlabel(x_label, 
                         fontsize=12, fontweight='bold')
            ax.set_ylabel('Probability Density', fontsize=12, fontweight='bold')
            
            # Add null value to x-axis tick marks for non-Chi-Square tests
            if test_type != "Chi-Square Test":
                current_ticks = list(ax.get_xticks())
                # Add the null value if it's not already very close to an existing tick
                if not any(abs(tick - null_value) < (test_stat_max - test_stat_min) * 0.05 for tick in current_ticks):
                    current_ticks.append(null_value)
                    current_ticks.sort()
                ax.set_xticks(current_ticks)
            
            # Determine decision
            reject = p_value < alpha
            
            ax.legend(fontsize=10, loc='upper right')
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            plt.close(fig)
            
            # Display detailed results below
            st.write("---")
            st.subheader("Detailed Test Results")
            
            col_res1, col_res2, col_res3 = st.columns(3)
            
            with col_res1:
                st.metric("Test Statistic", f"{test_statistic:.4f}" if test_type != "Chi-Square Test" else f"{test_statistic:.2f}")
                if test_type != "Chi-Square Test":
                    std_stat = (test_statistic - null_value) / se
                    st.metric("Standardized Statistic", f"{std_stat:.3f}")
            
            with col_res2:
                st.metric("P-value", f"{p_value:.4f}")
                st.metric("Significance Level (α)", f"{alpha}")
            
            with col_res3:
                if reject:
                    st.error("**Decision: REJECT H₀**")
                else:
                    st.success("**Decision: FAIL TO REJECT H₀**")
            
            st.write("---")
            st.write("**Hypotheses:**")
            
            if test_type == "Z-test (Proportion)":
                h0_text = f"H₀: p = {null_value}"
                if alternative == "Two-tailed (≠)":
                    ha_text = f"Hₐ: p ≠ {null_value}"
                elif alternative == "Right-tailed (>)":
                    ha_text = f"Hₐ: p > {null_value}"
                else:
                    ha_text = f"Hₐ: p < {null_value}"
            elif test_type == "Chi-Square Test":
                h0_text = "H₀: Variables are independent (or goodness of fit)"
                ha_text = "Hₐ: Variables are not independent (or poor fit)"
            else:
                h0_text = f"H₀: μ = {null_value}"
                if alternative == "Two-tailed (≠)":
                    ha_text = f"Hₐ: μ ≠ {null_value}"
                elif alternative == "Right-tailed (>)":
                    ha_text = f"Hₐ: μ > {null_value}"
                else:
                    ha_text = f"Hₐ: μ < {null_value}"
            
            st.write(f"- **Null Hypothesis**: {h0_text}")
            st.write(f"- **Alternative Hypothesis**: {ha_text}")
            
            st.write("---")
            st.write("**Interpretation:**")
            st.write(f"""
            - The **red shaded region(s)** represent the rejection region (significance level α = {alpha})
            - The **orange shaded region(s)** represent the p-value area
            - The **green vertical line** shows your test statistic
            - The **red dotted line(s)** show the critical value(s)
            """)
            
            if reject:
                st.error(f"""
                🔴 **Reject the null hypothesis**: The p-value ({p_value:.4f}) is less than the significance 
                level ({alpha}), indicating that the observed result is statistically significant. The test 
                statistic falls in the rejection region.
                """)
            else:
                st.success(f"""
                🟢 **Fail to reject the null hypothesis**: The p-value ({p_value:.4f}) is greater than or equal 
                to the significance level ({alpha}), indicating that we do not have sufficient evidence to reject 
                the null hypothesis. The test statistic does not fall in the rejection region.
                """)
            
            st.write("""
            **Key Concepts:**
            - Move the slider to see how different test statistics affect the p-value
            - The p-value represents the probability of observing a test statistic as extreme or more extreme 
              than the observed value, assuming the null hypothesis is true
            - When p-value < α, we reject the null hypothesis
            - When p-value ≥ α, we fail to reject the null hypothesis
            """)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
    
    with sim_tabs[6]:
        st.subheader("Two Proportions")
        st.write("""
        This simulation demonstrates the sampling distribution of the difference between two sample proportions.
        It helps you understand how differences between two groups behave under repeated sampling and visualizes
        the Central Limit Theorem for the difference between two proportions.
        """)
        
        # Create input columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            p1_pop = st.number_input(
                "Population 1 Proportion (p₁)", 
                min_value=0.01, 
                max_value=0.99, 
                value=0.6, 
                step=0.01,
                format="%.3f",
                help="The true proportion in population 1",
                key="diff_prop_p1"
            )
            n1_size = st.number_input(
                "Sample Size from Population 1 (n₁)", 
                min_value=10, 
                max_value=1000, 
                value=100, 
                step=10,
                help="Size of each sample from population 1",
                key="diff_prop_n1"
            )
        
        with col2:
            p2_pop = st.number_input(
                "Population 2 Proportion (p₂)", 
                min_value=0.01, 
                max_value=0.99, 
                value=0.4, 
                step=0.01,
                format="%.3f",
                help="The true proportion in population 2",
                key="diff_prop_p2"
            )
            n2_size = st.number_input(
                "Sample Size from Population 2 (n₂)", 
                min_value=10, 
                max_value=1000, 
                value=100, 
                step=10,
                help="Size of each sample from population 2",
                key="diff_prop_n2"
            )
        
        with col3:
            num_samples_diff_prop = st.number_input(
                "Number of Samples", 
                min_value=100, 
                max_value=10000, 
                value=1000, 
                step=100,
                help="Number of pairs of samples to generate",
                key="diff_prop_num_samples"
            )
        
        if st.button("Run Simulation", key="run_diff_prop_sim"):
            try:
                # Create placeholders for progressive updates
                progress_bar = st.progress(0)
                status_text = st.empty()
                plot_placeholder = st.empty()
                stats_placeholder = st.empty()
                
                # Store differences
                differences = []
                
                # Generate samples in batches
                batch_size = 100
                num_batches = int(np.ceil(num_samples_diff_prop / batch_size))
                
                for batch in range(num_batches):
                    # Update progress
                    progress = (batch + 1) / num_batches
                    progress_bar.progress(progress)
                    status_text.text(f"Generating samples... {int(progress * 100)}%")
                    
                    # Generate batch of samples
                    samples_in_batch = min(batch_size, num_samples_diff_prop - batch * batch_size)
                    
                    for _ in range(samples_in_batch):
                        # Generate sample from population 1
                        sample1 = np.random.binomial(1, p1_pop, n1_size)
                        p1_hat = np.mean(sample1)
                        
                        # Generate sample from population 2
                        sample2 = np.random.binomial(1, p2_pop, n2_size)
                        p2_hat = np.mean(sample2)
                        
                        # Calculate difference
                        diff = p1_hat - p2_hat
                        differences.append(diff)
                    
                    # Update plot every few batches
                    if (batch + 1) % 3 == 0 or batch == num_batches - 1:
                        with plot_placeholder.container():
                            fig, ax = plt.subplots(figsize=(12, 6))
                            
                            # Plot histogram
                            ax.hist(differences, bins=50, density=True, alpha=0.7, color='steelblue', 
                                   edgecolor='black', label='Sample Differences')
                            
                            # Calculate theoretical distribution
                            true_diff = p1_pop - p2_pop
                            theoretical_std = np.sqrt(p1_pop * (1 - p1_pop) / n1_size + p2_pop * (1 - p2_pop) / n2_size)
                            
                            # Overlay normal curve
                            x_range = np.linspace(min(differences), max(differences), 200)
                            normal_curve = stats.norm.pdf(x_range, loc=true_diff, scale=theoretical_std)
                            ax.plot(x_range, normal_curve, 'r-', linewidth=2, 
                                   label=f'Normal(μ={true_diff:.3f}, σ={theoretical_std:.3f})')
                            
                            # Mark the true difference
                            ax.axvline(true_diff, color='darkgreen', linestyle='--', linewidth=2, 
                                      label=f'True Difference (p₁ - p₂ = {true_diff:.3f})')
                            
                            # Mark the mean of sample differences
                            mean_diff = np.mean(differences)
                            ax.axvline(mean_diff, color='orange', linestyle=':', linewidth=2, 
                                      label=f'Mean of Differences = {mean_diff:.3f}')
                            
                            ax.set_xlabel('Difference in Sample Proportions (p̂₁ - p̂₂)', fontsize=12)
                            ax.set_ylabel('Density', fontsize=12)
                            ax.set_title('Sampling Distribution of Difference Between Two Proportions', fontsize=14, fontweight='bold')
                            ax.legend(loc='best', fontsize=10)
                            ax.grid(True, alpha=0.3)
                            
                            st.pyplot(fig)
                            plt.close()
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Display final statistics
                with stats_placeholder.container():
                    st.write("---")
                    st.subheader("Summary Statistics")
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("Population 1 Proportion (p₁)", f"{p1_pop:.4f}")
                        st.metric("Population 2 Proportion (p₂)", f"{p2_pop:.4f}")
                        st.metric("True Difference (p₁ - p₂)", f"{p1_pop - p2_pop:.4f}")
                    
                    with col_b:
                        mean_diff = np.mean(differences)
                        std_diff = np.std(differences, ddof=1)
                        st.metric("Mean of Sample Differences", f"{mean_diff:.4f}")
                        st.metric("Std Dev of Sample Differences", f"{std_diff:.4f}")
                        st.metric("Number of Samples", f"{len(differences)}")
                    
                    with col_c:
                        theoretical_mean = p1_pop - p2_pop
                        theoretical_std = np.sqrt(p1_pop * (1 - p1_pop) / n1_size + p2_pop * (1 - p2_pop) / n2_size)
                        st.metric("Theoretical Mean", f"{theoretical_mean:.4f}")
                        st.metric("Theoretical Std Dev", f"{theoretical_std:.4f}")
                    
                    st.write("---")
                    st.write("**Key Observations:**")
                    st.write(f"- The mean of sample differences ({mean_diff:.4f}) should be close to the true difference ({theoretical_mean:.4f})")
                    st.write(f"- The standard deviation is approximately {theoretical_std:.4f}")
                    st.write(f"- The distribution is approximately normal by the Central Limit Theorem")
                    st.write(f"- Larger sample sizes lead to a narrower (more precise) distribution")
                    
                    # Check conditions for normality
                    n1p1 = n1_size * p1_pop
                    n1q1 = n1_size * (1 - p1_pop)
                    n2p2 = n2_size * p2_pop
                    n2q2 = n2_size * (1 - p2_pop)
                    
                    st.write("**Conditions for Normal Approximation:**")
                    if n1p1 >= 10 and n1q1 >= 10 and n2p2 >= 10 and n2q2 >= 10:
                        st.success(f"✓ All conditions met: n₁p₁={n1p1:.1f}, n₁(1-p₁)={n1q1:.1f}, n₂p₂={n2p2:.1f}, n₂(1-p₂)={n2q2:.1f} (all ≥ 10)")
                    else:
                        st.warning(f"⚠ Some conditions not met: n₁p₁={n1p1:.1f}, n₁(1-p₁)={n1q1:.1f}, n₂p₂={n2p2:.1f}, n₂(1-p₂)={n2q2:.1f}")
                
            except Exception as e:
                st.error(f"An error occurred while running the simulation: {e}")
    
    with sim_tabs[7]:
        st.subheader("Two Means")
        st.write("""
        This simulation demonstrates the sampling distribution of the difference between two sample means
        using **sample standard deviations** and the **t-distribution**. This reflects real-world scenarios
        where population standard deviations are unknown and must be estimated from the samples.
        """)
        
        # Create input columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            mu1_pop = st.number_input(
                "Population 1 Mean (μ₁)", 
                min_value=-100.0, 
                max_value=100.0, 
                value=50.0, 
                step=1.0,
                format="%.2f",
                help="The true mean of population 1",
                key="diff_mean_mu1"
            )
            sigma1_pop = st.number_input(
                "Population 1 Std Dev (σ₁)", 
                min_value=0.1, 
                max_value=100.0, 
                value=10.0, 
                step=0.5,
                format="%.2f",
                help="The true standard deviation of population 1 (used to generate samples)",
                key="diff_mean_sigma1"
            )
            n1_mean_size = st.number_input(
                "Sample Size from Population 1 (n₁)", 
                min_value=5, 
                max_value=500, 
                value=30, 
                step=5,
                help="Size of each sample from population 1",
                key="diff_mean_n1"
            )
        
        with col2:
            mu2_pop = st.number_input(
                "Population 2 Mean (μ₂)", 
                min_value=-100.0, 
                max_value=100.0, 
                value=45.0, 
                step=1.0,
                format="%.2f",
                help="The true mean of population 2",
                key="diff_mean_mu2"
            )
            sigma2_pop = st.number_input(
                "Population 2 Std Dev (σ₂)", 
                min_value=0.1, 
                max_value=100.0, 
                value=12.0, 
                step=0.5,
                format="%.2f",
                help="The true standard deviation of population 2 (used to generate samples)",
                key="diff_mean_sigma2"
            )
            n2_mean_size = st.number_input(
                "Sample Size from Population 2 (n₂)", 
                min_value=5, 
                max_value=500, 
                value=30, 
                step=5,
                help="Size of each sample from population 2",
                key="diff_mean_n2"
            )
        
        with col3:
            num_samples_diff_mean = st.number_input(
                "Number of Samples", 
                min_value=100, 
                max_value=10000, 
                value=1000, 
                step=100,
                help="Number of pairs of samples to generate",
                key="diff_mean_num_samples"
            )
            equal_vars = st.checkbox(
                "Assume Equal Variances (Pooled)",
                value=True,
                help="If checked, uses pooled standard deviation; otherwise uses Welch's approximation",
                key="diff_mean_equal_vars"
            )
        
        if st.button("Run Simulation", key="run_diff_mean_sim"):
            try:
                # Create placeholders for progressive updates
                progress_bar = st.progress(0)
                status_text = st.empty()
                plot_placeholder = st.empty()
                stats_placeholder = st.empty()
                
                # Store differences and sample statistics
                differences = []
                sample_s1_list = []
                sample_s2_list = []
                
                # Generate samples in batches
                batch_size = 100
                num_batches = int(np.ceil(num_samples_diff_mean / batch_size))
                
                for batch in range(num_batches):
                    # Update progress
                    progress = (batch + 1) / num_batches
                    progress_bar.progress(progress)
                    status_text.text(f"Generating samples... {int(progress * 100)}%")
                    
                    # Generate batch of samples
                    samples_in_batch = min(batch_size, num_samples_diff_mean - batch * batch_size)
                    
                    for _ in range(samples_in_batch):
                        # Generate sample from population 1
                        sample1 = np.random.normal(mu1_pop, sigma1_pop, n1_mean_size)
                        mean1 = np.mean(sample1)
                        s1 = np.std(sample1, ddof=1)  # Sample std dev
                        
                        # Generate sample from population 2
                        sample2 = np.random.normal(mu2_pop, sigma2_pop, n2_mean_size)
                        mean2 = np.mean(sample2)
                        s2 = np.std(sample2, ddof=1)  # Sample std dev
                        
                        # Calculate difference
                        diff = mean1 - mean2
                        differences.append(diff)
                        sample_s1_list.append(s1)
                        sample_s2_list.append(s2)
                    
                    # Update plot every few batches
                    if (batch + 1) % 3 == 0 or batch == num_batches - 1:
                        with plot_placeholder.container():
                            fig, ax = plt.subplots(figsize=(12, 6))
                            
                            # Plot histogram
                            ax.hist(differences, bins=50, density=True, alpha=0.7, color='steelblue', 
                                   edgecolor='black', label='Sample Differences')
                            
                            # Calculate average sample standard deviations
                            avg_s1 = np.mean(sample_s1_list)
                            avg_s2 = np.mean(sample_s2_list)
                            
                            # Calculate standard error using sample std devs
                            if equal_vars:
                                # Pooled standard deviation approach
                                pooled_var = ((n1_mean_size - 1) * avg_s1**2 + (n2_mean_size - 1) * avg_s2**2) / (n1_mean_size + n2_mean_size - 2)
                                se = np.sqrt(pooled_var * (1/n1_mean_size + 1/n2_mean_size))
                                df = n1_mean_size + n2_mean_size - 2
                            else:
                                # Welch's approach
                                se = np.sqrt(avg_s1**2 / n1_mean_size + avg_s2**2 / n2_mean_size)
                                df = (avg_s1**2 / n1_mean_size + avg_s2**2 / n2_mean_size)**2 / \
                                     ((avg_s1**2 / n1_mean_size)**2 / (n1_mean_size - 1) + \
                                      (avg_s2**2 / n2_mean_size)**2 / (n2_mean_size - 1))
                            
                            # Overlay t-distribution curve
                            true_diff = mu1_pop - mu2_pop
                            x_range = np.linspace(min(differences), max(differences), 200)
                            t_curve = stats.t.pdf((x_range - true_diff) / se, df) / se
                            ax.plot(x_range, t_curve, 'r-', linewidth=2, 
                                   label=f't-distribution (df≈{df:.1f}, SE≈{se:.2f})')
                            
                            # Mark the true difference
                            ax.axvline(true_diff, color='darkgreen', linestyle='--', linewidth=2, 
                                      label=f'True Difference (μ₁ - μ₂ = {true_diff:.2f})')
                            
                            # Mark the mean of sample differences
                            mean_diff = np.mean(differences)
                            ax.axvline(mean_diff, color='orange', linestyle=':', linewidth=2, 
                                      label=f'Mean of Differences = {mean_diff:.2f}')
                            
                            ax.set_xlabel('Difference in Sample Means (x̄₁ - x̄₂)', fontsize=12)
                            ax.set_ylabel('Density', fontsize=12)
                            ax.set_title('Sampling Distribution of Difference Between Two Means (Using t-distribution)', fontsize=14, fontweight='bold')
                            ax.legend(loc='best', fontsize=10)
                            ax.grid(True, alpha=0.3)
                            
                            st.pyplot(fig)
                            plt.close()
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Calculate final statistics
                mean_diff = np.mean(differences)
                std_diff = np.std(differences, ddof=1)
                avg_s1 = np.mean(sample_s1_list)
                avg_s2 = np.mean(sample_s2_list)
                
                # Calculate standard error and degrees of freedom
                if equal_vars:
                    pooled_var = ((n1_mean_size - 1) * avg_s1**2 + (n2_mean_size - 1) * avg_s2**2) / (n1_mean_size + n2_mean_size - 2)
                    se_final = np.sqrt(pooled_var * (1/n1_mean_size + 1/n2_mean_size))
                    df_final = n1_mean_size + n2_mean_size - 2
                    pooled_s = np.sqrt(pooled_var)
                else:
                    se_final = np.sqrt(avg_s1**2 / n1_mean_size + avg_s2**2 / n2_mean_size)
                    df_final = (avg_s1**2 / n1_mean_size + avg_s2**2 / n2_mean_size)**2 / \
                               ((avg_s1**2 / n1_mean_size)**2 / (n1_mean_size - 1) + \
                                (avg_s2**2 / n2_mean_size)**2 / (n2_mean_size - 1))
                
                # Display final statistics
                with stats_placeholder.container():
                    st.write("---")
                    st.subheader("Summary Statistics")
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("Population 1 Mean (μ₁)", f"{mu1_pop:.2f}")
                        st.metric("Population 2 Mean (μ₂)", f"{mu2_pop:.2f}")
                        st.metric("True Difference (μ₁ - μ₂)", f"{mu1_pop - mu2_pop:.2f}")
                        st.metric("Number of Samples", f"{len(differences)}")
                    
                    with col_b:
                        st.metric("Mean of Sample Differences", f"{mean_diff:.2f}")
                        st.metric("Std Dev of Sample Differences", f"{std_diff:.2f}")
                        st.metric("Average Sample s₁", f"{avg_s1:.2f}")
                        st.metric("Average Sample s₂", f"{avg_s2:.2f}")
                    
                    with col_c:
                        st.metric("Standard Error (SE)", f"{se_final:.2f}")
                        st.metric("Degrees of Freedom", f"{df_final:.1f}")
                        if equal_vars:
                            st.metric("Pooled Std Dev (sp)", f"{pooled_s:.2f}")
                        else:
                            st.metric("Method", "Welch's")
                    
                    st.write("---")
                    st.write("**Key Observations:**")
                    st.write(f"- The mean of sample differences ({mean_diff:.2f}) should be close to the true difference ({mu1_pop - mu2_pop:.2f})")
                    st.write(f"- Using **sample standard deviations** (s₁ and s₂) to estimate the standard error")
                    st.write(f"- The **t-distribution** with df ≈ {df_final:.1f} is used instead of the normal distribution")
                    st.write(f"- Standard Error: SE ≈ {se_final:.2f}")
                    
                    if equal_vars:
                        st.write(f"- **Pooled approach**: Assumes equal population variances, df = n₁ + n₂ - 2 = {df_final:.0f}")
                        st.write(f"- Pooled standard deviation: sp = {pooled_s:.2f}")
                        st.write(f"- SE = sp × √(1/n₁ + 1/n₂)")
                    else:
                        st.write(f"- **Welch's approach**: Does not assume equal variances")
                        st.write(f"- Degrees of freedom calculated using Welch-Satterthwaite equation: df ≈ {df_final:.1f}")
                        st.write(f"- SE = √(s₁²/n₁ + s₂²/n₂)")
                    
                    st.write("**Note:** In practice, population standard deviations are unknown, so we use sample")
                    st.write("standard deviations and the t-distribution, which accounts for the additional uncertainty.")
                
            except Exception as e:
                st.error(f"An error occurred while running the simulation: {e}")
    
    with sim_tabs[8]:
        st.subheader("t-Distribution vs Standard Normal Distribution")
        st.write("""
        This simulation illustrates the key differences between the **t-distribution** and the **Standard Normal (Z) distribution**.
        The t-distribution is used when the population standard deviation is unknown and must be estimated from the sample.
        It has heavier tails than the normal distribution, especially with small sample sizes.
        """)
        
        # Create input columns
        col1, col2 = st.columns(2)
        
        with col1:
            df_value = st.slider(
                "Degrees of Freedom (df)", 
                min_value=1, 
                max_value=100, 
                value=5,
                help="Lower degrees of freedom → heavier tails and more spread"
            )
        
        with col2:
            show_multiple = st.checkbox(
                "Show Multiple df Values",
                value=False,
                help="Display multiple t-distributions with different degrees of freedom"
            )
        
        try:
            # Generate x values for plotting
            x = np.linspace(-5, 5, 1000)
            
            # Calculate distributions
            standard_normal = stats.norm.pdf(x, 0, 1)
            t_dist = stats.t.pdf(x, df_value)
            
            # Create the plot
            fig, ax = plt.subplots(figsize=(12, 7))
            
            # Plot Standard Normal
            ax.plot(x, standard_normal, 'b-', linewidth=2.5, label='Standard Normal (Z)', alpha=0.8)
            
            if show_multiple:
                # Show multiple t-distributions
                df_values = [1, 3, 5, 10, 30]
                colors = ['red', 'orange', 'green', 'purple', 'brown']
                
                for df, color in zip(df_values, colors):
                    t_curve = stats.t.pdf(x, df)
                    ax.plot(x, t_curve, color=color, linewidth=2, 
                           label=f't-distribution (df={df})', alpha=0.7)
            else:
                # Show single t-distribution
                ax.plot(x, t_dist, 'r-', linewidth=2.5, 
                       label=f't-distribution (df={df_value})', alpha=0.8)
            
            # Add shaded regions to highlight tail differences
            if not show_multiple:
                # Shade the tails beyond ±2
                tail_mask_right = x >= 2
                tail_mask_left = x <= -2
                
                ax.fill_between(x[tail_mask_right], 0, standard_normal[tail_mask_right], 
                               alpha=0.2, color='blue', label='Normal tail area')
                ax.fill_between(x[tail_mask_right], 0, t_dist[tail_mask_right], 
                               alpha=0.2, color='red', label='t-distribution tail area')
                
                ax.fill_between(x[tail_mask_left], 0, standard_normal[tail_mask_left], 
                               alpha=0.2, color='blue')
                ax.fill_between(x[tail_mask_left], 0, t_dist[tail_mask_left], 
                               alpha=0.2, color='red')
            
            # Styling
            ax.set_xlabel('Value', fontsize=12)
            ax.set_ylabel('Probability Density', fontsize=12)
            ax.set_title('Comparison: t-Distribution vs Standard Normal Distribution', 
                        fontsize=14, fontweight='bold')
            ax.legend(fontsize=10, loc='upper right')
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='black', linewidth=0.5)
            ax.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
            
            st.pyplot(fig)
            
            # Add comprehensive accessibility description
            if show_multiple:
                st.caption(f"""
                **Accessibility Description:** Comparison plot showing Standard Normal distribution (blue curve) 
                overlaid with multiple t-distributions at different degrees of freedom. 
                The t-distributions shown have df values of 1, 3, 5, 10, and 30 in colors red, orange, green, 
                purple, and brown respectively. As degrees of freedom increase, the t-distribution curves 
                converge toward the Standard Normal distribution. Distributions with lower df show heavier 
                tails and flatter peaks compared to the Standard Normal.
                """)
            else:
                st.caption(f"""
                **Accessibility Description:** Comparison plot showing Standard Normal distribution (blue curve) 
                overlaid with t-distribution having {df_value} degrees of freedom (red curve). 
                Shaded regions highlight differences in tail areas beyond ±2 standard deviations. 
                Blue shaded areas show Standard Normal tail probabilities, red shaded areas show 
                t-distribution tail probabilities. The t-distribution with df={df_value} has 
                {'heavier' if df_value < 30 else 'similar'} tails compared to the Standard Normal, 
                meaning extreme values are {'more' if df_value < 30 else 'similarly'} likely.
                """)
            plt.close()
            
            # Add interpretation section
            st.write("---")
            st.subheader("Key Differences")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.write("**Standard Normal (Z) Distribution:**")
                st.write("- Mean = 0, Standard Deviation = 1")
                st.write("- Used when σ (population std dev) is **known**")
                st.write("- Fixed shape - always the same")
                st.write("- Lighter tails")
                st.write("- Critical values: z* = 1.96 (95% confidence)")
                
            with col_b:
                st.write(f"**t-Distribution (df = {df_value}):**")
                st.write("- Mean = 0 (when df > 1)")
                st.write("- Used when σ is **unknown** (estimated by s)")
                st.write("- Shape depends on degrees of freedom")
                st.write("- Heavier tails (especially with small df)")
                t_critical = stats.t.ppf(0.975, df_value)
                st.write(f"- Critical values: t* = {t_critical:.3f} (95% confidence)")
            
            st.write("---")
            
            # Calculate and display tail probabilities
            st.subheader("Tail Probability Comparison")
            
            # Calculate probabilities beyond certain values
            test_values = [1.5, 2.0, 2.5, 3.0]
            
            comparison_data = {
                'Value': test_values,
                'P(Z > value)': [1 - stats.norm.cdf(v) for v in test_values],
                f'P(t > value) [df={df_value}]': [1 - stats.t.cdf(v, df_value) for v in test_values],
            }
            
            comparison_df = pd.DataFrame(comparison_data)
            comparison_df['P(Z > value)'] = comparison_df['P(Z > value)'].map('{:.4f}'.format)
            comparison_df[f'P(t > value) [df={df_value}]'] = comparison_df[f'P(t > value) [df={df_value}]'].map('{:.4f}'.format)
            
            st.dataframe(comparison_df, use_container_width=True)
            
            st.write("""
            **Observations:**
            - The t-distribution has **heavier tails**, meaning extreme values are more likely
            - As degrees of freedom increase, the t-distribution approaches the standard normal
            - With small sample sizes (low df), using the t-distribution is more conservative
            - When df ≥ 30, the t-distribution is very similar to the standard normal
            """)
            
            # Interactive section: Critical values
            st.write("---")
            st.subheader("Critical Values Comparison")
            
            confidence_level = st.slider(
                "Confidence Level (%)", 
                min_value=80, 
                max_value=99, 
                value=95,
                help="Select the confidence level to compare critical values"
            )
            
            alpha = 1 - confidence_level/100
            
            # Calculate critical values
            z_critical = stats.norm.ppf(1 - alpha/2)
            t_critical = stats.t.ppf(1 - alpha/2, df_value)
            
            col_c, col_d, col_e = st.columns(3)
            
            with col_c:
                st.metric("Confidence Level", f"{confidence_level}%")
            
            with col_d:
                st.metric("z* (Standard Normal)", f"{z_critical:.4f}")
            
            with col_e:
                st.metric(f"t* (df={df_value})", f"{t_critical:.4f}")
                difference = t_critical - z_critical
                st.metric("Difference (t* - z*)", f"{difference:.4f}")
            
            st.write(f"""
            - For a {confidence_level}% confidence interval, the t* critical value ({t_critical:.4f}) is 
            **{'larger' if t_critical > z_critical else 'smaller'}** than the z* critical value ({z_critical:.4f})
            - This results in **wider confidence intervals** when using the t-distribution
            - This accounts for the additional uncertainty from estimating σ with the sample standard deviation
            """)
            
        except Exception as e:
            st.error(f"An error occurred while generating the comparison: {e}")
    
    with sim_tabs[9]:
        st.subheader("F-Statistic Explorer: Understanding Within-Group and Between-Group Variation")
        st.write("""
        This interactive simulation helps you understand how the **F-statistic** in ANOVA is affected by:
        - **Between-group variation**: How different the group means are from each other
        - **Within-group variation**: How spread out the data is within each group
        
        The F-statistic measures the ratio: **F = (Between-Group Variability) / (Within-Group Variability)**
        """)
        
        # Create input columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Group 1 Parameters**")
            mean1 = st.slider(
                "Group 1 Mean", 
                min_value=0.0, 
                max_value=100.0, 
                value=50.0,
                step=1.0,
                help="Mean value for Group 1"
            )
            std1 = st.slider(
                "Group 1 Std Dev", 
                min_value=1.0, 
                max_value=20.0, 
                value=5.0,
                step=0.5,
                help="Standard deviation (spread) within Group 1"
            )
            n1 = st.slider(
                "Group 1 Sample Size", 
                min_value=5, 
                max_value=50, 
                value=30,
                step=5,
                help="Number of observations in Group 1"
            )
        
        with col2:
            st.write("**Group 2 Parameters**")
            mean2 = st.slider(
                "Group 2 Mean", 
                min_value=0.0, 
                max_value=100.0, 
                value=55.0,
                step=1.0,
                help="Mean value for Group 2"
            )
            std2 = st.slider(
                "Group 2 Std Dev", 
                min_value=1.0, 
                max_value=20.0, 
                value=5.0,
                step=0.5,
                help="Standard deviation (spread) within Group 2"
            )
            n2 = st.slider(
                "Group 2 Sample Size", 
                min_value=5, 
                max_value=50, 
                value=30,
                step=5,
                help="Number of observations in Group 2"
            )
        
        with col3:
            st.write("**Group 3 Parameters**")
            mean3 = st.slider(
                "Group 3 Mean", 
                min_value=0.0, 
                max_value=100.0, 
                value=60.0,
                step=1.0,
                help="Mean value for Group 3"
            )
            std3 = st.slider(
                "Group 3 Std Dev", 
                min_value=1.0, 
                max_value=20.0, 
                value=5.0,
                step=0.5,
                help="Standard deviation (spread) within Group 3"
            )
            n3 = st.slider(
                "Group 3 Sample Size", 
                min_value=5, 
                max_value=50, 
                value=30,
                step=5,
                help="Number of observations in Group 3"
            )
        
        try:
            # Generate data for each group
            np.random.seed(42)  # For reproducibility
            group1_data = np.random.normal(mean1, std1, n1)
            group2_data = np.random.normal(mean2, std2, n2)
            group3_data = np.random.normal(mean3, std3, n3)
            
            # Combine all data
            all_data = np.concatenate([group1_data, group2_data, group3_data])
            group_labels = ['Group 1'] * n1 + ['Group 2'] * n2 + ['Group 3'] * n3
            
            # Calculate statistics for ANOVA manually
            # Grand mean (overall mean)
            grand_mean = np.mean(all_data)
            
            # Calculate Between-Group Sum of Squares (SSB)
            ssb = n1 * (mean1 - grand_mean)**2 + n2 * (mean2 - grand_mean)**2 + n3 * (mean3 - grand_mean)**2
            
            # Calculate Within-Group Sum of Squares (SSW)
            ssw = np.sum((group1_data - mean1)**2) + np.sum((group2_data - mean2)**2) + np.sum((group3_data - mean3)**2)
            
            # Degrees of freedom
            k = 3  # Number of groups
            n_total = n1 + n2 + n3
            df_between = k - 1
            df_within = n_total - k
            
            # Mean Squares
            msb = ssb / df_between
            msw = ssw / df_within
            
            # F-statistic
            f_statistic = msb / msw if msw > 0 else 0
            
            # P-value
            p_value = 1 - stats.f.cdf(f_statistic, df_between, df_within)
            
            # Perform actual ANOVA test
            f_stat_scipy, p_value_scipy = stats.f_oneway(group1_data, group2_data, group3_data)
            
            # Create visualizations
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Plot 1: Dot plots for each group showing within-group variation
            ax1.scatter(np.ones(n1) * 1, group1_data, alpha=0.6, s=50, color='#0173B2', label='Group 1')
            ax1.scatter(np.ones(n2) * 2, group2_data, alpha=0.6, s=50, color='#DE8F05', label='Group 2')
            ax1.scatter(np.ones(n3) * 3, group3_data, alpha=0.6, s=50, color='#029E73', label='Group 3')
            
            # Add horizontal lines for group means
            ax1.hlines(mean1, 0.7, 1.3, colors='#0173B2', linewidth=3, label=f'Group 1 Mean = {mean1:.1f}')
            ax1.hlines(mean2, 1.7, 2.3, colors='#DE8F05', linewidth=3, label=f'Group 2 Mean = {mean2:.1f}')
            ax1.hlines(mean3, 2.7, 3.3, colors='#029E73', linewidth=3, label=f'Group 3 Mean = {mean3:.1f}')
            
            # Add grand mean line
            ax1.axhline(grand_mean, color='red', linestyle='--', linewidth=2, label=f'Grand Mean = {grand_mean:.1f}')
            
            ax1.set_xlim(0.5, 3.5)
            ax1.set_xticks([1, 2, 3])
            ax1.set_xticklabels(['Group 1', 'Group 2', 'Group 3'])
            ax1.set_ylabel('Value', fontsize=12)
            ax1.set_title('Data Distribution by Group\n(Within-Group Spread vs Between-Group Differences)', 
                         fontsize=13, fontweight='bold')
            ax1.grid(True, alpha=0.3, axis='y')
            ax1.legend(fontsize=8, loc='best')
            
            # Plot 2: Box plots showing variation
            positions = [1, 2, 3]
            bp = ax2.boxplot([group1_data, group2_data, group3_data], 
                            positions=positions,
                            widths=0.5,
                            patch_artist=True,
                            labels=['Group 1', 'Group 2', 'Group 3'])
            
            # Color the boxes
            colors = ['#0173B2', '#DE8F05', '#029E73']
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.6)
            
            # Add grand mean line
            ax2.axhline(grand_mean, color='red', linestyle='--', linewidth=2, label=f'Grand Mean = {grand_mean:.1f}')
            
            ax2.set_ylabel('Value', fontsize=12)
            ax2.set_title('Box Plots Showing Spread and Separation', fontsize=13, fontweight='bold')
            ax2.grid(True, alpha=0.3, axis='y')
            ax2.legend(fontsize=10)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Add comprehensive accessibility description
            st.caption(f"""
            **Accessibility Description:** Two-panel F-statistic visualization. 
            Left panel shows dot plot of individual data points for three groups: 
            Group 1 (blue circles, n={n1}) centered at mean {mean1:.1f} with standard deviation {std1:.1f}, 
            Group 2 (orange circles, n={n2}) centered at mean {mean2:.1f} with standard deviation {std2:.1f}, 
            Group 3 (green circles, n={n3}) centered at mean {mean3:.1f} with standard deviation {std3:.1f}. 
            Red dashed horizontal line marks grand mean at {grand_mean:.1f}. 
            Right panel displays box plots showing distribution spread for each group with quartiles, 
            median lines, and range whiskers. Grand mean marked with red dashed line. 
            Current F-statistic is {f_statistic:.4f} with p-value {p_value:.6f}.
            """)
            plt.close()
            
            # Display statistics
            st.write("---")
            st.subheader("ANOVA Calculation Breakdown")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.write("**Between-Group Variation**")
                st.write(f"- Sum of Squares Between (SSB): {ssb:.2f}")
                st.write(f"- Degrees of Freedom (df): {df_between}")
                st.write(f"- Mean Square Between (MSB): {msb:.2f}")
                st.write(f"- MSB measures how different the group means are from the grand mean")
            
            with col_b:
                st.write("**Within-Group Variation**")
                st.write(f"- Sum of Squares Within (SSW): {ssw:.2f}")
                st.write(f"- Degrees of Freedom (df): {df_within}")
                st.write(f"- Mean Square Within (MSW): {msw:.2f}")
                st.write(f"- MSW measures the average spread within groups")
            
            with col_c:
                st.write("**F-Statistic**")
                st.metric("F-value", f"{f_statistic:.4f}")
                st.metric("p-value", f"{p_value:.6f}")
                if p_value < 0.05:
                    st.success("✓ Significant at α = 0.05")
                else:
                    st.info("Not significant at α = 0.05")
            
            st.write("---")
            st.write("**F-Statistic Formula:**")
            st.latex(r"F = \frac{MSB}{MSW} = \frac{\text{Between-Group Variability}}{\text{Within-Group Variability}} = \frac{" + f"{msb:.2f}" + r"}{" + f"{msw:.2f}" + r"} = " + f"{f_statistic:.4f}")
            
            st.write("---")
            st.subheader("Key Insights")
            
            st.write("**Why Within-Group Spread Matters:**")
            st.write(f"- Current average within-group standard deviation: {np.mean([std1, std2, std3]):.2f}")
            st.write(f"- If groups have **high within-group variation** (large spread), it's harder to detect differences between groups")
            st.write(f"- This increases MSW (denominator), making F-statistic **smaller**")
            st.write(f"- Try increasing the standard deviations to see F decrease!")
            
            st.write("")
            st.write("**Why Between-Group Differences Matter:**")
            mean_diff = np.std([mean1, mean2, mean3])
            st.write(f"- Current separation between group means (std of means): {mean_diff:.2f}")
            st.write(f"- If group means are **far apart**, there's clear evidence of group differences")
            st.write(f"- This increases MSB (numerator), making F-statistic **larger**")
            st.write(f"- Try spreading the group means further apart to see F increase!")
            
            st.write("")
            st.write("**The F-Statistic Tells Us:**")
            if f_statistic > 5:
                st.write(f"- F = {f_statistic:.2f} is **large**, indicating that between-group differences are much larger than within-group variation")
                st.write(f"- Strong evidence that at least one group mean is significantly different")
            elif f_statistic > 2:
                st.write(f"- F = {f_statistic:.2f} suggests moderate evidence of group differences")
                st.write(f"- Between-group variation is larger than within-group variation")
            else:
                st.write(f"- F = {f_statistic:.2f} is **small**, indicating that between-group differences are not much larger than within-group variation")
                st.write(f"- Weak evidence for differences between groups")
            
            st.write("---")
            st.info("""
            **Try These Experiments:**
            1. **Keep means the same, increase standard deviations** → F decreases (harder to detect differences)
            2. **Keep standard deviations the same, spread means apart** → F increases (easier to detect differences)
            3. **Make all means equal** → F approaches 0 (no between-group differences)
            4. **Make standard deviations very small and means different** → F becomes very large (clear group differences)
            
            This demonstrates why ANOVA is sensitive to both the separation of means AND the consistency within groups!
            """)
            
        except Exception as e:
            st.error(f"An error occurred while running the F-statistic explorer: {e}")

# Placeholder for other tabs
else:
    st.header(selected_tab)
    st.info("This tab is under construction. Please use the 'Data Input' tab first to load or enter data.")
