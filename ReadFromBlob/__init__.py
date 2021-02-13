import logging
import azure.functions as func

def _rot13(c):
    if 'A' <= c and c <= 'Z':
        return chr((ord(c) - ord('A') + 13) % 26 + ord('A'))
    if 'a' <= c and c <= 'z':
        return chr((ord(c) - ord('a') + 13) % 26 + ord('a'))
    return c

def process_rot13(s):
    g = (_rot13(c) for c in s)
    return ''.join(g)

def main(queuemsg: func.QueueMessage, inputblob: func.InputStream, outputblob: func.Out[str]) -> None:

    # 1. Print 'Item name' from Queue Message
    logging.info('Queue item id:%s, body:%s, expiration_time:%s', queuemsg.id, queuemsg.get_body().decode('utf-8'), queuemsg.expiration_time)

    # 2. Read Blob file (the File name is the same as the item name from Queue message )
    clear_text = inputblob.read().decode('utf-8')
    logging.info("Clear text:%s'", clear_text)

    # 3. Process: Encrypt text with ROT13 encryption
    encrypted_text= process_rot13(clear_text)
    logging.info("Encrypted text:%s", encrypted_text)

    # 4. Write to Blob file:  Write encrypted_text to blob file
    outputblob.set(encrypted_text)
    logging.info("Done storing encrypted text")

# https://github.com/tensorflow/tensorflow/tree/v1.14.0
# pip install -e git://github.com/{ username }/{ reponame }.git@{ tag name }#egg={ desired egg name }
# pip install -e git://github.com/tensorflow/tensorflow.git@v1.14.0