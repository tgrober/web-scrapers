from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets'];

# The ID and range of a sample spreadsheet.
spreadID = '1AjYIpux4VQj-ui9x4SSpHi-76QlRrdpBKpKCtKwiuSM'
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'A1:AA100'
teams = ['OKC','LAC','MIL']
lines = ['-5.5','-3.0','-4.0']
rangeDoc = 'A1:C1'
from pprint import pprint

from googleapiclient import discovery

def main():
    
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    print(values)
    if not values:
        print('No data found.')
    
    request = service.spreadsheets().values().update(spreadsheetId=spreadID, range=rangeDoc, valueInputOption=value_input_option, body=teams)
    response = request.execute()


if __name__ == '__main__':
    main()