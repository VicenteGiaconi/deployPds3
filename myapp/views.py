from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout
from django.core.mail import EmailMessage

from rest_framework.views import View

import json

# from django.views.decorators.csrf import csrf_exempt

import os
from django.conf import settings

import paho.mqtt.client as paho
from paho import mqtt


# from mqtt import mqtt

broker = '27b6ae85dfb5497bb8e3e592bed69c85.s1.eu.hivemq.cloud'
port = 8883
# topic_send = "Password"
# topic_response = "django/response"
topic_out = "Password"
topic_in = "Open"
client_id = "Django-client"
client = paho.Client(client_id, userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

client.username_pw_set("PaginaWeb", "Hive2001!")

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Conectado con código de resultado: {rc}")
    client.subscribe(topic_in)
    client.subscribe(topic_out)

def on_message(client, userdata, msg):
    from myapp.models import Casillero
    from myapp.serializers import CasilleroSerializer
    if msg.topic == "Open":
        print(f"Mensaje recibido desde ESP32 en {msg.topic}: {msg.payload.decode()}")

        a = json.loads(msg.payload.decode())

        casillero = Casillero.objects.get(id=a['locker_id'])
        casillero_serializer = CasilleroSerializer(casillero).data

        send_open_mail(casillero_serializer)
                                                          
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.loop_start()

# Create your views here.

class logout_view(View):
    def post(self, request):
        logout(request)
        return redirect("/")
    
class home(View):
    def get(self, request):
        return render(request, "home.html")

class controller_view(View):
    def get(self, request):
        from myapp.models import Casillero
        from myapp.serializers import CasilleroSerializer

        casilleros = Casillero.objects.all()

        casilleros_serializer = CasilleroSerializer(casilleros, many=True).data

        context = {
            'casilleros': casilleros_serializer
        }

        return render(request, "controller.html", context)
    
class casillero_view(View):
    def get(self, request, id):
        from myapp.models import Casillero
        from myapp.serializers import CasilleroSerializer

        casilleros = Casillero.objects.get(id=id)
        casillero_serializer = CasilleroSerializer(casilleros).data

        context = {
            'casillero': casillero_serializer
        }

        return render(request, 'casillero.html', context)

class casillero_edit(View):
    def get(self, request, id):
        from myapp.models import Casillero
        from myapp.serializers import CasilleroSerializer

        casillero = Casillero.objects.get(id=id)
        casillero_serializer = CasilleroSerializer(casillero).data

        context = {
            'casillero': casillero_serializer
        }

        return render(request, 'casillero_edit.html', context)
    
    # @csrf_exempt
    def post(self, request, id):
        from myapp.models import Casillero

        response = request.POST

        casillero = Casillero.objects.get(id=id)
        casillero.email = response['email']
        casillero.password = response['password']

        casillero.save()
        publish_new_key_mqtt(casillero.id, casillero.password)
        send_email_with_image(response['email'], response['password'], id)

        return redirect('controller')

def send_email_with_image(user_mail, user_password, casillero_id):
    subject = f"Clave Casillero { casillero_id }"
    recipient_list = [user_mail]
    
    # Crea el contenido HTML del correo
    html_content = f"""
    <html>
    <body>
        <h2>Instrucciones para abrir el casillero</h2>
        <ul>
            <li>Seleccionar repetidamente el botón deselección hasta estar en el casillero deseado, indicado por el led</li>
            <li>Confirmar la selección del casillero con el botón de selección</li>
            <li>Mantener el gesto correspondiente de la clave hasta que se encienda la luz verde indicando que el gesto es correcto</li>
            <li>Repetir con los siguientes gestos hasta que se enciendan las cuatro luces en verde y se abra el casillero</li>
        </ul>
        <p>A continuación se muestran los gestos de su clave:</p>
        <p><strong>Clave del casillero: {user_password}</strong></p> <!-- Aquí se incluye la clave -->
    """
    
    # Ruta de la carpeta donde están las imágenes
    images_path = os.path.join(settings.BASE_DIR, 'myapp', 'utils')
    email = EmailMessage(subject, "", settings.EMAIL_HOST_USER, recipient_list)
    
    try:
        # Añade cada imagen tantas veces como caracteres en la clave
        for char in user_password:
            image_name = f"{char}.jpg"
            image_path = os.path.join(images_path, image_name)
            with open(image_path, 'rb') as img:
                # Adjunta la imagen en modo "inline"
                email.attach(image_name, img.read(), 'image/jpeg')
            
            # Incluye la imagen en el cuerpo del correo para mostrarlas en el HTML
            html_content += f'<img src="cid:{image_name}" alt="Imagen clave {char}"><br>'

        # Cierra el contenido HTML
        html_content += """
        </body>
        </html>
        """
        
        # Establece el contenido HTML del mensaje
        email.content_subtype = "html"
        email.body = html_content
        # Envía el correo
        email.send()
        print("Correo enviado con éxito con las imágenes incrustadas en el HTML.")

    except Exception as e:
        print(f"Error al enviar el correo: {e}")


def send_open_mail(casillero):
    subject = f"Casillero {casillero['id']} abierto"
    recipient_list = [casillero['email']]

    html_content = """
    <html>
    <body>
        <p>El casillero ha sido abierto.</p>
    </body>
    </html>
    """
    email = EmailMessage(subject, "", settings.EMAIL_HOST_USER, recipient_list)

    email.content_subtype = "html"
    email.body = html_content
    # Envía el correo
    email.send()
    print("Correo enviado con éxito indicando que se abrió el casillero.")



def publish_new_key_mqtt(casillero_id, new_password):
    message = f'{{"locker_id": {casillero_id}, "message": "{new_password}"}}'

    # Publica el mensaje en el tema
    client.publish(topic_out, message)
