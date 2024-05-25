
import boto3
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import json

s3 = boto3.client('s3')
bucket_name = 'pdfreceiptbucketforiicnose'
def hello(event, context):
    pdf_canvas = canvas.Canvas("/tmp/receipt.pdf", pagesize=letter)
    pdf_canvas.drawString(30, 750, "Receipt")
    pdf_canvas.drawString(60, 730, "Company id: {}".format(event['id']))
    pdf_canvas.drawString(60, 700, "Departure airport: {}".format(event['departure_airport_id']))
    pdf_canvas.drawString(60, 670, "Arrival airport: {}".format(event['arrival_airport_id']))
    pdf_canvas.drawString(60, 640, "Departure time: {}".format(event['departure_time']))
    pdf_canvas.drawString(60, 610, "quantity: {}".format(event['quantity']))

    
    pdf_data = pdf_canvas.getpdfdata()
    s3.put_object(Bucket=bucket_name,
                  Key='lambdademo/generated{}.pdf'.format(event['id']), Body=pdf_data)
    
    s3_url = f"https://{bucket_name}.s3.amazonaws.com/lambdademo/generated{event['id']}.pdf"
    
    return {
        'statusCode': 200,
        'body': 'PDF generated and saved to S3',
        'url': s3_url
    }

