# Privacy Policy
Effective Date: 2025-05-16

This privacy policy explains how the application "SEO Automation" (https://seo-automation.streamlit.app/) uses and protects your data when you use Google OAuth2 to log in and work with your Google Sheets.

## What Data We Access
When you use our app and sign in with your Google account, we request the following permissions (OAuth scopes):
- https://www.googleapis.com/auth/drive.file - allows access only to files you explicitly select and authorize.
- https://www.googleapis.com/auth/spreadsheets - allows reading and editing those authorized Google Sheets.

Although Google may warn that access is requested for "all your Google Sheets", due to the restrictions imposed by `drive.file` scope, our app can only interact with files you have manually selected and granted access to (entered a link to the document into our application).

From your Google account, we access:
- Your full name.
- Your email address.
- A refresh token (used to obtain a temporary access token).

## Why We Access This Data
Name and email are only used to display your account info within the app interface.

Refresh token is used to request short-lived access tokens from Google, enabling the app to read and edit your selected Google Sheets. The refresh token is valid for 7 days. After that, you will need to log in again.

## Data Storage and Security
We do not store any of your data on our servers. No database or external storage is used. All data retrieved during authentication is stored only in your browser's cookies and remains on your device.

The cookies are securely encrypted using a secret key that is stored safely on the server (not in the app's source code). These cookies are bound to the domain https://seo-automation.streamlit.app/ and cannot be accessed by any other site or app.

Once you close your browser tab, the app does not retain any access to your data.

## Google Sheets Editing Policy
Our tools are designed to never delete any existing data in your Google Sheets. We follow a strict non-destructive principle:
- The app only adds new data or formatting to your spreadsheets.
- Formatting can be removed manually, and any inserted data can be filtered or deleted by you.

The app may assist you in marking certain rows or columns for easier filtering or manual deletion, but it will never delete data automatically.

## Open Source Code
Our project is fully open-source. You can view the source code here:
https://github.com/ilarionkuleshov/seo-automation

## Contact
If you have any questions or concerns about this privacy policy, feel free to contact us at: ilarion.kuleshov@gmail.com
