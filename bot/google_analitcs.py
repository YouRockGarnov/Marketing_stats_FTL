import pandas as pd

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'google_key.json'
VIEW_ID = '204828335'


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = discovery.build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report_from_analitics(analytics):
    """Queries the Analytics Reporting API V4.

    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
      The Analytics Reporting API V4 response.
    """
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
                    'metrics': [
                        {'expression': 'ga:adxImpressions'},
                        {'expression': 'ga:adxCoverage'},
                        {'expression': 'ga:adxMonetizedPageviews'},
                        {'expression': 'ga:adxImpressionsPerSession'},
                        {'expression': 'ga:adxViewableImpressionsPercent'},
                        {'expression': 'ga:adxClicks'},
                        {'expression': 'ga:adxCTR'},
                        {'expression': 'ga:adxRevenue'},
                        {'expression': 'ga:adxRevenuePer1000Sessions'},
                        {'expression': 'ga:adxECPM'},
                    ],
                    'dimensions': [{'name': 'ga:country'}]
                }]
        }
    ).execute()


def create_data_frame_response(response) -> pd.DataFrame:
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
      response: An Analytics Reporting API V4 response.
    """

    for report in response.get('reports', []):
        values = report.get('data', {}).get('totals', [])

        return pd.DataFrame(map(lambda o:o['values'], values)
        , columns=[
            'AdX Impressions',
            'AdX Coverage',
            'AdX Monetized Pageviews',
            'AdX Impressions / Session',
            'AdX Viewable Impressions %',
            'AdX Clicks',
            'AdX CTR',
            'AdX Revenue',
            'AdX Revenue / 1000 Sessions',
            'AdX eCPM'
        ])



def get_report() -> pd.DataFrame:
    analytics = initialize_analyticsreporting()
    response = get_report_from_analitics(analytics)
    return create_data_frame_response(response)
