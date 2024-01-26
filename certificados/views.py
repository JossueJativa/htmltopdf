import base64
import json
from django.conf import settings
from django.shortcuts import render  # Add this import
from django.template.loader import get_template
import pika
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def certificado(request, username, course, date, email):
    message = f'Querido {username}, ha concluido el curso de {course} el día {date}. ¡Felicidades!'
    template = 'certificado.html'

    data = {
        'message': message,
        'username': username,
        'course': course,
        'date': date,
        'email': email
    }

    pdf_renderer = render_to_pdf(template, data)

    if pdf_renderer:
        # Enqueue the task to RabbitMQ
        enqueue_email_task(username, course, date, email, pdf_renderer)
        return HttpResponse('Processing your request. You will receive an email shortly.')
    else:
        return HttpResponseBadRequest('Error Rendering PDF', status=400)

def enqueue_email_task(username, course, date, email, pdf_content):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Change to your RabbitMQ server
        channel = connection.channel()

        channel.queue_declare(queue='email_queue')

        task_data = {
            'username': username,
            'course': course,
            'date': date,
            'email': email,
            'pdf_content': base64.b64encode(pdf_content).decode('utf-8')  # Encode the PDF content as base64
        }

        channel.basic_publish(exchange='',
                              routing_key='email_queue',
                              body=json.dumps(task_data))

        connection.close()
    except Exception as e:
        print("Error enqueuing email task:", str(e))

def render_to_pdf(template, data):
    template = get_template(template)
    context = template.render(data)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(context.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None
