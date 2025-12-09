import argparse
import os
import sys
from urllib.parse import urlparse

try:
    from telepress import TelegraphPublisher
except ImportError:
    print("❌ Error: 'telepress' package is not installed.")
    print("👉 Please install it using 'pip install telepress'.")
    sys.exit(1)

def convert_txt_to_tapnote(file_path, server_url, public_domain=None):
    """
    Reads a text file and posts it to TapNote (via telepress) to create a new page.
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return

    print(f"🚀 Publishing '{file_path}' using telepress...")
    
    try:
        # Initialize publisher with custom API URL
        publisher = TelegraphPublisher(api_url=server_url)
        
        # Publish the file
        url = publisher.publish(file_path)
        
        # Handle public_domain replacement if provided
        if public_domain:
            parsed = urlparse(url)
            base_url = public_domain.rstrip('/')
            full_url = f"{base_url}{parsed.path}"
        else:
            full_url = url
            
        print(f"✅ Successfully published!")
        print(f"🔗 URL: {full_url}")

    except Exception as e:
        print(f"❌ Publish failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a text file to a TapNote page.")
    parser.add_argument("file", help="Path to the text file to convert")
    parser.add_argument("--server", default="http://localhost:9009", help="TapNote server URL (default: http://localhost:9009)")
    parser.add_argument("--domain", help="Public domain to use in the output URL (e.g. https://mynote.com). Useful if deploying behind a proxy.")
    
    args = parser.parse_args()
    
    convert_txt_to_tapnote(args.file, args.server, args.domain)
