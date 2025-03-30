# QR Code Generator

A powerful and user-friendly QR Code Generator application built with Streamlit. This application allows you to generate QR codes for various types of content including text, URLs, WiFi networks, and contact information.

## Live Demo
Try the application online: [QR Code Generator](https://saz-qr-code-generator.streamlit.app/)

## Features

- Generate QR codes for:
  - Plain text
  - URLs
  - WiFi networks
  - Contact information (vCard format)
- Customize QR code appearance:
  - Size adjustment
  - Color customization
  - Error correction level
  - Background color
- Download generated QR codes as PNG files
- Modern and responsive user interface
- Easy-to-use tabs for different QR code types

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run main.py
```
 OR
```bash
python -m streamlit run main.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Choose the type of QR code you want to generate from the tabs at the top

4. Customize the QR code appearance using the settings in the sidebar

5. Enter the required information and click "Generate QR Code"

6. Download the generated QR code using the download button

## QR Code Types

### Text QR Code
- Generate QR codes containing any text content
- Perfect for sharing messages, notes, or any text-based information

### URL QR Code
- Create QR codes that link to websites
- Automatically adds https:// if not present
- Great for sharing website links

### WiFi QR Code
- Generate QR codes for WiFi networks
- Includes network name, password, and security type
- Makes it easy to share WiFi access with guests

### Contact QR Code
- Create QR codes containing contact information
- Includes name, phone, email, company, title, and website
- Compatible with most smartphone contact apps

## Customization Options

- **Size**: Adjust the QR code size from 100 to 400 pixels
- **Error Correction**: Choose from L (Low), M (Medium), Q (Quartile), or H (High)
- **Colors**: Customize both the QR code and background colors
- **Download**: Save QR codes as PNG files with timestamps

## Requirements

- Python 3.7+
- streamlit
- qrcode
- pillow
