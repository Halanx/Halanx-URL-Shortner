# noinspection PyUnusedLocal
def get_qr_code_upload_path(instance, filename):
    return "qrcode/{}/{}.png".format(instance.id, instance.short)
