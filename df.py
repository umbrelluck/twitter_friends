import urllib.request
import json
import twurl
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

URL_friends = "https://api.twitter.com/1.1/friends/list.json"
info = {}
path = ""


def user_input():
    ans = input("abhqg ")
    if ans in "q":
        raise EOFError
    elif ans == "b":
        raise NotImplementedError
    return ans


def look(what):
    global path
    try:
        if type(what) == dict:
            tmp = list(what.keys())
            section = "".join(str(key) + " | " if key != tmp[-1] else str(key) for key in what)
            print(section + "\n")
            ans = user_input()
            path += "/" + ans
            return look(what[ans])
        elif type(what) == list:
            if "name" in what[0]:
                section = "".join(
                    elem["name"] + " | " if elem != what[-1] else elem["name"] for elem in what)
                print(section + "\n")
                ans = user_input()
                for user in what:
                    if ans == user["name"]:
                        path += "/" + str(what.index(user))
                        return look(user)
                else:
                    raise EOFError
            else:
                section = "".join(
                    str(elem) + " | " if elem != what[-1] else str(elem) for elem in what)
                print(section + "\n")
                ans = user_input()
                return look(ans)
        else:
            print(what)
            return
    except EOFError:
        print('Exiting...')
        return None
    except NotImplementedError:
        print("../")
        global info
        new_what = info
        for elem in path.split("/"):
            if elem is not '':
                try:
                    new_what = new_what[int(elem)]
                except Exception as e:
                    new_what = new_what[elem]
        return look(new_what)
    except KeyError:
        print('Invalid input')
        return look(what)


def main():
    acc = input("Enter account name: ")
    if len(acc) < 1:
        return -1
    else:
        url = twurl.augment(URL_friends, {"screen_name": acc})
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()
        global info
        info = json.loads(data)
        look(info)


if __name__ == "__main__":
    main()
