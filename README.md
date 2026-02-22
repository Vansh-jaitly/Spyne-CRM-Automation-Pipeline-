# Spyne-CRM-Automation-Pipeline

End-to-end Selenium automation integrated with HubSpot CRM for dealership data scraping and analysis.

## 📋 Overview

This project provides a Streamlit-based web application with two powerful web scraping tools designed for automotive dealership data collection:

1. **DealerOn Vehicle Count Scraper** - Scrapes new and used vehicle counts from dealership websites
2. **Staff Finder** - Analyzes dealership websites for staff-related information and team pages

## ✨ Features

### DealerOn Vehicle Count Scraper
- Automatically scrapes vehicle counts from dealership websites
- Supports multiple XPath strategies for robust data extraction
- Handles both new and used vehicle inventory
- Website status validation (Relevant/Irrelevant/Timeout)
- CSV input/output support

### Staff Finder
- Searches for staff-related keywords across dealership websites
- Checks multiple common staff page URLs (`/staff`, `/team`, `/meet-our-staff`, etc.)
- Provides detailed word count analysis for staff-related terms
- Identifies presence of dedicated staff pages

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vansh-jaitly/Spyne-CRM-Automation-Pipeline-.git
   cd Spyne-CRM-Automation-Pipeline-
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit pandas selenium
   ```

3. **Install ChromeDriver**
   - Download ChromeDriver from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
   - Ensure ChromeDriver is in your system PATH, or install via package manager:
     ```bash
     # Windows (using Chocolatey)
     choco install chromedriver
     
     # macOS (using Homebrew)
     brew install chromedriver
     
     # Linux
     sudo apt-get install chromium-chromedriver
     ```

## 📖 Usage

### Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Access the web interface**
   - Open your browser and navigate to `http://localhost:8501`

3. **Using the Tools**
   - Select your desired tool (DealerOn Scraper or Staff Finder)
   - Upload a CSV file with the required columns:
     - **For DealerOn Scraper**: `Company name`, `Company Domain Name`
     - **For Staff Finder**: `Company Domain Name`
   - Wait for the scraping to complete
   - Download the results as a CSV file

### CSV Input Format

**DealerOn Scraper Input:**
```csv
Company name,Company Domain Name
ABC Motors,www.abcmotors.com
XYZ Dealership,xyzdealership.com
```

**Staff Finder Input:**
```csv
Company Domain Name
www.abcmotors.com
xyzdealership.com
```

## 📁 Project Structure

```
Spyne_Final/
├── app.py                  # Streamlit web application
├── dealeron_scraper.py     # Vehicle count scraper module
├── staff_finder.py         # Staff information finder module
└── README.md               # Project documentation
```

## 🔧 Technical Details

### Technologies Used
- **Streamlit** - Web application framework
- **Selenium** - Web automation and scraping
- **Pandas** - Data manipulation and CSV handling
- **Chrome WebDriver** - Browser automation

### Key Features
- Headless browser mode for efficient scraping
- Robust error handling and timeout management
- Multiple XPath fallback strategies
- Progress logging and status reporting
- CSV export functionality

## 🛠️ Configuration

The scrapers use optimized Chrome options for headless operation:
- Headless mode enabled
- Disabled GPU and sandbox for stability
- Custom user agent strings
- Page load timeout management

## 📝 Output Format

### DealerOn Scraper Output
- `Company name` - Original company name
- `Company Domain Name` - Website URL
- `Number Of New Cars` - Count of new vehicles (or "NA")
- `Number Of Used Cars` - Count of used vehicles (or "NA")
- `Website Status` - Relevance status

### Staff Finder Output
- `Company Domain Name` - Website URL
- `Status` - Staff information status
- `Staff_Page_Found` - Yes/No indicator
- `Total_Matches` - Total keyword matches
- Individual word counts for: `staff`, `team`, `management`, `sales`, `service`

## ⚠️ Notes

- Scraping may take time depending on the number of websites and their response times
- Some websites may block automated scraping; results may vary
- Ensure you comply with website terms of service and robots.txt policies
- The application uses headless Chrome, which requires ChromeDriver to be properly installed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is part of the Spyne CRM Automation Pipeline.

## 🔗 Repository

[GitHub Repository](https://github.com/Vansh-jaitly/Spyne-CRM-Automation-Pipeline-)
