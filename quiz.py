from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

message = b'gAAAAABcy37C0KA5ZBKIXSbC8uvNvRqWvb6ywydQ4CFuEubg4YDd89vW1VoJVRF00zaUns7yA0bsCBA-IFpDE0d35_joXSWKJSyGv4zMf2eKOgO3TpM9Z5nHembylcVw76z8A504qXNQeWM_PWn8CPrqvGCV_XmQqMQznziFU-BccCl61UkEyBqN9Xmy9TlumaXY4RlDdhzX'

def main():
     f = Fernet(key)
     print(f.decrypt(message))


if __name__ == "__main__":
    main()
