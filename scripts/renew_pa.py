import requests
import os
import sys
import re

def renew_pythonanywhere():
    username = os.environ.get('PA_USERNAME')
    password = os.environ.get('PA_PASSWORD')
    
    if not username or not password:
        print("❌ Error: PA_USERNAME and PA_PASSWORD environment variables are required.")
        sys.exit(1)

    domain = os.environ.get('PA_DOMAIN', f'{username}.pythonanywhere.com')
    login_url = 'https://www.pythonanywhere.com/login/'
    dashboard_url = f'https://www.pythonanywhere.com/user/{username}/webapps/'

    print(f"🚀 Starting renewal process for user: '{username}'")
    print(f"🎯 Target domain hint: '{domain}'")

    session = requests.Session()

    # 1. Get login page to fetch CSRF token
    print(f"1️⃣  Fetching login page: {login_url}")
    try:
        login_page = session.get(login_url)
        login_page.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to load login page: {e}")
        sys.exit(1)

    if 'csrftoken' not in session.cookies:
        print("❌ CSRF token not found in cookies.")
        sys.exit(1)
    
    csrf_token = session.cookies['csrftoken']
    print(f"   🔑 Got CSRF token: {csrf_token[:10]}...")

    # 2. Perform Login
    print("2️⃣  Logging in...")
    login_data = {
        'auth-username': username,
        'auth-password': password,
        'csrfmiddlewaretoken': csrf_token,
        'login_view-current_step': 'auth'
    }
    
    headers = {
        'Referer': login_url,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }

    try:
        response = session.post(login_url, data=login_data, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Login request failed: {e}")
        sys.exit(1)

    # Verify login success
    if 'Log out' not in response.text and 'Dashboard' not in response.text:
        print("❌ Login failed. Please check your credentials.")
        print("   📄 Login response preview:")
        print(response.text[:500])
        sys.exit(1)
    
    print("✅ Login successful.")

    # 3. Get Dashboard to find the Extend URL
    print(f"3️⃣  Fetching dashboard: {dashboard_url}")
    try:
        dashboard_page = session.get(dashboard_url, headers=headers)
        dashboard_page.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to load dashboard: {e}")
        sys.exit(1)

    # Find the extend action URL
    print("   🔍 Searching for extension URL in dashboard HTML...")
    
    # Search for ANY extend URL first to see what we find
    # Looking for form action like: /user/username/webapps/domain.com/extend
    matches = re.findall(r'action="([^"]+/extend)"', dashboard_page.text)
    
    if not matches:
        print(f"❌ Could not find any extension URL on dashboard.")
        print("   📄 Dashboard HTML preview (first 2000 chars):")
        print(dashboard_page.text[:2000])
        print("   💾 Dumping full dashboard to 'dashboard_dump.html'...")
        with open("dashboard_dump.html", "w", encoding="utf-8") as f:
            f.write(dashboard_page.text)
        sys.exit(1)

    print(f"   👀 Found candidate extension URLs: {matches}")
    
    # Select the best match based on domain
    relative_extend_url = None
    for url in matches:
        if domain in url:
            relative_extend_url = url
            break
    
    # Fallback: if only one exists, use it (useful if PA_DOMAIN isn't exact)
    if not relative_extend_url and len(matches) == 1:
        print("   ⚠️  Domain not found in URL, but only one app exists. Using it.")
        relative_extend_url = matches[0]
    
    if not relative_extend_url:
        print(f"❌ Could not match domain '{domain}' to any found extension URL.")
        print(f"   Available options were: {matches}")
        sys.exit(1)

    final_extend_url = f"https://www.pythonanywhere.com{relative_extend_url}"
    print(f"   ✅ Selected extension URL: {final_extend_url}")

    # 4. Extend the Web App
    print("4️⃣  Extending web app...")
    
    # Update CSRF token
    if 'csrftoken' in session.cookies:
        csrf_token = session.cookies['csrftoken']

    extend_data = {
        'csrfmiddlewaretoken': csrf_token
    }
    
    headers['Referer'] = dashboard_url

    try:
        print(f"   📤 Sending POST request to {final_extend_url}")
        response = session.post(final_extend_url, data=extend_data, headers=headers)
        print(f"   📥 Status Code: {response.status_code}")
        
        try:
            result_json = response.json()
            if result_json.get('status') == 'OK':
                print(f"✅ Successfully extended!")
                print(f"   🎉 New expiry: {result_json.get('expires')}")
            else:
                print(f"⚠️  Extension request returned unexpected status: {result_json}")
                print("   📄 Full JSON response:", result_json)
        except ValueError:
            # PythonAnywhere returns 200 OK with HTML on success, not JSON
            if response.status_code == 200:
                print(f"✅ Successfully extended! (HTTP 200)")
                print(f"   The 'Run until 3 months from today' button was triggered successfully.")
            else:
                print(f"❌ Failed. Response was not JSON and Status Code is {response.status_code}.")
                print(f"   Response content preview: {response.text[:1000]}")
                sys.exit(1)

    except Exception as e:
        print(f"❌ Failed to extend web app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    renew_pythonanywhere()
