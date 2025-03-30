import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFilter
import io
import base64
from datetime import datetime
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import tempfile
import os

# Set page config
st.set_page_config(
    page_title="QR Code Generator",
    page_icon="🔲",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin-top: 10px;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .qr-preview {
        transition: transform 0.3s ease;
    }
    .qr-preview:hover {
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🔲 Advanced QR Code Generator")
st.markdown("Generate and scan QR codes with advanced features!")

# Sidebar for QR code customization
with st.sidebar:
    st.header("QR Code Settings")
    
    # QR code size
    qr_size = st.slider("QR Code Size", 100, 400, 200)
    
    # Error correction level
    error_correction = st.selectbox(
        "Error Correction Level",
        ["L", "M", "Q", "H"],
        help="Higher levels provide better error correction but increase QR code complexity"
    )
    
    # QR code color
    qr_color = st.color_picker("QR Code Color", "#000000")
    
    # Background color
    bg_color = st.color_picker("Background Color", "#FFFFFF")
    
    # Style options
    st.subheader("Style Options")
    style = st.selectbox(
        "QR Code Style",
        ["Classic", "Rounded", "Dots", "Artistic"],
        help="Choose different styles for your QR code"
    )
    
    # Logo upload
    st.subheader("Add Logo")
    logo_file = st.file_uploader("Upload Logo (PNG with transparency)", type=['png'])
    
    # Animation options
    st.subheader("Animation")
    animate = st.checkbox("Enable Animation Preview", value=False)
    if animate:
        animation_speed = st.slider("Animation Speed", 1, 5, 3)

# Main content area
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Text", "URL", "WiFi", "Contact", "Batch", "Scan"])

def create_qr_with_logo(data, logo=None, style="Classic"):
    # Calculate box size based on desired QR code size
    # For a QR code with border=4, we need to account for the border in our calculation
    box_size = qr_size // 25  # Adjusted for better size control
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{error_correction}"),
        box_size=box_size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create QR code image with exact size
    img = qr.make_image(fill_color=qr_color, back_color=bg_color)
    img = img.convert('RGBA')
    
    # Get image dimensions
    width, height = img.size
    
    # Apply style
    if style == "Rounded":
        # Create rounded corners effect
        radius = 20
        new_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        new_img.paste(img, (0, 0))
        mask = Image.new('L', (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (width, height)], radius, fill=255)
        output = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        output.paste(new_img, mask=mask)
        img = output
    elif style == "Dots":
        # Create dots effect
        img = img.resize((width * 2, height * 2), Image.NEAREST)
        img = img.filter(ImageFilter.GaussianBlur(1))
        # Resize back to original size
        img = img.resize((width, height), Image.NEAREST)
    
    # Add logo if provided
    if logo:
        try:
            # Open the uploaded file as an image
            logo_img = Image.open(logo)
            # Convert to RGBA if not already
            if logo_img.mode != 'RGBA':
                logo_img = logo_img.convert('RGBA')
            
            # Resize logo
            logo_size = int(qr_size * 0.2)
            logo_img = logo_img.resize((logo_size, logo_size), Image.NEAREST)
            
            # Calculate position to center the logo
            pos = ((img.size[0] - logo_img.size[0]) // 2,
                   (img.size[1] - logo_img.size[1]) // 2)
            
            # Paste logo onto QR code
            img.paste(logo_img, pos, logo_img)
        except Exception as e:
            st.warning(f"Could not process logo: {str(e)}")
    
    return img

def generate_animated_qr(data, logo=None, style="Classic", frames=10):
    frames_list = []
    for i in range(frames):
        angle = (i / frames) * 360
        img = create_qr_with_logo(data, logo, style)
        if angle > 0:
            img = img.rotate(angle, expand=True, resample=Image.BICUBIC)
        frames_list.append(img)
    return frames_list

# Text QR Code
with tab1:
    st.header("Text QR Code")
    text_content = st.text_area("Enter your text", height=100)
    if st.button("Generate Text QR Code"):
        if text_content:
            img = create_qr_with_logo(text_content, logo_file, style)
            
            if animate:
                frames = generate_animated_qr(text_content, logo_file, style)
                # Display each frame with its own caption
                for i, frame in enumerate(frames):
                    st.image(frame, caption=f"Frame {i+1}", use_column_width=True)
            else:
                st.image(img, caption="QR Code Preview", use_column_width=True)
            
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            st.download_button(
                "Download QR Code",
                buffered.getvalue(),
                file_name=f"text_qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )
        else:
            st.warning("Please enter some text!")

# URL QR Code
with tab2:
    st.header("URL QR Code")
    url_content = st.text_input("Enter URL", placeholder="https://example.com")
    if st.button("Generate URL QR Code"):
        if url_content:
            if not url_content.startswith(('http://', 'https://')):
                url_content = 'https://' + url_content
            
            img = create_qr_with_logo(url_content, logo_file, style)
            
            if animate:
                frames = generate_animated_qr(url_content, logo_file, style)
                # Display each frame with its own caption
                for i, frame in enumerate(frames):
                    st.image(frame, caption=f"Frame {i+1}", use_column_width=True)
            else:
                st.image(img, caption="QR Code Preview", use_column_width=True)
            
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            st.download_button(
                "Download QR Code",
                buffered.getvalue(),
                file_name=f"url_qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )
        else:
            st.warning("Please enter a URL!")

# WiFi QR Code
with tab3:
    st.header("WiFi QR Code")
    col1, col2 = st.columns(2)
    with col1:
        ssid = st.text_input("WiFi Name (SSID)")
    with col2:
        password = st.text_input("WiFi Password", type="password")
    wifi_type = st.selectbox("WiFi Type", ["WPA", "WEP", "nopass"])
    hidden = st.checkbox("Hidden Network")
    
    if st.button("Generate WiFi QR Code"):
        if ssid:
            wifi_data = f"WIFI:T:{wifi_type};S:{ssid};P:{password};H:{str(hidden).lower()};"
            
            img = create_qr_with_logo(wifi_data, logo_file, style)
            
            if animate:
                frames = generate_animated_qr(wifi_data, logo_file, style)
                # Display each frame with its own caption
                for i, frame in enumerate(frames):
                    st.image(frame, caption=f"Frame {i+1}", use_column_width=True)
            else:
                st.image(img, caption="QR Code Preview", use_column_width=True)
            
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            st.download_button(
                "Download QR Code",
                buffered.getvalue(),
                file_name=f"wifi_qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )
        else:
            st.warning("Please enter a WiFi name!")

# Contact QR Code (vCard)
with tab4:
    st.header("Contact QR Code (vCard)")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
    with col2:
        company = st.text_input("Company")
        title = st.text_input("Title")
        website = st.text_input("Website")
    
    if st.button("Generate Contact QR Code"):
        if name:
            vcard_data = f"""BEGIN:VCARD
VERSION:3.0
N:{name}
TEL:{phone}
EMAIL:{email}
ORG:{company}
TITLE:{title}
URL:{website}
END:VCARD"""
            
            img = create_qr_with_logo(vcard_data, logo_file, style)
            
            if animate:
                frames = generate_animated_qr(vcard_data, logo_file, style)
                # Display each frame with its own caption
                for i, frame in enumerate(frames):
                    st.image(frame, caption=f"Frame {i+1}", use_column_width=True)
            else:
                st.image(img, caption="QR Code Preview", use_column_width=True)
            
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            st.download_button(
                "Download QR Code",
                buffered.getvalue(),
                file_name=f"contact_qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )
        else:
            st.warning("Please enter at least a name!")

# Batch QR Code Generation
with tab5:
    st.header("Batch QR Code Generation")
    st.write("Upload a CSV file with data to generate multiple QR codes")
    batch_file = st.file_uploader("Upload CSV File", type=['csv'])
    
    if batch_file:
        import pandas as pd
        df = pd.read_csv(batch_file)
        st.write("Preview of your data:")
        st.dataframe(df.head())
        
        if st.button("Generate Batch QR Codes"):
            for index, row in df.iterrows():
                # Create QR code for each row
                data = str(row.to_dict())
                img = create_qr_with_logo(data, logo_file, style)
                
                # Save QR code
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                
                # Create download button
                st.download_button(
                    f"Download QR Code {index + 1}",
                    buffered.getvalue(),
                    file_name=f"batch_qr_{index + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png"
                )

# QR Code Scanner
with tab6:
    st.header("QR Code Scanner")
    st.write("Use your camera to scan QR codes")
    
    webrtc_streamer(key="qr-scanner")
    
    uploaded_file = st.file_uploader("Or upload an image with QR code", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Read image
        img = cv2.imread(tmp_file_path)
        
        # Initialize QR code detector
        detector = cv2.QRCodeDetector()
        
        # Detect QR code
        data, bbox, _ = detector.detectAndDecode(img)
        
        if data:
            st.success(f"QR Code detected! Content: {data}")
        else:
            st.error("No QR code detected in the image")
        
        # Clean up temporary file
        os.unlink(tmp_file_path)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit") 