# import cv2
# import face_recognition
# import qrcode
# from googletrans import Translator
#
#
# # Face recognition
# def face(a, b):
#     img = cv2.imread(a)
#     rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img_encoding = face_recognition.face_encodings(rgb_img)[0]
#
#     img2 = cv2.imread(b)
#     rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
#     img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]
#
#     result = face_recognition.compare_faces([img_encoding], img_encoding2)
#     return result
#
#
# # QR Code create and read
# def createqr(name, text):
#     qr = qrcode.make(text)
#     qr.save(f'{name}.png')
#     return f'{name}.png'
#
#
# def readqr(img):
#     d = cv2.QRCodeDetector()
#     url, _, _ = d.detectAndDecode(cv2.imread((img)))
#     return url


# Google translator
# def trans(txt, lang):
#     strtxt = str(txt)
#     translator = Translator()
#     tt = translator.translate(strtxt, dest=lang, src='auto').text
#     return tt



