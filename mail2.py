import imaplib
import email
from email.header import decode_header
import webbrowser
import os
from getpass import getpass


def login():
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        status, data = imap.login(username, password)

        if status == "OK":
            print(f'Logged in as {username}')
            return imap
        else:
            raise Exception(status)
    except Exception as error:
        print(f"Error al logear {username}: {error}")


def get_OTP(imap: imaplib.IMAP4_SSL):
    try:
        status, inbox_messages = imap.select("INBOX")
        print('get inbox:', status)

        inbox_messages_len = int(inbox_messages[0])

        N = 10
        for i in range(inbox_messages_len, inbox_messages_len - N, -1):
            get_mail(imap, i)

    except Exception as error:
        print(f"Error obtener OTP {username}: {error}")


def get_mail(imap: imaplib.IMAP4_SSL, i: int):
    res, mensajes = imap.fetch(str(i), "(RFC822)")
    print('get mail:', res)

    for respuesta in mensajes:
        if isinstance(respuesta, tuple):
            mensaje = email.message_from_bytes(respuesta[1])
            subject = decode_header(mensaje["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()

            # from_ = mensaje.get("From")
            # print("Subject:", subject)
            # print("From:", from_)
            # print("Mensaje obtenido con exito")
            if mensaje.is_multipart():
                # Recorrer las partes del correo
                for part in mensaje.walk():
                    # Extraer el contenido
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # el cuerpo del correo
                        body = part.get_payload(decode=True).decode()
                        if content in body:
                            print('walk ' + body)
                    except:
                        pass
                    # if content_type == "text/plain" and "attachment" not in content_disposition:
                    #     # Mostrar el cuerpo del correo
                    #     if content in body:
                    #         print('walk ' + body)
                    # elif "attachment" in content_disposition:
                    #     #                         # download attachment
                    #     nombre_archivo = part.get_filename()
                    #     if nombre_archivo:
                    #         if not os.path.isdir(subject):
                    #             # crear una carpeta para el mensaje
                    #             os.mkdir(subject)
                    #         ruta_archivo = os.path.join(
                    #             subject, nombre_archivo)
                    #         # download attachment and save it
                    #         open(ruta_archivo, "wb").write(
                    #             part.get_payload(decode=True))
        else:
            # contenido del mensaje
            content_type = mensaje.get_content_type()
            # cuerpo del mensaje
            body = mensaje.get_payload(decode=True).decode()
            if content_type == "text/plain":
                #                     # mostrar solo el texto
                if content in body:
                    print('walk 2 ' + body)


def otro():
    try:
        res, mensaje = imap.fetch(str(mensajes), "(RFC822)")
    except:
        print("No hay mensajes")

    for respuesta in mensaje:
        if isinstance(respuesta, tuple):
            # Obtener el contenido
            mensaje = email.message_from_bytes(respuesta[1])
            # decodificar el contenido
            subject = decode_header(mensaje["Subject"])[0][0]
            if isinstance(subject, bytes):
                # convertir a string
                subject = subject.decode()
            # de donde viene el correo
            from_ = mensaje.get("From")
            print("Subject:", subject)
            print("From:", from_)
            print("Mensaje obtenido con exito")
            # si el correo es html
            if mensaje.is_multipart():
                # Recorrer las partes del correo
                for part in mensaje.walk():
                    # Extraer el contenido
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # el cuerpo del correo
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # Mostrar el cuerpo del correo
                        print(body)
                    elif "attachment" in content_disposition:
                        #                         # download attachment
                        nombre_archivo = part.get_filename()
                        if nombre_archivo:
                            if not os.path.isdir(subject):
                                # crear una carpeta para el mensaje
                                os.mkdir(subject)
                            ruta_archivo = os.path.join(
                                subject, nombre_archivo)
                            # download attachment and save it
                            open(ruta_archivo, "wb").write(
                                part.get_payload(decode=True))
            else:
                # contenido del mensaje
                content_type = mensaje.get_content_type()
                # cuerpo del mensaje
                body = mensaje.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    #                     # mostrar solo el texto
                    print(body)
            # if content_type == "text/html":
            #     # Abrir el html en el navegador
            #     if not os.path.isdir(subject):
            #         os.mkdir(subject)
            #     nombre_archivo = f"{subject}.html"
            #     ruta_archivo = os.path.join(subject, nombre_archivo)
            #     open(ruta_archivo, "w").write(body)
            #     # abrir el navegador
            #     webbrowser.open(ruta_archivo)
    #             print("********************************")
    imap.close()
    imap.logout()


def logging(username, password):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password)

    status, mensajes = imap.select("INBOX")
    # print(mensajes)
    # mensajes a recibir
    N = 30
    # cantidad total de correos
    mensajes = int(mensajes[0])

    for i in range(mensajes, mensajes - N, -1):
        # print(f"vamos por el mensaje: {i}")
        #     # Obtener el mensaje
        try:
            res, mensaje = imap.fetch(str(i), "(RFC822)")
        except:
            break
        for respuesta in mensaje:
            if isinstance(respuesta, tuple):
                # Obtener el contenido
                mensaje = email.message_from_bytes(respuesta[1])
                # decodificar el contenido
                subject = decode_header(mensaje["Subject"])[0][0]
                if isinstance(subject, bytes):
                    # convertir a string
                    subject = subject.decode()
                # de donde viene el correo
                from_ = mensaje.get("From")
                # print("Subject:", subject)
                # print("From:", from_)
                # print("Mensaje obtenido con exito")
                # si el correo es html
                if mensaje.is_multipart():
                    # Recorrer las partes del correo
                    for part in mensaje.walk():
                        # Extraer el contenido
                        # content_type = part.get_content_type()
                        # content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # el cuerpo del correo
                            body = part.get_payload(decode=True).decode()
                            otp = search_otp_into_body(body, content)
                            if otp != None:
                                break
                        except:
                            pass

                #         if content_type == "text/plain" and "attachment" not in content_disposition:
                #             # Mostrar el cuerpo del correo
                #             print(body)
                #         elif "attachment" in content_disposition:
                #             #                         # download attachment
                #             nombre_archivo = part.get_filename()
                #             if nombre_archivo:
                #                 if not os.path.isdir(subject):
                #                     # crear una carpeta para el mensaje
                #                     os.mkdir(subject)
                #                 ruta_archivo = os.path.join(
                #                     subject, nombre_archivo)
                #                 # download attachment and save it
                #                 open(ruta_archivo, "wb").write(
                #                     part.get_payload(decode=True))
                else:
                    # contenido del mensaje
                    content_type = mensaje.get_content_type()
                    # cuerpo del mensaje
                    body = mensaje.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        otp = search_otp_into_body(body, content)
                        if otp != None:
                            break
                # if content_type == "text/html":
                #     # Abrir el html en el navegador
                #     if not os.path.isdir(subject):
                #         os.mkdir(subject)
                #     nombre_archivo = f"{subject}.html"
                #     ruta_archivo = os.path.join(subject, nombre_archivo)
                #     open(ruta_archivo, "w").write(body)
                #     # abrir el navegador
                #     webbrowser.open(ruta_archivo)
    #             print("********************************")
    imap.close()
    imap.logout()

def search_otp_into_body(body, content):
    if content in body:
        print(body)
        return body
    else:
        return None
logging(username, password)