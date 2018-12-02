from app.boilerplate import put_file, get_file, minioClient, MINIO_BUCKET_NAME
import os
import shutil

ASSETSDIR = "/home/laks/hseling-api-catandkittens/tests/assets/upload"
FGETTED = os.path.join("/home/laks/hseling-api-catandkittens/tests/assets", 'fgetted')


def test_upload():

    for asset in os.listdir(ASSETSDIR):
        put_file(os.path.join(ASSETSDIR,asset))

    os.mkdir(FGETTED)

    for asset in os.listdir(ASSETSDIR):
        if asset != 'fgetted':
            filepath = os.path.join(FGETTED, asset)
            get_file(MINIO_BUCKET_NAME, asset, filepath)
            minioClient.remove_object(MINIO_BUCKET_NAME, asset)
    assert set(os.listdir(ASSETSDIR)) == set(os.listdir(FGETTED))


    shutil.rmtree(FGETTED)
