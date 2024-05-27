from email.header import decode_header

def decode_mime_words(s):
    decoded_words = decode_header(s)
    return ''.join(word.decode(encoding or 'utf8') if isinstance(word, bytes) else word for word, encoding in decoded_words)

def set_email_content(result):
    disclaimer_message = "<p style=\"font-size: 11px;\">Descargo de Responsabilidad: Este servicio es una prueba de concepto para ser utilizada y demostrada en un Trabajo Final Integrador de la carrera Ingeniería en Informática de la Universidad UNSTA, Tucumán. Su certeza está solo probada en mails con contenido en <b>inglés</b>. Si bien esta certeza está calculada en un 90% (REVISAR), no se garantiza que el resultado sea exacto. La mejor herramienta es la educación. Visitá el siguiente enlace para acceder a una infografía sobre Phishing: ENLACE. El servicio no cobra responsabilidad alguna por haber detectado incorrectamente un tipo de mail. <b>Por favor, tené cuidado al operar y abrir enlaces en la web. Nunca envíes información confidencial por mail</b>, como ser contraseñas, números de tarjetas de crédito, etc.</p>"

    message = ''
    if result == -1:
        message = '⚠️ <b>ATENCION</b>: Este correo es <b>sospechoso</b>, y podría tratarse de un correo de phishing (fraudulento). Por favor, tené cuidado y no entres a ningún enlace.\n\nGracias por usar nuestro servicio!'
    else:
        message = '✅ Este correo parece ser <b>seguro</b>. Sin embargo, siempre tené cuidado al operar y abrir enlaces en la web.\n\nGracias por usar nuestro servicio!'

    return message + '\n\n' + disclaimer_message

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'