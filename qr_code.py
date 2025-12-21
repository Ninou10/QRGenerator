import qrcode

# Lien vers lequel le QR code doit diriger
url = "https://medium.com/@deepikagundrathi02/navigating-the-trade-offs-in-machine-learning-model-complexity-selection-overfitting-and-e4ac86227186"

# Création du QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # correction d'erreur élevée
    box_size=10,
    border=4,
)

qr.add_data(url)
qr.make(fit=True)

# Création de l'image
img = qr.make_image(fill_color="black", back_color="white")

# Sauvegarde de l'image
img.save("qr_site.png")

print("QR code généré : scanne-le pour ouvrir le site !")
