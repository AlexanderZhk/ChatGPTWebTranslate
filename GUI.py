def RunGUI(DeeplHandler):
    totranslate = 0
    while totranslate != "e":
        totranslate= input()
        print(DeeplHandler.translate(totranslate,0))