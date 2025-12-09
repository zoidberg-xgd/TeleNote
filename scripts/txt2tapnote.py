import argparse
import requests
import os
import sys

def convert_txt_to_tapnote(file_path, server_url, public_domain=None):
    print("⚠️  DEPRECATION WARNING: This script is deprecated.")
    print("👉 Please use 'telepress' which is much more powerful.")
    print("   Usage: telepress <file> --api-url <url>")
    print("-" * 50)

    """
    Reads a text file and posts it to TapNote to create a new page.
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    if not content.strip():
        print("❌ Error: File is empty.")
        return

    publish_url = f"{server_url.rstrip('/')}/publish/"
    
    print(f"📤 Uploading '{file_path}' to {publish_url}...")

    try:
        # Send POST request
        # allow_redirects=False to capture the 302 Location header directly
        response = requests.post(publish_url, data={'content': content}, allow_redirects=False)
        
        if response.status_code == 302:
            location = response.headers.get('Location')
            # Location is likely relative, e.g., '/<hashcode>/'
            
            base_url = public_domain.rstrip('/') if public_domain else server_url.rstrip('/')
            
            if location.startswith('http'):
                # If server returned full URL, and we want to force a domain
                if public_domain:
                    # Replace protocol and domain
                    # Simple way: split by / and replace first part?
                    # Or just use hashcode if we can extract it.
                    # location format: http://host/hash/
                    parts = location.split('/')
                    # parts[-2] should be hashcode if ends with /
                    # http://host/hash/ -> ['http:', '', 'host', 'hash', '']
                    if len(parts) >= 4:
                         # Reconstruct using public_domain + path
                         path = '/' + '/'.join(parts[3:])
                         full_url = f"{base_url}{path}"
                    else:
                         full_url = location # Fallback
                else:
                    full_url = location
            else:
                full_url = f"{base_url}{location}"
            
            print(f"✅ Successfully published!")
            print(f"🔗 URL: {full_url}")
            
        elif response.status_code == 200:
            # If it didn't redirect, maybe it returned the editor with an error (e.g. too long)
            print(f"⚠️  Server returned 200 OK (did not redirect). Check for errors.")
            if "Error!" in response.text:
                print("   Server reported an error in the response HTML.")
        else:
            print(f"❌ Failed to publish. Status Code: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")

    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a text file to a TapNote page.")
    parser.add_argument("file", help="Path to the text file to convert")
    parser.add_argument("--server", default="http://localhost:9009", help="TapNote server URL (default: http://localhost:9009)")
    parser.add_argument("--domain", help="Public domain to use in the output URL (e.g. https://mynote.com). Useful if deploying behind a proxy.")
    
    args = parser.parse_args()
    
    convert_txt_to_tapnote(args.file, args.server, args.domain)
